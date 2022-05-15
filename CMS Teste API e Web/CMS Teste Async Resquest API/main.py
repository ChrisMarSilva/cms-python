import requests
import aiohttp
import asyncio
import os
import platform
import time
from dotenv import load_dotenv


# https://www.alphavantage.co/documentation/
load_dotenv() # To work with the .env file
api_key = os.getenv('ALPHAVANTAGE_API_KEY')
url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'  # https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo'
symbols = ['AAPL', 'GOOG', 'TSLA', 'MSFT']
# nasdaq 100 - 102 stocks
# symbols = ['FOXA','ATVI','ADBE','AKAM','ALXN','ALTR','AMZN','AAL','AMGN','ADI','AAPL','AMAT','ADSK','ADP','AVGO','BIDU','BBBY','BIIB','BMRN','BRCM','CHRW','CA','CTRX','CELG','CERN','CHTR','CHKP','CSCO','CTXS','CTSH','CMCSA','COST','DISCA','DISH','DLTR','EBAY','EA','EQIX','EXPD','ESRX','FB','FAST','FISV','GRMN','GILD','GOOG','GOOGL','GMCR','HSIC','ILMN','INTC','INTU','ISRG','KLAC','KHC','LRCX','LBTYA','LINTA','LMCK','LMCA','LLTC','MAR','MAT','MU','MSFT','MDLZ','MNST','MYL','NTAP','NFLX','NVDA','NXPI','ORLY','PCAR','PAYX','PCLN','QCOM','REGN','ROST','SNDK','SBAC','STX','SIAL','SIRI','SPLS','SBUX','SRCL','SYMC','TSLA','TXN','TSCO','TRIP','VRSK','VRTX','VIAB','VIP','VOD','WDC','WFM','WYNN','XLNX','YHOO']
results1 = []
results2 = []
results3 = []


def teste_01_sync_request():
    start = time.time()
    for symbol in symbols:
        # print('#1 - Working on symbol {}'.format(symbol))
        try:
            response = requests.get(url=url.format(symbol, api_key))
            results1.append(response.json())
        except:
            pass
    # print('#1 - len:', len(results1))
    print("Teste #1 - Levou {} segundos para fazer {} chamadas de API".format(time.time() - start, len(symbols)))


async def teste_02_async_run():
    start = time.time()
    async with aiohttp.ClientSession() as session:
        for symbol in symbols:
            # print('#2 - Working on symbol {}'.format(symbol))
            response = await asyncio.create_task(session.get(url.format(symbol, api_key), ssl=False))
            results2.append(await response.json())
    # print('#2 - len:', len(results2))
    print("Teste #2 - Levou {} segundos para fazer {} chamadas de API".format(time.time() - start, len(symbols)))



async def teste_03_tasks_run():
    def get_tasks(session):
        tasks = []
        for symbol in symbols:
            tasks.append(asyncio.create_task(session.get(url.format(symbol, api_key), ssl=False)))
        return tasks
    start = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = get_tasks(session=session)  # tasks = [asyncio.create_task(session.get(url.format(symbol, api_key), ssl=False)) for symbol in symbols]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            results3.append(await response.json())
    # print('#3 - len:', len(results3))
    print("Teste #3 - Levou {} segundos para fazer {} chamadas de API".format(time.time() - start, len(symbols)))



async def teste_04_tasks_prints():
    
    async def other_function():
        print('1')
        await asyncio.sleep(delay=2)
        print('2')
        return 10

    print('Ini')

    # tasks = []
    # tasks.append(asyncio.create_task(other_function()))
    # tasks.append(asyncio.create_task(other_function()))
    tasks = asyncio.create_task(other_function())

    print('A')
    await asyncio.sleep(delay=1)
    print('B')
    
    # await asyncio.gather(*tasks)
    return_value = await tasks
    print(f'Return value was {return_value}')

    print('Fim')


def main():

    # https://books.toscrape.com/catalogue/page-1.html
    # https://books.toscrape.com/catalogue/page-50.html

    # https://www.scrapethissite.com/pages/forms/?page_num=1
    # https://www.scrapethissite.com/pages/forms/?page_num=24

    if platform.system() == 'Windows':
        asyncio.set_event_loop(asyncio.ProactorEventLoop())
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # teste_01_sync_request()            # 28.13797378540039   segundos
    # asyncio.run(teste_02_async_run())  # 16.63886523246765   segundos
    # asyncio.run(teste_03_tasks_run())  #  2.2582812309265137 segundos
    asyncio.run(teste_04_tasks_prints()) 
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(teste_02_async_run())
    # loop.close()


if __name__ == '__main__':
    main()


#  C:/Python310/python.exe "c:/Users/chris/Desktop/CMS Python/CMS Teste Async Resquest API/main.py"

# py -3 -m venv .venv

# python -m pip install aiohttp
# python -m pip install requests
# python -m pip install python-dotenv

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste Async Resquest API
# .venv\scripts\activate
# python main.py
