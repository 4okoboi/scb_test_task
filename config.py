from dotenv import load_dotenv
import os

load_dotenv()

dadata_token = os.environ.get("dadata_api_key")
dadata_secret = os.environ.get("dadata_secret_key")
