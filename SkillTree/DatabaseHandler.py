import configparser
import os
import sys

from supabase import Client, create_client

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.ini'))

parent_module = sys.modules[".".join(__name__.split(".")[:-1]) or "__main__"]
if __name__ == "__main__" or parent_module.__name__ == "__main__":
    from CSVHandler import CSVHandler
    from Skill import Skill
else:
    from .CSVHandler import CSVHandler
    from .Skill import Skill

SUPABASE_URL = config["DATABASE"]["DATABASE_URL"]
SUPABASE_KEY = config["DATABASE"]["DATABASE_API_KEY"]

class DatabaseHandler:
    def __init__(self, database:str = "skills.sqlite") -> None:
        self.database = database
    
    def update_data(self) -> int:
        data = CSVHandler.load_skills_from_csv()
        data = [item.export() for item in data]
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        try:
            return_data = supabase.table("Skills").upsert(data).execute()
                
            inserted = len(return_data.data)
        except:
            # conn.rollback()
            raise
        print(f"Inserted {inserted} new rows")
        return inserted

    
    def get_data(self, raw=False) -> list[Skill] or list[tuple]:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
        data = supabase.table("Skills").select("*").execute()
        
        skills = [tuple(skill.values()) for skill in data.data]
        if raw:
            return skills
        skills = [Skill().import_data(data) for data in skills]
        return skills
    
    def get_headers(self) -> list[str]:
        with sqlite3.connect(self.database) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM skills LIMIT 0")
            
            headers = [column[0] for column in c.description]
        return headers
            
        
if __name__ == "__main__":
    db = DatabaseHandler()

    db.update_data()