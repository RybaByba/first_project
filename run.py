from shops import fora, novus
from db import write_to_db, get_last_update
from prices_db import get_last_update_price, write_price_to_db
import datetime
from recipe import get_price, recipe

print(get_last_update(shop="novus"))


def update_data(shop):

    if get_last_update(shop) < datetime.date.today():

        if shop == "novus":
            dict = novus.get_data()

        elif shop == "fora":
            dict = fora.get_data()

        write_to_db(dict=dict)

    else:
        print(f"shop - { shop } - has current date ")


for shop in ['fora', 'novus']:
    update_data(shop)


def update_data_price(shop):

    if get_last_update_price(shop) < datetime.date.today():

        for shop in ['fora', 'novus']:
            get_price(shop, recipe)
            write_price_to_db(shop)
    else:
        print(f"price fo shop - { shop } - has current date ")


for shop in ['fora', 'novus']:
    update_data_price(shop)
