from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai

from env_loader import API_KEY

def get_embedding_function():
    google_embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)
    return google_embedding_function

def get_chat_model():
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model