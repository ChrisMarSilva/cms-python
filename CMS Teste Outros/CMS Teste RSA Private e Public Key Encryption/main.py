import datetime as dt
import pathlib
import time

import rsa
from loguru import logger


def teste_01_rsa_newkeys():
    try:

        public_key, private_key = rsa.newkeys(nbits=1024)
        # nbits=1024, accurate=True, poolsize=1, exponent=65537
        # logger.info(f"{public_key=}")
        # logger.info(f"{private_key=}")

        file = pathlib.Path(__file__).parent.joinpath("public.pem")
        with open(file=file, mode="wb") as f:
            f.write(public_key.save_pkcs1("PEM"))

        file = pathlib.Path(__file__).parent.joinpath("private.pem")
        with open(file=file, mode="wb") as f:
            f.write(private_key.save_pkcs1("PEM"))

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_02_rsa_encrypt_decrypt():
    try:

        file = pathlib.Path(__file__).parent.joinpath("public.pem")
        with open(file=file, mode="rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        logger.info(f"{public_key=}")

        file = pathlib.Path(__file__).parent.joinpath("private.pem")
        with open(file=file, mode="rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        logger.info(f"{private_key=}")

        message = "Hello my password is neural_nine999"
        logger.info(f"{message=}")

        encrypted_message_write = rsa.encrypt(message.encode(), public_key)
        logger.info(f"{encrypted_message_write=}")

        file = pathlib.Path(__file__).parent.joinpath("encrypted.message")
        with open(file=file, mode="wb") as f:
            f.write(encrypted_message_write)

        file = pathlib.Path(__file__).parent.joinpath("encrypted.message")
        with open(file=file, mode="rb") as f:
            encrypted_message_read = f.read()
        logger.info(f"{encrypted_message_read=}")

        clear_message = rsa.decrypt(encrypted_message_read, private_key)
        logger.info(f"{clear_message.decode()=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_03_rsa_signature():
    try:

        file = pathlib.Path(__file__).parent.joinpath("public.pem")
        with open(file=file, mode="rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())
        logger.info(f"{public_key=}")

        file = pathlib.Path(__file__).parent.joinpath("private.pem")
        with open(file=file, mode="rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())
        logger.info(f"{private_key=}")

        message = "I have a new account on Twitter which is @madeupname9987615"
        logger.info(f"{message=}")

        signature_write = rsa.sign(message.encode(), private_key, "SHA-256")
        logger.info(f"{signature_write=}")

        file = pathlib.Path(__file__).parent.joinpath("signature")
        with open(file=file, mode="wb") as f:
            f.write(signature_write)

        file = pathlib.Path(__file__).parent.joinpath("signature")
        with open(file=file, mode="rb") as f:
            signature_read = f.read()
        logger.info(f"{signature_read=}")

        result = rsa.verify(message.encode(), signature_read, public_key)
        logger.info(f"{result=}")
        # result='SHA-256'

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_99_rsa():
    try:

        result = "ok"
        logger.info(f"{result=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()
    logger.info(f"Inicio")
    try:

        # teste_01_rsa_newkeys()
        # teste_02_rsa_encrypt_decrypt()
        teste_03_rsa_signature()
        # teste_99_rsa()

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == "__main__":
    main()

# python -m pip install --upgrade pip
# python -m pip install --upgrade rsa

# python main.py
# C:/Python310/python.exe "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste RSA Private e Public Key Encryption/main.py"
