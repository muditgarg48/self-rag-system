from langchain.schema import Document
from langchain_chroma import Chroma
import os
import shutil
import requests

from env_loader import CHROMA_PATH, FILES_FOR_DATABASE, DATA_PATH
from genai_loader import get_embedding_function
from langchain_loader import get_pdf_loader, get_text_splitter, get_txt_loader, get_json_loader

def main():
    download_files()
    generate_data_store()

def download_files():
    print("Downloading files for RAG system preparation!")
    if os.path.exists(DATA_PATH):
        shutil.rmtree(DATA_PATH)
    os.makedirs(DATA_PATH)
    for file in FILES_FOR_DATABASE:
        response = requests.get(file['link'])
        with open(os.path.join(DATA_PATH,file['name']), "wb") as f:
            f.write(response.content)

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    pdf_loader = get_pdf_loader()
    text_loader = get_txt_loader()
    json_loader = get_json_loader()
    # print("Loader ready")
    print("Loading .pdf files:")
    pdf_docs = pdf_loader.load()
    print("Loading .txt files:")
    txt_docs = text_loader.load()
    print("Loading .json files:")
    json_docs = json_loader.load()
    print("Done!!")
    documents = pdf_docs + txt_docs + json_docs
    return documents

def split_text(documents: list[Document]):
    text_splitter = get_text_splitter()
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks

def save_to_chroma(chunks: list[Document]):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    google_embedding_function = get_embedding_function()
    Chroma.from_documents(
        chunks, google_embedding_function, persist_directory=CHROMA_PATH
    )
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()