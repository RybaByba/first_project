from bs4 import BeautifulSoup
import requests
from datetime import datetime


headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
cookie = {"OCSESSID": "e87dc143b397f8933a11ad421f"}
base_url = "https://shop.fora.ua/index.php?route=product/search&search={product_id}"
last_date = datetime.now().date()

products = {
    "pork": {
        "product_id": "112_1292_32694",
        "unit": "weight"
    },
    "potatoes": {
        "product_id": "112_1326_531296",
        "unit": "weight"
    },
    "beets": {
        "product_id": "112_1326_32570",
        "unit": "weight"
    },
    "carrots": {
        "product_id": "112_1326_34650",
        "unit": "weight"
    },
    "cabbage": {
        "product_id": "112_1326_32572",
        "unit": "weight"
    },
    "onions": {
        "product_id": "112_1326_32573",
        "unit": "weight"
    },
    "sour_cream": {
        "product_id": "112_1340_540796",
        "unit": "count"
    },
    "sunflower_oil": {
        "product_id": "112_1344_757520",
        "unit": "count"
    },
    "tomato_paste": {
        "product_id": "112_1372_318797",
        "unit": "count"
    }
}


def get_products(products):

    for item in products:
        product = products[item]
        url = base_url.format(product_id=product['product_id'])
        r = requests.get(url, headers=headers, cookies=cookie)
        soup = BeautifulSoup(r.text, 'html.parser')

        try:
            price = soup.find(class_='price').text.lstrip('\n').split()[0]
            product_name = soup.find('p', class_='description').text.split('(')[0]

        except AttributeError:
            print(f"ATTR ERRR  {item}")

            products[item].update(
                {
                    "shop_name": 'fora',
                    "product_name": 'None',
                    "price": '',
                    "href": 'None',
                    "date": datetime.now().date()
                }
            )

            continue

        except Exception as e:
            print(f" Item: [ {e} ] pass error!!")

        products[item].update(
            {
                "shop_name": 'fora',
                "product_name": product_name,
                "price": price,
                "href": url,
                "date": datetime.now().date()
                }
            )
#
#
    return products


def get_data():
    return get_products(products)

