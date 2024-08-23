from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from env_loader import DATA_PATH

def get_pdf_loader():
    pdf_loader = DirectoryLoader(DATA_PATH, glob="*.pdf", show_progress=True, loader_cls=PyPDFLoader)
    return pdf_loader

def get_txt_loader():
    text_loader = DirectoryLoader(DATA_PATH, glob="*.txt", show_progress=True, loader_cls=TextLoader)
    return text_loader

def get_json_loader():
    json_loader = DirectoryLoader(DATA_PATH, glob='*.json', show_progress=True, loader_cls=JSONLoader, loader_kwargs = {'jq_schema':'.', 'text_content':False})
    return json_loader

def get_text_splitter():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=75,
        length_function=len,
        add_start_index=True,
    )
    return text_splitter