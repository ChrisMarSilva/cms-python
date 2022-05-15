from loguru import logger
import speedtest
import csv
import time
import datetime as dt
import pytz
import telebot
import pandas as pd   
import numpy as np
import math
from dotenv import load_dotenv


def bytes_to_mb(size_bytes: float = 0.0) -> str:
    i = int(math.floor(math.log(size_bytes, 1024)))
    power = math.pow(1024, i)
    size = round(size_bytes / power, 2)
    return  f"{size} Mpbs"


def decimal_to_str(valor: float = 0.0) -> str:
    return "{0:,.2f}".format(valor).replace(",", "X").replace(".", ",").replace("X", ".")


def coletando_dados() -> dict:
    try:

        logger.info(f'Coletando dados')

        threads = 4  # 16  # 4
        servers = [49776]  # 49776 Penápolis  # 20777 Guaiçara 

        # logger.info('Criando Speedtest')
        s = speedtest.Speedtest()
        try:
            #logger.info(f'Escolhendo o Servidor {servers}')
            s.get_servers(servers)
        except Exception as e:
            #logger.error(f'Erro ao escolher o Servidor: "{str(e)}"')
            #logger.info('fechando o Servidor')
            s.get_closest_servers()
            #logger.info('Escolhendo o melhor Servidor')
            s.get_best_server()

        logger.info(f'Fazendo download')
        s.download(threads=threads)

        logger.info(f'Fazendo upload')
        s.upload(threads=threads)

        # s.results.share()
        results_dict = s.results.dict()

        download = round(results_dict["download"] / 1000000,2)
        upload = round(results_dict["upload"] / 1000000,2)
        ping = results_dict["ping"]

        #logger.info('Resultado')
        #logger.info(f'Sevidor - {results_dict["server"]["id"]} - {results_dict["server"]["name"]} - {results_dict["server"]["country"]}')
        logger.info(f'Download {decimal_to_str(valor=float(download))} Mbps - {bytes_to_mb(size_bytes=float(results_dict["download"]))}')
        logger.info(f'Upload {decimal_to_str(valor=float(upload))} Mbps - {bytes_to_mb(size_bytes=float(results_dict["upload"]))}')
        logger.info(f'Ping {decimal_to_str(valor=float(ping))} ms')
        # print(results_dict)

        return results_dict

    except Exception as e:
        logger.error(f'Falha Geral(coletando_dados): "{str(e)}"')


