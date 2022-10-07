import datetime as dt
import pathlib
import time

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from loguru import logger


def teste_01_encrypt():
    try:

        # simple_key = get_random_bytes(32)
        # logger.info(f"{simple_key=}")

        salt = b"_}\r\xad\xa5\xfd>\xc8\x0e\x0f\xaf\xdfz\xec&u\xbf\xc1\xde\xdd\x99\x86\xa0X?\x89\xac\x1fiC\x18R"
        password = "mypassword"
        key = PBKDF2(password, salt, dkLen=32)

        file = pathlib.Path(__file__).parent.joinpath("key.bin")
        with open(file=file, mode="wb") as f:
            f.write(key)

        message = b"Hello Secret World!"
        cipher = AES.new(key, AES.MODE_CBC)
        ciphered_data = cipher.encrypt(pad(message, AES.block_size))

        file = pathlib.Path(__file__).parent.joinpath("encrypted.bin")
        with open(file=file, mode="wb") as f:
            f.write(cipher.iv)
            f.write(ciphered_data)

        file = pathlib.Path(__file__).parent.joinpath("encrypted.bin")
        with open(file=file, mode="rb") as f:
            iv = f.read(16)
            decrypt_data = f.read()

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        original = unpad(cipher.decrypt(decrypt_data), AES.block_size)
        logger.info(f"{original=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_02_decrypt():
    try:

        file = pathlib.Path(__file__).parent.joinpath("key.bin")
        with open(file=file, mode="rb") as f:
            key = f.read()

        file = pathlib.Path(__file__).parent.joinpath("encrypted.bin")
        with open(file=file, mode="rb") as f:
            iv = f.read(16)
            decrypt_data = f.read()

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        original = unpad(cipher.decrypt(decrypt_data), AES.block_size)
        logger.info(f"{original=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_03_decrypt():
    try:

        salt = b"_}\r\xad\xa5\xfd>\xc8\x0e\x0f\xaf\xdfz\xec&u\xbf\xc1\xde\xdd\x99\x86\xa0X?\x89\xac\x1fiC\x18R"
        password = "mypassword"
        key = PBKDF2(password, salt, dkLen=32)

        file = pathlib.Path(__file__).parent.joinpath("encrypted.bin")
        with open(file=file, mode="rb") as f:
            iv = f.read(16)
            decrypt_data = f.read()

        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        original = unpad(cipher.decrypt(decrypt_data), AES.block_size)
        logger.info(f"{original=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()
    logger.info(f"Inicio")
    try:

        # teste_01_encrypt()
        # teste_02_decrypt()
        teste_03_decrypt()

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == "__main__":
    main()

# python -m pip install --upgrade pip
# python -m pip install --upgrade pycryptodome

# python main.py
# C:/Python310/python.exe "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste xxxxxx/main.py"
