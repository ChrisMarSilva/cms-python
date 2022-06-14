from loguru import logger
import time
import datetime as dt
from infra.repository.atores_repository import AtoresRepository
from infra.repository.filmes_repository import FilmesRepository


def main() -> None:
    start_time = time.perf_counter()
    logger.info(f'Inicio') 
    try:

        # https://github.com/programadorLhama/sqlalchemy

        atoresRepo = AtoresRepository()
        # result = atoresRepo.select_all()
        result = atoresRepo.select_with_filmes()
        logger.warning(f'Atores')
        logger.warning(f'{result}')
        logger.warning(f'{result[0].nome} - {result[0].genero} - {result[0].titulo}')

        filmesRepo = FilmesRepository()
        # filmesRepo.insert(titulo="Alguma Coisa", genero="Drama", ano=2010)
        # filmesRepo.insert(titulo="Alguma Coisa", ano=2020)
        # filmesRepo.delete(titulo="Alguma Coisa")
        result = filmesRepo.select_all()
        # result = filmesRepo.select_drama_filmes(genero="Drama")
        logger.warning(f'Filmes')
        logger.warning(f'{result}')
        logger.warning(f'{result[0].titulo} - {result[0].genero} - {result[0].ano} - {result[0].atores}')

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == '__main__':
    main()

# python -m pip install --upgrade SQLAlchemy
# python main.py