def salvando_arquivo(arquivo_relatorio: str, results_dict: dict) -> None:
    try:

        logger.info(f'Salvando Arquivo')

        # data_atual = datetime.now(tz=pytz.timezone("America/Sao_Paulo")).strftime('%d/%m/%Y')
        # hora_atual = datetime.now(tz=pytz.timezone("America/Sao_Paulo")).strftime('%H:%M')
        
        try:

            # logger.info(f'Criando Arquivo {arquivo_relatorio}')
            file = open(arquivo_relatorio, 'x', encoding='UTF8')
            file.close()
            
            # logger.info(f'Gravando no Arquivo {arquivo_relatorio} pela primeira vez')
            with open(arquivo_relatorio, 'w', newline='', encoding='UTF8') as f:
                w = csv.DictWriter(f, results_dict.keys(), delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                w.writeheader()
                w.writerow(results_dict)
            
        except IOError:
            # logger.info(f'Gravando no Arquivo {arquivo_relatorio}')
            with open(arquivo_relatorio, 'a', newline='', encoding='UTF8') as f:
                w = csv.DictWriter(f, results_dict.keys(), delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                w.writerow(results_dict)

    except Exception as e:
        logger.error(f'Falha Geral(salvando_arquivo): "{str(e)}"')


def send_msg_telegram(
        download_day: float = 0.0, upload_day: float = 0.0, ping_day: float = 0.0, 
        download_week: float = 0.0, upload_week: float = 0.0, ping_week: float = 0.0, 
        download_month: float = 0.0, upload_month: float = 0.0, ping_month: float = 0.0, 
        download_year: float = 0.0, upload_year: float = 0.0, ping_year: float = 0.0, 
        download_total: float = 0.0, upload_total: float = 0.0, ping_total: float = 0.0
    ) -> None:
    try:
        
        logger.info(f'Enviando Msg Telegram')

        chat_text = ''
        chat_text += f'<u><b>Alerta SpeedTest</b></u><br><br>'
        
        chat_text += f'<b>Resultado do Dia</b><br>'
        chat_text += f'<b>Download:</b> {decimal_to_str(valor=float(download_day))} Mbps<br>'
        chat_text += f'<b>Upload:</b>      {decimal_to_str(valor=float(upload_day))} Mbps<br>'
        chat_text += f'<b>Ping:</b>           {decimal_to_str(valor=float(ping_day))} ms<br><br>'
        
        chat_text += f'<b>Resultado da Semana</b><br>'
        chat_text += f'<b>Download:</b> {decimal_to_str(valor=float(download_week))} Mbps<br>'
        chat_text += f'<b>Upload:</b>      {decimal_to_str(valor=float(upload_week))} Mbps<br>'
        chat_text += f'<b>Ping:</b>           {decimal_to_str(valor=float(ping_week))} ms<br><br>'
        
        chat_text += f'<b>Resultado do Mês</b><br>'
        chat_text += f'<b>Download:</b> {decimal_to_str(valor=float(download_month))} Mbps<br>'
        chat_text += f'<b>Upload:</b>      {decimal_to_str(valor=float(upload_month))} Mbps<br>'
        chat_text += f'<b>Ping:</b>           {decimal_to_str(valor=float(ping_month))} ms<br><br>'
        
        chat_text += f'<b>Resultado do Ano</b><br>'
        chat_text += f'<b>Download:</b> {decimal_to_str(valor=float(download_year))} Mbps<br>'
        chat_text += f'<b>Upload:</b>      {decimal_to_str(valor=float(upload_year))} Mbps<br>'
        chat_text += f'<b>Ping:</b>           {decimal_to_str(valor=float(ping_year))} ms<br><br>'
        
        chat_text += f'<b>Resultado Geral</b><br>'
        chat_text += f'<b>Download:</b> {decimal_to_str(valor=float(download_total))} Mbps<br>'
        chat_text += f'<b>Upload:</b>      {decimal_to_str(valor=float(upload_total))} Mbps<br>'
        chat_text += f'<b>Ping:</b>           {decimal_to_str(valor=float(ping_total))} ms<br><br>'

        chat_text += f'<i><u>{dt.datetime.now(tz=pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")}</u></i><br>'
        chat_text = chat_text.replace('<br>', '\n')

        # token = '1238835452:AAGTATI9bldZfHtD2iMrvHiVztz9DguLHck'
        token = '5126234178:AAHJFigJPJWOBt3KcsPdpO5z1bTsPIR2AGE'
        bot = telebot.TeleBot(token=token)
        try:
            bot.send_message(chat_id='452513294', text=chat_text, parse_mode="HTML", disable_web_page_preview=False)
        finally:
            bot.stop_bot()

    except Exception as e:
        logger.error(f'Falha Geral(send_msg_telegram): "{str(e)}"')


def analisando_arquivo(arquivo_relatorio: str) -> None:
    try:
        
        logger.info(f'Analisando Arquivo')

        df = pd.read_csv(filepath_or_buffer=arquivo_relatorio, sep=';', thousands=None, decimal='.')
        df = df[['download', 'upload', 'ping', 'timestamp']]
        df['data'] = pd.to_datetime(df['timestamp'], errors='ignore').dt.strftime('%Y-%m-%d')  # .dt.strftime('%Y-%m-%d %X')
        df['data'] = pd.to_datetime(df['data'])
        df = df[['download', 'upload', 'ping', 'data']] 
        # df.head() # df.dtypes # df.info() # df.describe() # df['download'][0]

        tday = dt.date.today()
        tday = np.datetime64(tday)
        tweek = dt.date.today() + dt.timedelta(days=-7)
        tweek = np.datetime64(tweek)
        tmonth = dt.date.today().replace(day=1)
        tmonth = np.datetime64(tmonth)
        tyear = dt.date.today().replace(day=1, month=1)
        tyear = np.datetime64(tyear)

        logger.info(f'pegar a media da dia')
        df_day = df.loc[df['data'] == tday]
        download_day = float(round(float(df_day['download'].mean())/1000000, 2)) # median
        upload_day = float(round(float(df_day['upload'].mean())/1000000, 2))
        ping_day = float(round(float(df_day['ping'].mean()), 2))

        logger.info(f'pegar a media da semana')
        df_week = df.loc[(df['data'] >= tweek) & (df['data'] <= tday)]
        download_week = float(round(float(df_week['download'].mean())/1000000, 2)) # median
        upload_week = float(round(float(df_week['upload'].mean())/1000000, 2))
        ping_week = float(round(float(df_week['ping'].mean()), 2))

        logger.info(f'pegar a media do mes')
        df_moth = df.loc[(df['data'] >= tmonth) & (df['data'] <= tday)]
        download_month = float(round(float(df_moth['download'].mean())/1000000, 2)) # median
        upload_month = float(round(float(df_moth['upload'].mean())/1000000, 2))
        ping_month = float(round(float(df_moth['ping'].mean()), 2))

        logger.info(f'pegar a media do ano')
        df_year =df.loc[(df['data'] >= tyear) & (df['data'] <= tday)]
        download_year = float(round(float(df_year['download'].mean())/1000000, 2)) # median
        upload_year = float(round(float(df_year['upload'].mean())/1000000, 2))
        ping_year = float(round(float(df_year['ping'].mean()), 2))

        logger.info(f'pegar a media do geral')
        download_total = float(round(float(df['download'].mean())/1000000, 2)) # median
        upload_total = float(round(float(df['upload'].mean())/1000000, 2))
        ping_total = float(round(float(df['ping'].mean()), 2))

        logger.info(f'dia \t download: {download_day} Mbps \t upload: {upload_day} Mbps \t ping: {ping_day} ms')
        logger.info(f'semana \t download: {download_week} Mbps \t upload: {upload_week} Mbps \t ping: {ping_week} ms')
        logger.info(f'mes \t download: {download_month} Mbps \t upload: {upload_month} Mbps \t ping: {ping_month} ms')
        logger.info(f'ano \t download: {download_year} Mbps \t upload: {upload_year} Mbps \t ping: {ping_year} ms')
        logger.info(f'geral \t download: {download_total} Mbps \t upload: {upload_total} Mbps \t ping: {ping_total} ms')       

        send_msg_telegram(
            download_day=download_day, upload_day=upload_day, ping_day=ping_day, 
            download_week=download_week, upload_week=upload_week, ping_week=ping_week, 
            download_month=download_month, upload_month=upload_month, ping_month=ping_month, 
            download_year=download_year, upload_year=upload_year, ping_year=ping_year, 
            download_total=download_total, upload_total=upload_total, ping_total=ping_total
        )

        logger.info(f'Anaisando Arquivo')

    except Exception as e:
        logger.error(f'Falha Geral(analisando_arquivo): "{str(e)}"')


def main():
    try:

        logger.info(f'Inicio') 
        start_time = time.time()

        hr_atual = dt.datetime.now(tz=pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S')
        logger.info(f'hr_atual: {hr_atual}') 

        results_dict = coletando_dados()
        salvando_arquivo(arquivo_relatorio='speedtest.csv', results_dict=results_dict)

        if hr_atual >= "21:00:00" and hr_atual <= "21:10:00": 
            analisando_arquivo(arquivo_relatorio='speedtest.csv')

        logger.info(f'Fim - {time.time()-start_time:.2f} seconds') 

    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


if __name__ == '__main__':
    main()
    # while True:
    #     main()
    #     time.sleep(1)


# py -3 -m venv .venv

# cd c:/Users/chris/Desktop/CMS Python/CMS Teste Internet Speed Test
# .venv\scripts\activate

# python -m ensurepip --upgrade
# py -m pip install --upgrade pip
# python -m pip install --upgrade pip
# python -m pip install --upgrade speedtest-cli
# python -m pip install --upgrade pandas
# python -m pip install --upgrade loguru
# python -m pip install --upgrade pyTelegramBotAPI
# python main.py

# C:\pypy39\pypy.exe -m ensurepip
# pypy -m ensurepip
# pypy -m pip install --upgrade pip
# pypy3 -m pip install --upgrade speedtest-cli
# pypy3 -m pip install --upgrade pandas
# pypy3 main.py

# python3 -m pip install --upgrade speedtest-cli
# python3 -m pip install --upgrade pandas
# python3 -m pip install --upgrade loguru
# python3 -m pip install --upgrade pytz
# python3 main.py 
