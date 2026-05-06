import os
import sys
from src.logger import logging
from src.exception import CustomException
from dotenv import load_dotenv
from supabase import create_client, Client
from src.db.db import TableManager
load_dotenv()


if __name__=="__main__":
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    logging.info("Creating Supabase API connection.")

    user_table = TableManager(table="users", client=supabase)
    session_table = TableManager(table="sessions", client=supabase)
    logging.info("Creating connection to PostgreSQL tables.")
