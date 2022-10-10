import datetime as dt
import time
from datetime import datetime
from venv import create

import requests
from bs4 import BeautifulSoup
from loguru import logger
from pony import orm
from this import d

db = orm.Database()
db.bind(provider="sqlite", filename="products.db", create_db=True)
# db.bind(provider='sqlite', filename=':sharedmemory:')
# db.bind(provider='postgres', user='', password='', host='', database='')
# db.bind(provider='mysql', host='', user='', passwd='', db='')
# db.bind(provider='oracle', user='', password='', dsn='')


class Product(db.Entity):
    name = orm.Required(str)
    price = orm.Required(float)
    created_at = orm.Required(datetime)


db.generate_mapping(create_tables=True)
orm.set_sql_debug(True)


def gears4(session):
    url = "https://www.gear4music.com/Recording-and-Computers/Shure-SM7B-Dynamic-Studio-Microphone/G6X"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "gear4music",
        float(soup.select_one("span.info-row-price span.c-val").text.replace("£", "")),
    )
    return data


def amazon(session):
    url = "https://www.amazon.co.uk/Shure-SM7B-Microphone/dp/B0002E4Z8M"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "amazon",
        float(
            soup.select_one("div.a-box-group span.a-offscreen").text.replace("£", "")
        ),
    )
    return data


def thomann(session):
    url = "https://www.thomann.de/gb/shure_sm_7b_studiomikro.htm"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "thomann",
        float(soup.select_one("div.price-wrapper div.price").text.replace("£", "")),
        # /html/body/div[4]/div/div[2]/div/div/div[1]/div/div[3]/div/div[1]/div[2]/div[1]/div/text()
    )
    return data


def main():
    start_time = time.perf_counter()
    logger.info(f"Inicio")
    try:

        session = requests.Session()
        # session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'})
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
            }
        )

        logger.info(f" --> Scraping")
        data = [
            amazon(session),
            gears4(session),
            thomann(session),
        ]

        logger.info(f" --> Insert")
        with orm.db_session:
            for item in data:
                Product(name=item[0], price=item[1], created_at=datetime.now())

        logger.info(f" --> Select")
        with orm.db_session:
            products = orm.select(p for p in Product).order_by(Product.name)
            for p in products:
                logger.info(
                    f" --> name: {p.name} - price: {p.price} - create_date: {p.created_at}"
                )

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == "__main__":
    main()

# python -m pip install --upgrade pip
# python -m pip install --upgrade pony

# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste API e Web\CMS Teste Price Monitoring"

# python main.py
