import sqlite3
import datetime

class DatabaseManagment():

    def __init__(self) -> None:
        self.con = sqlite3.connect(r"C:\Users\logan\OneDrive\Documents\Programming\Python\api's\BL_API\database.db")
        self.cursor = self.con.cursor()


    def add_category_info(self, categories) -> None:
        for category in categories:
            self.cursor.execute(f'''
                INSERT INTO Category VALUES
                ("{category["category_id"]}", "{category["category_name"]}")
            ''')
        self.con.commit()


    def add_price_info(self, items) -> None:
        today = datetime.date.today()
        for item in items:
            try:
                self.cursor.execute(f"""
                    INSERT INTO Price VALUES
                    ('{item["item"]["no"]}', '{today}', '{round(float(item["avg_price"]), 2)}')
                """)
            except sqlite3.IntegrityError:
                pass
        self.con.commit()