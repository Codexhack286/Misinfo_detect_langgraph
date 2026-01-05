import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_FACTCHECK_KEY = os.getenv("GOOGLE_FACTCHECK_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
