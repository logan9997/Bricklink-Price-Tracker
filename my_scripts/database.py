import sqlite3
import datetime


class DatabaseManagment():

    def __init__(self) -> None:
        self.con = sqlite3.connect(r"C:\Users\logan\OneDrive\Documents\Programming\Python\api's\BL_API\database.db", check_same_thread=False)
        self.cursor = self.con.cursor()


    def add_price_info(self, item) -> None:
        #add all prices for current day
        today = datetime.date.today()
        print(item["item"]["no"])
        try:
            self.cursor.execute(f"""
                INSERT INTO Price VALUES
                (
                    '{item["item"]["no"]}', '{today}', '{round(float(item["avg_price"]), 2)}',
                    '{round(float(item["min_price"]),2)}', '{round(float(item["max_price"]),2)}',
                    '{item["total_quantity"]}'
                )
            """)
        except sqlite3.IntegrityError:
            pass
        self.con.commit()


    def get_all_items(self) -> list[str]:
        #return a list of all items inside 'Price' table
        result = self.cursor.execute(f"""
            SELECT item_id
            FROM Price
            GROUP BY item_id
        """)
        return [str(fig_id).split("'")[1] for fig_id in result.fetchall()]


    def check_for_todays_date(self) -> int:
        today = datetime.date.today()
        result = self.cursor.execute(f"""
            SELECT COUNT()
            FROM Price
            WHERE date = '{today}'
        """)
        return result.fetchall()


    def get_minifig_prices(self, minifig_id) -> list[str]:
        result = self.cursor.execute(f"""
            SELECT date, avg_price, min_price, max_price, total_qty
            FROM Price
            WHERE item_id = '{minifig_id}'
        """)
        
        return result.fetchall()

    def get_dates(self, minifig_id) -> list[str]:
        result = self.cursor.execute(f"""
            SELECT date
            FROM Price
            WHERE item_id = '{minifig_id}'
        """)
        return result.fetchall()     

    
    def get_biggest_trends(self) -> list[str]:
        result = self.cursor.execute('''
            SELECT name, P1.item_id, round(avg_price - (
                SELECT avg_price
                FROM price P2
                WHERE P2.item_id = P1.item_id
                    AND date = (
                        SELECT max(date)
                        FROM price
                    ) 
            ),2) as [£ change]

            FROM price P1, item I
            WHERE I.item_id = P1.item_id 
                AND date = (
                    SELECT min(date)
                    FROM price
                ) 
            ORDER BY [£ change] desc
        ''')

        result = result.fetchall()
        losers = result[len(result)-10:][::-1]
        winners = result[:10]
        return losers, winners


    def group_by_items(self) -> list[str]:
        result = self.cursor.execute(f"""
            SELECT item_id, type
            FROM item
            GROUP BY item_id
        """)
        return result.fetchall()


    def get_parent_themes(self) -> list[str]:
        result = self.cursor.execute(f"""
            SELECT REPLACE(theme_path, '/', ''), thumbnail_url
            FROM item
            WHERE theme_path NOT LIKE '%~%'
                AND type = 'S'
            GROUP BY theme_path
        """)
        return result.fetchall()


    def get_theme_items(self, theme_path) -> list[str]:
        result = self.cursor.execute(f"""
            SELECT item_id, type
            FROM item
            WHERE theme_path = '{theme_path}'
        """)
        return result.fetchall()      


    def get_item_ids(self) -> list[str]:
        result = self.cursor.execute(f"""
            SELECT item_id, type
            FROM item
            GROUP BY item_id
        """)
        return result.fetchall()


    def insert_thumbnail_url_name(self, details) -> None:
        self.cursor.execute(f"""
            UPDATE item
            SET thumbnail_url = '{details.get("thumbnail_url")}', name = '{details.get("name")}'
            WHERE item_id = '{details.get("item_id")}'
        """)
        self.con.commit()


    def insert_year_released(self, year_released, item_id) -> None:
        self.cursor.execute(f"""
            UPDATE item
            SET year_released = '{year_released}'
            WHERE item_id = '{item_id}'
        """)
        self.con.commit()


    def get_item_info(self, item_id) -> list[str]:
        result = self.cursor.execute(f"""
            SELECT item_id, name, year_released, thumbnail_url
            FROM item
            WHERE item_id = '{item_id}'
            GROUP BY item_id
        """)
        return result.fetchall()

    def get_not_null_years(self) -> list[str]:
        result = self.cursor.execute(f"""
            SELECT item_id
            FROM item
            WHERE year_released is null
        """)
        return result.fetchall()


    def get_thumbnail_url(self, item_id) -> str:
        result = self.cursor.execute(f"""
            SELECT thumbnail_url
            FROM item
            WHERE item_id = '{item_id}'
            GROUP BY item_id
        """)
        return result.fetchall()        


#update database without calling a view
def main():
    pass
    
if __name__ == "__main__":
    main()
