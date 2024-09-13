from dotenv import load_dotenv
import os

load_dotenv()

dadata_token = os.environ.get("dadata_api_key")
dadata_secret = os.environ.get("dadata_secret_key")

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
SECRET_AUTH_KEY = os.environ.get("SECRET_AUTH_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
