import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'database': os.environ.get('DB_NAME', 'f1_database'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', ''),
        'port': int(os.environ.get('DB_PORT', 5432))
    }
    
    OPENF1_API_BASE_URL = 'https://api.openf1.org/v1'