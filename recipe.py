import sqlite3
from config import db_file, table_name

recipe = {
    "pork": 500,
    "potatoes": 500,
    "beets": 500,
    "carrots": 200,
    "cabbage": 300,
    "onions": 200,
    "sour_cream": 200,
    "sunflower_oil": 20,
    "tomato_paste": 90,
}


conn = sqlite3.connect(db_file)
curs = conn.cursor()


def get_last_price_if_empty(shop_name, category):
    last_price = curs.execute(f"""
    SELECT price_for_100gr FROM {table_name} WHERE shop_name like '{shop_name}' AND category = '{category}' 
    AND date = (SELECT max(date) AS d FROM {table_name} WHERE date != (SELECT max(date) FROM {table_name})) LIMIT 1
    """).fetchall()[0][0]

    return last_price


def get_last_price(shop_name):
    data = []
    last_prices = []
    last_date = curs.execute(f"""
        SELECT max (date) FROM {table_name} WHERE shop_name like '{shop_name}'
        """).fetchone()[0]

    res = curs.execute(f"""
             SELECT * FROM {table_name} WHERE shop_name like '{shop_name}' AND date = '{last_date}'
             """).fetchall()

    # NOTE: Need tp rewrite this !!!
    for c in range(0,len(res)):
        data.append(dict(zip([c[0] for c in curs.description], res[c])))

    # ----------------
    for d in data:

        if d["price_for_100gr"] == "":
           d["price_for_100gr"] = get_last_price_if_empty(shop_name, d['category'])
        last_prices.append(d)

    return last_prices


def get_price(shop_name, recipe):
    last_shop_data = get_last_price(shop_name)

    for name, weight in recipe.items():
        borscht = []

        for item in last_shop_data:

            if item['unit'] == "weight":
                price = item['price_for_100gr']
                result_price = round(price * weight * 0.01, 2)
                borscht.append(result_price)

            elif item['unit'] == "count":

                if item["category"] == "sour_cream":
                    result_price = round(item['price_for_100gr'] * 200/350, 2)
                    borscht.append(result_price)

                elif item["category"] == "sunflower_oil":
                    result_price = round(item['price_for_100gr'] * 20/750, 2)
                    borscht.append(result_price)

                elif item["category"] == "tomato_paste":
                    result_price = round(item['price_for_100gr'] * 90/485, 2)
                    borscht.append(result_price)

        return (round(sum(borscht), 2))



