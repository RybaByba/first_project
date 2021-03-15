import sqlite3
from config import db_file, table_name
from datetime import datetime, timedelta

create_db = f"""
CREATE TABLE IF NOT EXISTS {table_name}
                    ( 
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     shop_name TEXT NOT NULL,
                     date DATE,
                     product_id TEXT NOT NULL,
                     product_name TEXT NOT NULL,
                     price_for_100gr REAL NOT NULL,
                     unit TEXT,
                     href CHAR(100),
                     category TEXT
                    )
"""

conn = sqlite3.connect(db_file)
curs = conn.cursor()
curs.execute(create_db)


def get_last_update(shop):

    last_date = curs.execute(f"""
        SELECT max (date) FROM {table_name} WHERE shop_name like '{shop}' 
        """).fetchone()[0]

    if last_date is not None:
        last_date = datetime.strptime(last_date, "%Y-%m-%d").date()

    else:
        last_date = datetime.now().date() - timedelta(days=1)

    return last_date


def write_to_db(dict):

    insert_table = f"""
    INSERT INTO {table_name} (shop_name, date, product_id, product_name, price_for_100gr, unit, href, category) 
    VALUES (?,?,?,?,?,?,?,?)
    """

    for item in dict.items():

        current_elem = item[1]
        curs.execute(
            insert_table,
                (
                    current_elem["shop_name"],
                    current_elem["date"],
                    current_elem["product_id"],
                    current_elem["product_name"],
                    current_elem["price"],
                    current_elem["unit"],
                    current_elem["href"],
                    item[0]

                )
            )

    conn.commit()



