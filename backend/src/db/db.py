import os
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

    def create(self, data: dict):
        try:
            if not data:
                raise ValueError("Empty data")
            response = self.client.table(self.table).insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Create failed: {e}")
            return None

    def read_all(self):
        try:
            response = self.client.table(self.table).select('*').execute()
            return response.data
        except Exception as e:
            print(f"Read failed: {e}")
            return None

    def read_filter(self, col: str, value: str):
        try:
            response = self.client.table(self.table).select('*').eq(col, value).execute()
            return response.data
        except Exception as e:
            print(f"Filtered read failed: {e}")
            return None

    def update(self, col: str, value: str, data: dict):
        try:
            response = self.client.table(self.table).update(data).eq(col, value).execute()
            return response.data
        except Exception as e:
            print(f"Update failed: {e}")
            return None

    def delete(self, col: str, value: str):
        try:
            response = self.client.table(self.table).delete().eq(col, value).execute()
            return response.data
        except Exception as e:
            print(f"Delete failed: {e}")
            return None