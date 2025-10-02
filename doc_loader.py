from langchain.schema import Document
from langchain_community.vectorstores import FAISS
import os, shutil, requests
from threading import Thread

from env_loader import FAISS_PATH, FILES_FOR_DATABASE, DATA_PATH
from models_loader import get_embedding_function
from langchain_loader import get_pdf_loader, get_text_splitter, get_txt_loader, get_json_semantic_docs

# Global FAISS reference
db = None

def main():
    download_files()
    build_faiss_index()
    save_faiss_index_locally()

def download_files():
    print("Downloading files for RAG system preparation!")
    if os.path.exists(DATA_PATH):
        shutil.rmtree(DATA_PATH)
    os.makedirs(DATA_PATH)
    for file in FILES_FOR_DATABASE:
        response = requests.get(file['link'])
        with open(os.path.join(DATA_PATH, file['name']), "wb") as f:
            f.write(response.content)

def load_documents():
    pdf_loader = get_pdf_loader()
    text_loader = get_txt_loader()
    # print("Loader ready")
    print("Loading .pdf files:", end=' ')
    pdf_docs = pdf_loader.load()
    print(f"{len(pdf_docs)} found")
    print("Loading .txt files:", end=' ')
    txt_docs = text_loader.load()
    print(f"{len(txt_docs)} found")
    print("Loading .json files:", end=' ')
    json_docs = get_json_semantic_docs()
    print("============= ✅ ================")
    return pdf_docs + txt_docs + json_docs

def split_documents(documents: list[Document]):
    text_splitter = get_text_splitter()
    chunks = []
    for doc in documents:
        if doc.metadata.get("source","").endswith(".json"):
            # JSON: keep as-is (semantic already)
            chunks.append(doc)
        else:
            # PDFs/TXTs: split
            chunks.extend(text_splitter.split_documents([doc]))
    print(f"📦 Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def build_faiss_index():
    global db
    documents = load_documents()
    chunks = split_documents(documents)
    faiss_embedding_function = get_embedding_function()
    print(f"📇 FAISS index with {len(chunks)} chunks built!")
    db = FAISS.from_documents(chunks, faiss_embedding_function)
    print("📲 Built FAISS index stored in-memory")

def save_faiss_index_locally():
    global db
    if db is None:
        print("⚠️ No FAISS index in memory to save.")
        return
    if os.path.exists(FAISS_PATH):
        shutil.rmtree(FAISS_PATH)
    db.save_local(FAISS_PATH)
    print(f"🏁 FAISS index saved to {FAISS_PATH}.")

def init_faiss_index():
    global db
    embedding_fn = get_embedding_function()

    # 1. Load prebuilt index from repo
    if os.path.exists(FAISS_PATH):
        try:
            db = FAISS.load_local(FAISS_PATH, embedding_fn, allow_dangerous_deserialization=True)
            print(f"Loaded FAISS index from {FAISS_PATH}")
        except Exception as e:
            print(f"Failed to load FAISS index: {e}")

    # 2. Kick off async rebuild (non-blocking)
    def rebuild():
        print("Rebuilding FAISS index in-memory...")
        # Swap global reference
        build_faiss_index()

        # Overwrite persisted repo index (disk write)
        save_faiss_index_locally()
        print(f"Saved refreshed FAISS index to {FAISS_PATH}")

    Thread(target=rebuild, daemon=True).start()

if __name__ == "__main__":
    main()