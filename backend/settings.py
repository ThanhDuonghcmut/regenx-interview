import os

from dotenv import load_dotenv

from constant import DOTENV_PATH

load_dotenv(DOTENV_PATH)
SECRET_KEY = os.environ.get("SUPABASE_API_KEY")