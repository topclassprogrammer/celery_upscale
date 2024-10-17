import os

from dotenv import load_dotenv

load_dotenv()

REDIS_BROKER_DSN = os.getenv('REDIS_BROKER_DSN')
REDIS_BACKEND_DSN = os.getenv('REDIS_BACKEND_DSN')
MONGO_DSN = os.getenv('MONGO_DSN')
MODEL_PATH = 'EDSR_x2.pb'
TIMEOUT_TASK = 30
