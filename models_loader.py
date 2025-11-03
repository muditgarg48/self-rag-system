import google.generativeai as genai
from langchain_huggingface import HuggingFaceEmbeddings

from env_loader import API_KEY

# Cache embedding function globally
_embedding_function = None

def get_embedding_function():
    global _embedding_function
    if _embedding_function is None:
        model_name = "sentence-transformers/all-MiniLM-L6-v2"  # lightweight, good quality
        # model_name = "sentence-transformers/all-mpnet-base-v2"  # higher quality, slightly heavier
        print("Loading embedding model (first time only)...")
        _embedding_function = HuggingFaceEmbeddings(model_name=model_name)
        print("Embedding model loaded and cached.")
    return _embedding_function

# Cache chat model globally to avoid recreating on every request
_chat_model = None

def get_chat_model():
    global _chat_model
    if _chat_model is None:
        genai.configure(api_key=API_KEY)
        print("Initializing chat model (first time only)...")
        _chat_model = genai.GenerativeModel("gemini-2.5-flash")
        print("Chat model initialized and cached.")
    return _chat_model