from dotenv import load_dotenv
from pathlib import Path
import os 

app_dir = Path(__file__).resolve().parent
env_file = app_dir / '.env'

# print(Path('.').resolve())
load_dotenv(env_file)

class Config:
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG')
    SECRET_KEY = os.environ.get('SECRET_KEY') #key to security
    FLASK_APP = os.environ.get('FLASK_APP')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False