import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    NAUKRI_USERNAME = os.getenv("NAUKRI_USERNAME")
    NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
    
    # LLM API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Job Search Criteria
    KEYWORDS = ["Generative AI", "System Architect", "LLM", "RAG"]
    LOCATION = "Remote"
    EXPERIENCE = 4
    
    # Paths
    RESUME_PATH = os.path.abspath("../main.tex")
    OUTPUT_DIR = os.path.abspath("./output")
