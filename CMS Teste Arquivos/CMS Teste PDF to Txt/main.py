from loguru import logger
import datetime as dt
import time
from PyPDF2 import PdfFileReader
import pdfplumber
from dotenv import load_dotenv


def teste_pdf_pypdf2(filaname: str) -> None:

    with open(file=filaname, mode='rb') as f:
        reader = PdfFileReader(stream=f)  # PdfFileReader(filaname, 'rb')
        num_pages = reader.numPages
        logger.info(f'{num_pages=}')
        docinfo = reader.getDocumentInfo()
        # metadict = dict(docinfo)
        # logger.info(f'{metadict=}')
        # logger.info(f'{docinfo=}')
        # logger.info(f'{docinfo.title=}')
        # logger.info(f'{docinfo.author=}')
        # logger.info(f'{docinfo.creator=}')
        # logger.info(f'{docinfo.producer=}')
        # logger.info(f'{docinfo.subject=}')
        # outlines = reader.getOutlines()
        # logger.info(f'{outlines=}')
        logger.info(f'PdfFileReader')
        for idx, page in enumerate(reader.pages):
            text = page.extractText()
            logger.info(f'idx={idx+1} {text=}')

        page = reader.getPage(1)
        text = page.extractText()
        logger.info(f'{text=}')

    logger.info(f'pdfplumber')
    with pdfplumber.open(filaname) as pdf:
        for idx in range(0, num_pages):
            page = pdf.pages[idx]
            text = page.extract_text()
            logger.info(f'reader page {idx+1}/{num_pages}')
            # logger.info(f'{page=} {text=}')


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        filaname = './2020.04.pdf'
        teste_pdf_pypdf2(filaname=filaname)

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
# python -m pip install --upgrade PyPDF2
# python -m pip install --upgrade pdfplumber
# cd c:/Users/chris/Desktop/CMS Python/xxxxxx
# .venv\scripts\activate
# python main.py
# python3 main.py  
# pypy3 main.py
