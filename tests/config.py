import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
TIMEOUT_TASK = 30
