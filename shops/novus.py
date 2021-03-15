from bs4 import BeautifulSoup
import requests
from datetime import datetime


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
base_url = "https://novus.zakaz.ua/ru/products/{product_id}/{path}"

products_novus = {
    "pork": {
        "product_id": "novus02856448000000",
        "path": "oshiiok-maistri-smaku",
        "unit": "weight"
    },
    "potatoes": {
        "product_id": "novus02850128000000",
        "path": "ovochi-kartoplia",
        "unit": "weight"
    },
    "beets": {
        "product_id": "novus02850048000000",
        "path": "ovochi-buriak",
        "unit": "weight"
    },
    "carrots": {
        "product_id": "novus02850535000000",
        "path": "ovochi-morkva",
        "unit": "weight"
    },
    "cabbage": {
        "product_id": "novus02850121000000",
        "path": "ovochi-kapusta",
        "unit": "weight"
    },
    "onions": {
        "product_id": "novus02850972000000",
        "path": "ovochi-tsibulia",
        "unit": "weight"
     },
    "sour_cream": {
        "product_id": "04823005203803",
        "path": "smetana-iagotin-350g",
        "unit": "count"
    },
    "sunflower_oil": {
        "product_id": "04820078575721",
        "path": "oliia-shchedrii-dar-870ml",
        "unit": "count"
    },
    "tomato_paste": {
        "product_id": "04820015942517",
        "path": "sous-priprava-runa-485g",
        "unit": "count"
    }
}


def get_novus_products(products_novus):

    for item in products_novus:
        product = products_novus[item]
        url = base_url.format(**product)
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        product_name = soup.find('h1', class_='big-product-card__title').text

        try:
            price = soup.find(class_='Price__value_title').text

            if product["unit"] == "weight":
                price = float(price) / 10

        except AttributeError:
            print(f"ATTR ERRR  {item}")

            products_novus[item].update(
                {
                    "shop_name": 'fora',
                    "product_name": 'None',
                    "price": '',
                    "href": 'None',
                    "date": datetime.now().date()
                }
            )

            continue

        products_novus[item].update(
            {
                "shop_name": "novus",
                "product_name": product_name,
                "price": price,
                "href": url,
                "date": datetime.now().date()
            }
        )

    return products_novus


def get_data():
    return get_novus_products(products_novus)


