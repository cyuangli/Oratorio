import os
import sys
from src.logger import logging
from src.exception import CustomException
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


class TableManager:
    def __init__(self, table: str, client: Client):
        self.table = table
        self.client = client

    def insert(self, data: dict):
        try:
            if not data:
                raise ValueError("Empty data")
            response = self.client.table(self.table).insert(data).execute()
            logging.info("Finished inserting data.")
            return response.data
        except Exception as e:
            raise CustomException(e, sys)
        
    def read_all(self):
        try:
            response = self.client.table(self.table).select('*').execute()
            logging.info("Finished reading all data.")
            return response.data
        except Exception as e:
            raise CustomException(e, sys)

    def read_filter(self, col: str, value: str):
        try:
            response = self.client.table(self.table).select('*').eq(col, value).execute()
            logging.info("Finished filter reading data.")
            return response.data
        except Exception as e:
            raise CustomException(e, sys)

    def update(self, col: str, value: str, data: dict):
        try:
            response = self.client.table(self.table).update(data).eq(col, value).execute()
            logging.info("Finished updating data.")
            return response.data
        except Exception as e:
            raise CustomException(e, sys)

    def delete(self, col: str, value: str):
        try:
            response = self.client.table(self.table).delete().eq(col, value).execute()
            logging.info("Finished deleting data.")
            return response.data
        except Exception as e:
            raise CustomException(e, sys)