from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import json, glob, os

from env_loader import DATA_PATH

def get_pdf_loader():
    pdf_loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)
    return pdf_loader

def get_txt_loader():
    text_loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    return text_loader

def get_json_semantic_docs():
    docs = []
    number_of_jsons = 0
    for filepath in glob.glob(os.path.join(DATA_PATH, "*.json")):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            number_of_jsons += 1

        # Handle dicts, lists, and nested objects gracefully
        if isinstance(data, dict):
            for key, val in data.items():
                docs.append(Document(
                    page_content=f"{key}: {val}",
                    metadata={"source": os.path.basename(filepath), "section": key}
                ))
        elif isinstance(data, list):
            for idx, obj in enumerate(data):
                docs.append(Document(
                    page_content=json.dumps(obj, indent=2),
                    metadata={"source": os.path.basename(filepath), "index": idx}
                ))
        else:
            docs.append(Document(
                page_content=str(data),
                metadata={"source": os.path.basename(filepath)}
            ))

    print(f"{number_of_jsons} found ({len(docs)} objects detected)")
    return docs

def get_text_splitter():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        add_start_index=True,
    )
    return text_splitter