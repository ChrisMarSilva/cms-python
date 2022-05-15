from urllib import response
from loguru import logger
import datetime as dt
import time
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from dotenv import load_dotenv


def teste_01_imdb_to_csv():
    try:

        headers = {"Accept-Language": "en-US,en;q=0.5"}
        movie_name, year, time, rating, metascore, votes, gross, description = [], [], [], [], [], [], [], []
        pages = np.arange(1, 1000, 100)

        tot_pages = len(pages)
        for idx_page, page in enumerate(pages):
            logger.info(f'Page {idx_page+1}/{tot_pages}')
            url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(page)+"&ref_=adv_nxt"
            resp = requests.get(url=url)
            soup = BeautifulSoup(markup=resp.text,  features='html.parser')
            movie_data = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})
            sleep(randint(2, 8))
            tot_store = len(movie_data)
            for idx_store, store in enumerate(movie_data):
                name = store.h3.a.text
                # logger.info(f'Page {idx_page+1}/{tot_pages} - Store {idx_store+1}/{tot_store} - {name=}')
                movie_name.append(name)
                year.append(store.h3.find('span', class_ = "lister-item-year text-muted unbold").text)
                time.append(store.p.find("span", class_ = 'runtime').text)
                rating.append(store.find('div', class_ = "inline-block ratings-imdb-rating").text.replace('\n', ''))
                metascore.append(store.find('span', class_ = "metascore").text if store.find('span', class_ = "metascore") else "****")
                value = store.find_all('span', attrs = {'name': "nv"})
                votes.append(value[0].text)
                gross.append(value[1].text if len(value)>1 else '%^%^%^')
                describe = store.find_all('p', class_ = 'text-muted')
                description_ = describe[1].text.replace('\n', '') if len(describe) >1 else '*****'
                description.append(description_)

        movie_list = pd.DataFrame({ "Movie Name": movie_name, "Year of Release" : year, "Watch Time": time,"Movie Rating": rating, "Meatscore of movie": metascore, "Votes" : votes, "Gross": gross, "Description": description })
        logger.info(f'{movie_list.head(5)}')

        movie_list.to_excel("./Top 1000 IMDb movies.xlsx") # #saving the data in excel format
        movie_list.to_csv("./Top 1000 IMDb movies.csv") # #If you want to save the data in csv format

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        teste_01_imdb_to_csv()

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# python -m pip install --upgrade xxxxxxx
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
