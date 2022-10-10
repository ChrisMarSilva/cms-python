import datetime as dt
import pathlib
import struct
import time

from loguru import logger


def teste_01():
    try:

        # byte_stream = struct.pack("iii", 10, 20, 30)
        # logger.info(f"{byte_stream=}")
        # logger.info(f"{struct.calcsize('i')=}")

        # byte_stream = struct.pack("hhh", 10, 20, 30)
        # logger.info(f"{byte_stream=}")
        # logger.info(f"{struct.calcsize('h')=}")

        # byte_stream = struct.pack("HHH", 9000, 20, 30)
        # logger.info(f"{byte_stream=}")
        # logger.info(f"{struct.calcsize('H')=}")

        # byte_stream = struct.pack("HHH", 10, 20, 30)
        # logger.info(f"{byte_stream=}")
        # a, b, c = struct.unpack("HHH", byte_stream)
        # logger.info(f"{a=}  {b=}  {c=}")

        # byte_stream = struct.pack("HH", 10, 20)
        # logger.info(f"{byte_stream=}")
        # a = struct.unpack("i", byte_stream)
        # logger.info(f"{a=}")

        company = b"NeuralNine"
        day, month, year = 1, 1, 2022
        awesome = True
        byte_stream = struct.pack("10s 3i ?", company, day, month, year, awesome)
        logger.info(f"{byte_stream=}")
        company, day, month, year, awesome = struct.unpack("10s 3i ?", byte_stream)
        logger.info(f"{company=} {day=} {month=} {year=} {awesome=}")

        # file = pathlib.Path(__file__).parent.joinpath("data")
        # with open(file=file, mode="wb") as f:
        #     f.write(byte_stream)
        # file = pathlib.Path(__file__).parent.joinpath("data")
        # with open(file=file, mode="rb") as f:
        #     data = f.read()
        # company, day, month, year, awesome = struct.unpack("10s 3i ?", data)
        # logger.info(f"{company=} {day=} {month=} {year=} {awesome=}")

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

# cd "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Packaging Data Using Structs"
# C:/Python310/python.exe "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste Packaging Data Using Structs/main.py"

# python main.py
