import sys
import sqlite3

parent_module = sys.modules[".".join(__name__.split(".")[:-1]) or "__main__"]
if __name__ == "__main__" or parent_module.__name__ == "__main__":
    from CSVHandler import CSVHandler
    from Skill import Skill
else:
    from .CSVHandler import CSVHandler
    from .Skill import Skill

CHECK_OLD_ROWS = True

class DatabaseHandler:
    def __init__(self, database:str = "skills.sqlite") -> None:
        self.database = database
    
    def check_for_new_data(self) -> int:
        data = CSVHandler.load_skills_from_csv()
        data = [item.export() for item in data]
        with sqlite3.connect(self.database) as conn:
            try:
                c = conn.cursor()
                    
                c.executemany('INSERT OR IGNORE INTO skills (name, archetype, prerequisite, casting_time, range, duration, uses, has_active, has_passive, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
                inserted = c.rowcount
            except:
                conn.rollback()
                raise
            conn.commit()
            print(f"Inserted {inserted} new rows")
            return inserted
    
    def update_data(self) -> int:
        data = CSVHandler.load_skills_from_csv()
        data = [item.export() for item in data]
        with sqlite3.connect(self.database) as conn:
            try:
                c = conn.cursor()
                    
                c.executemany('INSERT OR REPLACE INTO skills (name, archetype, prerequisite, casting_time, range, duration, uses, has_active, has_passive, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
                inserted = c.rowcount
            except:
                conn.rollback()
                raise
            conn.commit()
            print(f"Inserted {inserted} new rows")
            return inserted
    
    def get_data(self, raw=False) -> list[Skill] or list[tuple]:
        with sqlite3.connect(self.database) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM skills")
            
            skills = c.fetchall()
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
    if CHECK_OLD_ROWS:
        db.update_data()
    else:
        db.check_for_new_data()