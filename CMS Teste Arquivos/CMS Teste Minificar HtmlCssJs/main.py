from loguru import logger
import time
import datetime as dt
import pathlib
import requests
import minify_html
import htmlmin
from enum import Enum, unique, auto


@unique
class Minificacao(Enum):
    REQUESTS = auto()
    HTMLMIN = auto()
    MINIFYHTML = auto()

@unique
class Extensao(Enum):
    HTML = 'html'
    JS = 'js'
    CSS = 'css'


def limpar_pasta(path: pathlib.Path):
    try:

        logger.info(f'Removendo Arquivos na Pasta Destino')

        files = [x for x in path.iterdir() if x.is_file()] 
        for idx, file in enumerate(files):
            logger.info(f'  - {idx+1}/{len(files)} - {file.name}')
            file.unlink() 

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def minificar_arquivo(path_origem: pathlib.Path, path_destino: pathlib.Path, extensao: Extensao, tipo: Minificacao):
    try:

        logger.info(f'{extensao.value.upper()}')

        files = list(path_origem.glob(f'**/*.{extensao.value.lower()}'))

        for idx, file in enumerate(files):
            logger.info(f'  - {idx+1}/{len(files)} - {file.name}') # html_file.rstrip('.html')+'.min.html'

            if tipo == Minificacao.REQUESTS:
                with open(file=file, mode='rb') as reader, open(file=path_destino.joinpath(file.name), mode='w', encoding='utf-8') as writer:  # 'rb' # 'wb' # , encoding='utf-8'
                    # if extensao == Extensao.HTML: url = 'https://www.toptal.com/developers/html-minifier/raw'
                    # elif extensao == Extensao.JS: url = 'https://www.toptal.com/developers/javascript-minifier/raw'
                    # elif extensao == Extensao.CSS': url = 'https://www.toptal.com/developers/cssminifier/raw'
                    # data = {'input': reader.read()}
                    if extensao == Extensao.HTML: url = "https://api.dotmaui.com/client/1.1/htmlmin/"
                    elif extensao == Extensao.JS: url = "https://api.dotmaui.com/client/1.0/jsmin/"
                    elif extensao == Extensao.CSS: url = "https://api.dotmaui.com/client/1.2/cssmin/"
                    YOUR_API_KEY = 'fAs37aLPRmUhsZsXL5Z0PqnY73sE42D8OoWq2rYPSUpgL'
                    if extensao == Extensao.HTML: data = {'apikey': YOUR_API_KEY, 'html': reader.read(), 'collapsewhitespace': 'all'}
                    elif extensao == Extensao.JS: data = {'apikey': YOUR_API_KEY, 'js': reader.read()}
                    elif extensao == Extensao.CSS: data = {'apikey': YOUR_API_KEY, 'css': reader.read()}
                    response = requests.post(url=url, data=data)
                    conteudo = response.text  # text  # content
                    writer.write(conteudo)

            elif tipo == Minificacao.HTMLMIN:
                with open(file=file, mode='r' , encoding='utf-8') as reader, open(file=path_destino.joinpath(file.name), mode='w', encoding='utf-8') as writer:
                    # conteudo = htmlmin.minify(reader.read(), remove_comments=True, remove_empty_space=True)
                    conteudo = htmlmin.minify(reader.read(), remove_comments=True, remove_empty_space=True, remove_all_empty_space=True, reduce_empty_attributes=True, remove_optional_attribute_quotes=False)
                    writer.write(conteudo)

            elif tipo == Minificacao.MINIFYHTML:
                with open(file=file, mode='r' , encoding='utf-8') as reader, open(file=path_destino.joinpath(file.name), mode='w', encoding='utf-8') as writer:
                    # if extensao == Extensao.HTML: conteudo = minify_html.minify(reader.read(), keep_comments=False, minify_js=True, minify_css=True, remove_processing_instructions=True)
                    # elif extensao == Extensao.JS: conteudo = minify_html.minify(reader.read(), keep_comments=False, minify_js=True)
                    # elif extensao == Extensao.CSS: conteudo = minify_html.minify(reader.read(), keep_comments=False, minify_css=True)
                    conteudo = minify_html.minify(reader.read())
                    writer.write(conteudo)

        # python main.py

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time() # time.monotonic()
    logger.info(f'Inicio') 
    try:

        # Teste local

        # path_origem_html = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python\CMS Teste Arquivos\CMS Teste Minificar HtmlCssJs\01_origem_html")  # pathlib.Path.cwd().joinpath('01_origem_html')
        # path_origem_js = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python\CMS Teste Arquivos\CMS Teste Minificar HtmlCssJs\02_origem_js")  # pathlib.Path.cwd().joinpath('02_origem_js')
        # path_origem_css = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python\CMS Teste Arquivos\CMS Teste Minificar HtmlCssJs\03_origem_css")  # pathlib.Path.cwd().joinpath('03_origem_css')

        # path_destino_html = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python\CMS Teste Arquivos\CMS Teste Minificar HtmlCssJs\04_destino_html")  # pathlib.Path.cwd().joinpath('04_destino_html')
        # path_destino_js = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python\CMS Teste Arquivos\CMS Teste Minificar HtmlCssJs\05_destino_js")  # pathlib.Path.cwd().joinpath('05_destino_js')
        # path_destino_css = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python\CMS Teste Arquivos\CMS Teste Minificar HtmlCssJs\06_destino_css")  # pathlib.Path.cwd().joinpath('06_destino_css')

        # # Teste TamoNaBolsa

        # path_origem_html = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\templates") 
        # path_origem_js = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\static\pages\js")
        # path_origem_css = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\static\pages\css")

        # path_destino_html = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\templatesmin")
        # path_destino_js = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\static\pages\jsmin")
        # path_destino_css = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\static\pages\cssmin")

        # # Teste TamoNaBolsa

        path_origem_html = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\templatesorig") 
        path_origem_js = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\static\pages\jsorig")
        path_origem_css = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\static\pages\cssorig")

        path_destino_html = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\templates")
        path_destino_js = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\static\pages\js")
        path_destino_css = pathlib.Path(r"C:\Users\chris\Desktop\CMS Python TnB Site\app\static\pages\css")

        # limpar_pasta(path=path_destino_html)
        # minificar_arquivo(path_origem=path_origem_html, path_destino=path_destino_html, extensao=Extensao.HTML, tipo=Minificacao.HTMLMIN) # REQUESTS # HTMLMIN  # MINIFYHTML

        # limpar_pasta(path=path_destino_js)
        # minificar_arquivo(path_origem=path_origem_js, path_destino=path_destino_js, extensao=Extensao.JS, tipo=Minificacao.HTMLMIN)

        # limpar_pasta(path=path_destino_css)
        # minificar_arquivo(path_origem=path_origem_css, path_destino=path_destino_css, extensao=Extensao.CSS, tipo=Minificacao.MINIFYHTML)

        # python main.py

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()  # time.monotonic()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == '__main__':
    main()

# python -m pip install --upgrade minify-html
# python -m pip install --upgrade htmlmin
# python main.py
