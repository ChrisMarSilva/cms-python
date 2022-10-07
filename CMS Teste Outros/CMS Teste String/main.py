import datetime as dt
import time

from loguru import logger


def teste_string_01():
    try:

        txt_completo = "A request to the Telegram API was unsuccessful. Error code: 403 Description: Forbidden: bot was blocked by the user"
        txt_completo = "https://www.rad.cvm.gov.br/ENET/frmExibirArquivoIPEExterno.aspx?ID=1013049 ): A request to the Telegram API was unsuccessful. Error code: 403 Description: Forbidden: bot was blocked by the user"
        # txt_completo = 'https://www.rad.cvm.gov.br/ENET/frmExibirArquivoIPEExterno.aspx?ID=1013049 )'
        logger.info(f"{txt_completo=}")

        txt_search = "Forbidden: bot was blocked by the user"
        logger.info(f"{txt_search=}")

        txt_result_find = txt_completo.find(txt_search)
        # if txt_completo.find(txt_search) < 0:
        logger.info(f"{txt_result_find=}")

        txt_result_in = txt_search.lower() in txt_completo.lower()
        logger.info(f"{txt_result_in=}")

        txt_result_contains = txt_completo.__contains__(txt_search)
        # txt_result_contains = txt_completo.contains(txt_search)
        logger.info(f"{txt_result_contains=}")

        txt_result_count = txt_completo.count(txt_search)
        logger.info(f"{txt_result_count=}")

        try:
            txt_completo.index(txt_search)
            logger.info(f"txt_result_index=True")
        except ValueError:
            logger.info(f"txt_result_index=False")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_string_02():
    try:

        command: str = "A"
        match command:
            case "A":
                logger.info(f"command=A")
            case "B":
                logger.info(f"command=B")
            case _:
                logger.info(f"command=OutraLetra")

        command: int = 5
        match command:
            case 1 | 2:
                logger.info(f"command=1|2")
            case 3 | 4 | 5:
                logger.info(f"command=3|4|5")
            case _:
                logger.info(f"command=OutroNumero")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()
    logger.info(f"Inicio")
    try:

        # teste_string_01()
        teste_string_02()

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == "__main__":
    # logger.add("file_{time}.log", level='DEBUG', rotation="500 MB", compression="zip", enqueue=True, format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
    main()


# python -m pip install --upgrade pip
# python -m pip install --upgrade xxxxxxx

# python main.py
