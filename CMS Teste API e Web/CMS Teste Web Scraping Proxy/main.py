from email import parser
from loguru import logger
import datetime as dt
import time
import requests
from bs4 import BeautifulSoup
import statistics
from dotenv import load_dotenv


def normal_requests(url: str):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def proxy_requests(url: str):
    pauload = {'source': 'universal', 'url': url, 'geo_location': 'Germany'} #  'user_agent_type': 'desktop', 'domain': 'com', 'query': 'adidas', render':'html', 'parse':'true',
    # username, password = open('creds.txt', 'r').read().splitlines()
    username = 'username'
    password = 'password'
    response = requests.request(
        'POST', 
        'https://realtime.oxylabs.io/v1/queries', 
        auth=(username, password),
        json=pauload
    )
    response_html = response.json()['results'][0]['content']
    soup = BeautifulSoup(response_html, 'lxml')
    return soup


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # https://dashboard.oxylabs.io/en/

        BASE_URL = 'https://books.toscrape.com/'
        
        # --------------------------------------------------
        # --------------------------------------------------

        # url = BASE_URL + 'catalogue/category/books/philosophy_7/index.html'
        # soup = normal_requests(url=url)  # normal_requests # proxy_requests

        # # logger.info(f"{soup}")
        # # logger.info(f"{soup.find_all('p')}")
        # # logger.info(f"{soup.find_all('a')}")

        # prices_tags = soup.find_all('p', {'class': 'price_color'})
        # logger.info(f"{prices_tags}")

        # prices = [float(price.text[2:]) for price in prices_tags]
        # logger.info(f"{prices}")
        # logger.info(f"{round(statistics.mean(prices), 2)}")

        # --------------------------------------------------
        # --------------------------------------------------

        # cat = 'catalogue/category/books/fiction_10/'
        # url = BASE_URL + cat + "index.html"
        # prices = []
        # next_link = True

        # while next_link:
        #     logger.info(f"{url=}")
        #     soup = normal_requests(url=url)  # normal_requests # proxy_requests
        #     prices_tags = soup.find_all('p', {'class': 'price_color'})
        #     page_prices = [float(price.text[2:]) for price in prices_tags]
        #     prices += page_prices
        #     link = soup.body.find('a', text='next')
        #     if link:
        #         url = BASE_URL + cat + link['href']
        #     else:
        #         next_link = False

        # logger.info(f"{prices}")
        # logger.info(f"{round(statistics.mean(prices), 2)}")

        # --------------------------------------------------
        # --------------------------------------------------

        url = BASE_URL + 'catalogue/category/books/psychology_26/index.html'
        soup = normal_requests(url=url)  # normal_requests # proxy_requests

        books = soup.find_all('article', {'class': 'product_pod'})
        books_links = [book.find('a')['href'] for book in books]
        books_names = [book.find('h3').text for book in books]
        # logger.info(f"{books_links}")

        for name, link in zip(books_names, books_links): # for i in range(len(books_links)):
            # logger.info(f"{name} --- > {link}")
            url = BASE_URL + 'catalogue/category/books/psychology_26/' + link
            soup = normal_requests(url=url)  # normal_requests # proxy_requests
            new_name = soup.find('div', {'class': 'product_main'})
            new_name = new_name.find('h1')
            new_name = new_name.text.strip()
            availability = soup.find('p', {'class': 'instock availability'})
            availability = availability.text.strip()[10:12].strip()
            # logger.info(f"{name} --- > {new_name} --- > {availability}")
            logger.info(f"{name} {availability}")

        # --------------------------------------------------
        # --------------------------------------------------

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade lxml
# python -m pip install --upgrade html5lib
# python -m pip install --upgrade beautifulsoup4
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
