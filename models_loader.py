import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings

from env_loader import API_KEY

def get_embedding_function():
    model_name = "sentence-transformers/all-MiniLM-L6-v2"  # lightweight, good quality
    # model_name = "sentence-transformers/all-mpnet-base-v2"  # higher quality, slightly heavier
    hf_embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return hf_embeddings

def get_chat_model():
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    return model