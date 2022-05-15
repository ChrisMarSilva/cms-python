from email import parser
from loguru import logger
import datetime as dt
import time
import requests
from bs4 import BeautifulSoup
import statistics
import random
import csv
import concurrent.futures
from tabulate import tabulate
from dotenv import load_dotenv


def get_proxies_01():
    url = 'https://free-proxy-list.net/'
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
    return proxies


def get_proxies_01_v2():
    url = 'https://free-proxy-list.net/'
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find('tbody') # table # tbody
    rows = table.findAll('tr')
    # headers = [row.text for row in rows[0]]
    # proxies = [':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text]) for row in rows]
    # proxies = []
    # for row in rows:
    #     proxies.append([data.text for data in row.findAll('td')])
    proxies = [[data.text for data in row.findAll('td')] for row in rows]
    proxies = [row[0] for row in proxies]
    #print(tabulate(proxies))
    # print(proxies)
    return proxies


def get_proxies_02():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    url = 'https://hidemy.name/en/proxy-list/'
    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    proxies = []
    for row in soup.find('tbody'):
        if row.find_all('td')[5].text == 'High': # no
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
    return proxies

def extract(proxy):
    #proxy = random.choice(proxylist)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    try:
        r = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=2)
        # print(r.json(), ' | Works')
        print(r.json(), r.status_code)
    except requests.ConnectionError as err:
        print(repr(err))
    return proxy


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        logger.info(f'') 

        proxy_list = get_proxies_01()
        # logger.info(f'{proxy_list=}') 
        logger.info(f'{len(proxy_list)=}') 
        #logger.info(f'{extract(proxy=proxy_list[0])}') 
        logger.info(f'') 

        proxy_list = get_proxies_01_v2()
        # logger.info(f'{proxy_list=}') 
        logger.info(f'{len(proxy_list)=}') 
        #logger.info(f'{extract(proxy=proxy_list[0])}') 
        logger.info(f'') 

        proxy_list = get_proxies_02()
        # logger.info(f'{proxy_list=}') 
        logger.info(f'{len(proxy_list)=}') 
        #logger.info(f'{extract(proxy=proxy_list[0])}') 
        logger.info(f'') 

        # proxylist = []
        # with open('proxylist.csv', 'r') as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         proxylist.append(row[0])
        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #         executor.map(extract, proxylist)

        # python main.py

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade tabulate
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
