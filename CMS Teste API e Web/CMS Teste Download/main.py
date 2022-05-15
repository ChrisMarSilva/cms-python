from loguru import logger
import time
from dotenv import load_dotenv


def teste01():
    try:

        from pathlib import Path
        from tqdm.auto import tqdm
        import requests
        
        urls = open('files.txt').read().splitlines()
        output_dir = Path('downloaded')
        output_dir.mkdir(parents=True, exist_ok=True)

        for url in tqdm(urls):
            print(url)
            filename = Path(url).name
            response = requests.get(url)
            output_dir.joinpath(filename).write_bytes(response.content)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste02():
    try:

        import urllib.request
        from os import path

        urls = open('files-alt.txt').read().splitlines()
        for url in urls:
            filename = path.basename(url)
            urllib.request.urlretrieve(url, filename)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste03():
    try:

        import requests
        from pathlib import Path

        response = requests.get("http://www.vineland.org/sites/default/files/10_06_21%20Combined%20Meeting%20Minutes%20%281%29.pdf")
        Path("output.pdf").write_bytes(response.content)
        
        response = requests.get("http://www.vineland.org/sites/default/files/10_06_21 Combined Meeting Minutes (1).pdf")
        Path("output2.pdf").write_bytes(response.content)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste04():
    try:

        from os import path
        import requests
        from pathlib import Path

        # Method one: os.path

        url = "http://www.vineland.org/sites/default/files/10_06_21 Combined Meeting Minutes (1).pdf"
        filename = path.basename(url)
        print("Saving to", filename)

        response = requests.get(url)
        Path(filename).write_bytes(response.content)

        # Method two: pathlib

        # Hey Path, pull out the filename we want to save it as
        filename = Path(url).name
        print("I'm going to save to", filename)

        # Hey requests,go get the file
        url = "http://www.vineland.org/sites/default/files/10_06_21 Combined Meeting Minutes (1).pdf"
        response = requests.get(url)

        # Hey both of you, work together to save it to the filename
        Path(filename).write_bytes(response.content)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste05():
    try:

        import requests
        from pathlib import Path

        urls = open("files.txt").read().splitlines()

        for url in urls:
            print("------")
            print(url)
            filename = Path(url).name
            print("I want to save this as", filename)
            response = requests.get(url)
            Path(filename).write_bytes(response.content)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste06():
    try:

        from tqdm.auto import tqdm
        import requests
        from pathlib import Path
        
        urls = open("files.txt").read().splitlines()

        for url in tqdm(urls):
            filename = Path(url).name
            response = requests.get(url)
            Path(filename).write_bytes(response.content)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste07():
    try:

        from tqdm.auto import tqdm
        import requests
        from pathlib import Path
        
        urls = open("files.txt").read().splitlines()

        download_dir = Path('downloads/pdfs/secret-pdfs')
        download_dir.mkdir(parents=True, exist_ok=True)

        for url in tqdm(urls):
            filename = Path(url).name
            response = requests.get(url)
            download_dir.joinpath(filename).write_bytes(response.content)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste08():
    try:

        import pandas as pd
        import requests
        from pathlib import Path
        from tqdm.auto import tqdm
        tqdm.pandas()

        df = pd.read_csv("filelist.csv", sep=';')
        # print(df.head())

        download_dir = Path('downloads/pdfs/secret-pdfs-from-pandas')
        download_dir.mkdir(parents=True, exist_ok=True)

        def download_file(row):
            url = row['url']
            print("Downloading", url)
            filename = f"{row['date']}-minutes.pdf"
            response = requests.get(url)
            download_dir.joinpath(filename).write_bytes(response.content)
            
        # df.apply(download_file, axis=1)
        df.progress_apply(download_file, axis=1)

        # Saving a nice CSV file as a rough-and-tumble list of filenames
        # df.to_csv("filelist.txt", index=False, columns=['url'], header=False)

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste09():
    try:

        pass

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.time()

        # teste01() # The perfect way
        # teste02() # The fewer-lines-of-code-but-less-flexible way
        # teste03() # Downloading files one at a time
        # teste04() # Automatic filenames
        # teste05() # From a plain list of files
        # teste06() # Adding a progress bar
        # teste07() # Saving into a separate folder
        # teste08() # From inside of a CSV/pandas dataframe
        teste09() # 

        logger.info(f'Fim - {time.time()-start_time:.2f} seconds') 

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


if __name__ == '__main__':
    main()


# py -3 -m venv .venv

# cd C:\Users\chris\Desktop\CMS Python\00.CMS Teste API e Web\CMS Teste Download
# .venv\scripts\activate

# python -m pip install --upgrade tqdm
# python -m pip install --upgrade wget
# python main.py
