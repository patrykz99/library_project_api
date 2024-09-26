from dotenv import load_dotenv
from pathlib import Path
import os

app_dir = Path(__file__).resolve().parent
env_file = app_dir / '.env'

# print(Path('.').resolve())
load_dotenv(env_file)

class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') #key to security