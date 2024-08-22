import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ['GEMINI_API_KEY']
CHROMA_PATH = "chromadb"
DATA_PATH = "data"

FILES_FOR_DATABASE = [
    {
        "name": "certificates_data.json",
        "link":"https://raw.githubusercontent.com/muditgarg48/muditgarg48.github.io/master/src/assets/data/certificates_data.json",
    },
    {
        "name": "education_history.json",
        "link":"https://raw.githubusercontent.com/muditgarg48/muditgarg48.github.io/master/src/assets/data/education_history.json",
    },
    {
        "name": "experience_data.json",
        "link":"https://raw.githubusercontent.com/muditgarg48/muditgarg48.github.io/master/src/assets/data/experience_data.json",
    },
    {
        "name": "projects_data.json",
        "link":"https://raw.githubusercontent.com/muditgarg48/muditgarg48.github.io/master/src/assets/data/projects_data.json",
    },
    {
        "name": "skills.json",
        "link":"https://raw.githubusercontent.com/muditgarg48/muditgarg48.github.io/master/src/assets/data/skills.json",
    },
    {
        "name": "Current Resume.pdf",
        "link":"https://raw.githubusercontent.com/muditgarg48/muditgarg48.github.io/master/src/assets/pdfs/My Resume.pdf",
    },
]