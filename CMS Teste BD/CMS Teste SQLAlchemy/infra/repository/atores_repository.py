from infra.configs.connection import DBConnectionHandler
from infra.entities.atores import Atores
from infra.entities.filmes import Filmes


class AtoresRepository:

    def select_all(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session.query(Atores).all()
                return data
            except Exception as exception:
                db.session.rollback()
                raise exception

    def select_with_filmes(self):
        with DBConnectionHandler() as db:
            try:
                data = db.session\
                    .query(Atores)\
                    .join(Filmes, Atores.titulo_filme == Filmes.titulo)\
                    .with_entities(Atores.nome, Filmes.genero, Filmes.titulo)\
                    .all()
                return data
            except Exception as exception:
                db.session.rollback()
                raise exception
