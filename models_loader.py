import google.generativeai as genai
from langchain_core.embeddings import Embeddings
from typing import List
from fastembed import TextEmbedding

from env_loader import API_KEY

class FastEmbedLangChain(Embeddings):

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        print(f"Initializing FastEmbed model: {model_name} (first time only)...")
        self.embedding_model = TextEmbedding(model_name=model_name)
        print("FastEmbed model loaded and cached.")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = list(self.embedding_model.embed(texts))
        # Convert numpy arrays to Python lists
        return [emb.tolist() if hasattr(emb, 'tolist') else list(emb) for emb in embeddings]
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a single query text."""
        embedding = list(self.embedding_model.embed([text]))[0]
        # Convert numpy array to Python list
        return embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)

# Cache embedding function globally
_embedding_function = None

def get_embedding_function():
    global _embedding_function
    if _embedding_function is None:
        # Use FastEmbed - lightweight, ONNX-based, no PyTorch needed!
        # Uses BAAI/bge-small-en-v1.5 which is optimized for CPU and small memory footprint
        _embedding_function = FastEmbedLangChain(model_name="BAAI/bge-small-en-v1.5")
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