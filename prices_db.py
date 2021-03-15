import sqlite3
from config import db_file, table_price, table_name
from datetime import datetime
from recipe import get_price, recipe

create_db = f"""
CREATE TABLE IF NOT EXISTS {table_price}
                    (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     shop_name TEXT NOT NULL,
                     date DATE,
                     price REAL NOT NULL
                    )
"""
conn = sqlite3.connect(db_file)
curs = conn.cursor()
curs.execute(create_db)


def get_last_update_price(shop):

    last_date = curs.execute(f"""
    SELECT max (date) FROM {table_price} WHERE shop_name like '{shop}'
    """).fetchone()[0]
    last_date = datetime.strptime(last_date, "%Y-%m-%d").date()

    return last_date


def write_price_to_db(shop):

    insert_table = f"""
    INSERT INTO {table_price} (shop_name, date, price) VALUES (?,?,?)
    """
    dd = (shop, datetime.now().date(), get_price(shop_name=shop, recipe=recipe))
    curs.execute(insert_table, dd)
    conn.commit()
