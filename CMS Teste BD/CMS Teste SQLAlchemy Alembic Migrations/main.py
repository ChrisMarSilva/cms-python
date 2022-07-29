from loguru import logger
import time
import datetime as dt


def teste_01_xxx():
    try:

        import sqlite3

        con = sqlite3.connect('banco.db')
        con.close()

        result = 'ok'
        logger.info(f'{result=}')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')


def main():
    start_time = time.perf_counter()
    logger.info(f'Inicio')
    try:

        teste_01_xxx()

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == '__main__':
    main()

# py -3 -m venv .venv
# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste BD\CMS Teste SQLAlchemy Alembic Migrations\.venv\Scripts"
# .venv\scripts\activate
# source activate 
# pip install --upgrade pip
# pip install loguru
# pip install alembic
# pip install db-sqlite3
# pip install sqlacodegen
# pip install sqlacodegen==3.0.0rc1  somente para testes
# pip install SQLAlchemy
# python.exe -m pip install --upgrade pip
# cd "C:\Users\chris\Desktop\CMS Python\CMS Teste BD\CMS Teste SQLAlchemy Alembic Migrations"

# alembic init migrations
# alembic revision -m "primeira"
# alembic upgrade head
# alembic downgrade base
# alembic history
# alembic history -i

# alembic revision --autogenerate -m "criando campo de senha na tabela pessoa"
# alembic upgrade +1
# alembic history
# alembic history -i

# alembic revision --autogenerate -m "tabela pessoa 2"
# alembic upgrade +1
# alembic revision --autogenerate -m "criando campo de idade na tabela pessoa 2"
# alembic upgrade +1
# alembic history
# alembic history -i

# alembic revision --autogenerate -m "alteracao no campo email para 100 chars na tabela pessoa"
# alembic upgrade head

# alembic downgrade -1 
# alembic upgrade +1 --sql
# alembic upgrade +1 --sql > xpto.sql
# alembic upgrade head
# alembic history
# alembic downgrade
# alembic downgrade c357afe11b1c:e6a1748a3b5a --sql
# alembic downgrade c357afe11b1c:e6a1748a3b5a --sql > xpto2.sql

# sqlacodegen sqlite:///banco.db
# sqlacodegen sqlite:///banco.db > models.py
# Core                === > sqlacodegen --generator tables sqlite:///banco.db > models.py
# ORM (Default)       === > sqlacodegen --generator declarative sqlite:///banco.db > models.py
# Dataclasses (1.4+)  === > sqlacodegen --generator dataclasses sqlite:///banco.db > models.py

# python -m pip install --upgrade pip
# python -m pip install --upgrade alembic
# python -m pip install --upgrade db-sqlite3
# python -m pip install --upgrade SQLAlchemy
# python main.py
