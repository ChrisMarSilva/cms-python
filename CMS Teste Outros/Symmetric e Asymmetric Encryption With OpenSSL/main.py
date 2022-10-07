import datetime as dt
import time

from loguru import logger


def teste_01():
    try:

        result = "ok"
        logger.info(f"{result=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()
    logger.info(f"Inicio")
    try:

        teste_01()

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == "__main__":
    main()

# python -m pip install --upgrade pip
# python -m pip install --upgrade xxxx

# https://www.youtube.com/watch?v=1jE_UOiFAVw

# cmd ou bash with admin
# choco install openssl

# openssl genrsa -aes-256-cbc -out myprivate.key
# abc@123
# C:\Users\chris\myprivate.key

# openssl rsa -in myprivate.key -pubout > mypublic.key
# abc@123

# openssl rsautl --encrypt -inkey mypublic.key -pubin -in message.txt -out message.enc
# openssl rsautl --decrypt -inkey myprivate.key -in message.enc > messageclear.txt
# abc@123

# python main.py
# C:/Python310/python.exe "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Asymmetric Encryption With OpenSSL/main.py"
