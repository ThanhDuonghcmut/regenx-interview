import os

from dotenv import load_dotenv
from supabase import create_client, Client

from constant import DOTENV_PATH

load_dotenv(DOTENV_PATH)
SECRET_KEY = os.environ.get("JWT_SECRET")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_API_KEY = os.environ.get("SUPABASE_API_KEY")
client: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)