from loguru import logger
import datetime as dt
import time
import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
# from tqdm.auto import tqdm
from tqdm import tqdm
from dotenv import load_dotenv


def teste_download_img_airbnb():
    folder = 'imgs'
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    url = 'https://www.airbnb.co.uk/s/Bratislava--Slovakia/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&place_id=ChIJl2HKCjaJbEcRaEOI_YKbH2M&query=Bratislava%2C%20Slovakia&checkin=2020-11-01&checkout=2020-11-22&source=search_blocks_selector_p1_flow&search_type=search_query'
    r = requests.get(url=url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    for image in tqdm(images):
        name = image['alt']
        link = image['src']
        if not name:
            name = Path(link).name.replace('?', '-').replace('.', '-').replace('=', '-')
        with open(file=name.replace(' ', '-').replace('/', '') + '.jpg', mode='wb') as f:
            im = requests.get(url=link)
            f.write(im.content)
            # print('Writing: ', name)


def teste_download_img_statsroyale():
    url = 'https://statsroyale.com/cards'
    page = requests.get(url=url)
    souped = BeautifulSoup(markup=page.content, features='html.parser')
    imgs = souped.find_all('img')
    imgs = imgs[3:-1]
    for img in tqdm(imgs):
        img_link = img.attrs.get("src")
        img_name = Path(img_link).name
        image = requests.get(url=img_link)
        with open(file="./imgs/"+img_name, mode='wb') as f:
            f.write(image.content)
        # print('img_name: ', img_name, 'img_link: ', img_link)
        # break


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        # teste_download_img_airbnb()
        teste_download_img_statsroyale()

        # python main.py

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()


# py -3 -m venv .venv

# cd C:\Users\chris\Desktop\CMS Python\00.CMS Teste API e Web\CMS Teste Download
# .venv\scripts\activate

# python -m pip install --upgrade xxxx
# python main.py
