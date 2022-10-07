import datetime as dt
import string
import time

from loguru import logger


def teste_01():
    try:

        plain_text = "hello world"
        shift = 7  # 7  # 1  # 5  # 25  # 80
        shift %= 26

        alphabet = string.ascii_lowercase
        shifted = alphabet[shift:] + alphabet[:shift]
        table = str.maketrans(alphabet, shifted)

        encrypted = plain_text.translate(table)
        logger.info(f"{encrypted=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def teste_02_caesar():
    try:

        def caesar(text, shift, alphabets):
            def shift_alphabet(alphabet):
                return alphabet[shift:] + alphabet[:shift]

            shifted_alphabets = tuple(map(shift_alphabet, alphabets))
            final_alphabet = "".join(alphabets)
            final_shifted_alphabet = "".join(shifted_alphabets)
            table = str.maketrans(final_alphabet, final_shifted_alphabet)

            return text.translate(table)

        plain_text = "This is a new test. Hello World!"
        shift = 7
        alphabets = [string.ascii_lowercase, string.ascii_uppercase, string.punctuation]

        encrypted = caesar(text=plain_text, shift=shift, alphabets=alphabets)
        logger.info(f"{encrypted=}")

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()
    logger.info(f"Inicio")
    try:

        # teste_01()
        teste_02_caesar()

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == "__main__":
    main()

# python -m pip install --upgrade pip
# python -m pip install --upgrade xxxx

# python main.py
# C:/Python310/python.exe "c:/Users/chris/Desktop/CMS Python/CMS Teste Outros/CMS Teste xxxxxx/main.py"
