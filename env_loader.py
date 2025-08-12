import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ['GEMINI_API_KEY']
CHROMA_PATH = "chromadb"
DATA_PATH = "data"

FILES_FOR_DATABASE = [
    {
        "name": "about_data.json",
        "link":"https://muditgarg48.github.io/portfolio_data/data/about_data.json",
    },
    {
        "name": "certificates_data.json",
        "link":"https://muditgarg48.github.io/portfolio_data/data/certificates_data.json",
    },
    {
        "name": "education_history.json",
        "link":"https://muditgarg48.github.io/portfolio_data/data/education_history.json",
    },
    {
        "name": "experience_data.json",
        "link":"https://muditgarg48.github.io/portfolio_data/data/experience_data.json",
    },
    {
        "name": "facts_data.json",
        "link":"https://muditgarg48.github.io/portfolio_data/data/facts_data.json",
    },
    {
        "name": "projects_data.json",
        "link":"https://muditgarg48.github.io/portfolio_data/data/projects_data.json",
    },
    {
        "name": "skills.json",
        "link":"https://muditgarg48.github.io/portfolio_data/data/skills.json",
    },
    {
        "name": "Current Resume.pdf",
        "link":"https://muditgarg48.github.io/portfolio_data/documents/My Resume.pdf",
    },
]