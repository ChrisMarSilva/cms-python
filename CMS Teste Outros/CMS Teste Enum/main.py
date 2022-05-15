from loguru import logger
import time
import datetime as dt
from enum import Enum, unique, auto


def main():
    start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time() # time.monotonic()
    logger.info(f'Inicio') 
    try:

        @unique
        class Minificacao(Enum):
            REQUESTS = 1
            HTMLMIN = 2
            MINIFYHTML = auto()

        tipo = Minificacao.REQUESTS
        logger.info(f'{tipo=}')
        logger.info(f'{tipo.name=}')
        logger.info(f'{tipo.value=}')
        logger.info(f'{repr(tipo)=}')
        logger.info(f'{type(tipo)=}')
        logger.info(f'{isinstance(tipo, Minificacao)=}')

        if tipo == Minificacao.REQUESTS: logger.info('OK')

        tipo = Minificacao.MINIFYHTML
        logger.info(f'{tipo=}')
            
        class ExtendedEnum(Enum):

            @classmethod
            def list(cls):
                return list(map(lambda c: c.value, cls))
                
        class OperationType(ExtendedEnum):
            CREATE = 'CREATE'
            STATUS = 'STATUS'
            EXPAND = 'EXPAND'
            DELETE = 'DELETE'
        
        tipo = OperationType.CREATE
        logger.info(f'{tipo=}')
        
        logger.info(OperationType.list())

        class OperationType2(Enum):
            CREATE = 'CREATE'
            STATUS = 'STATUS'
            EXPAND = 'EXPAND'
            DELETE = 'DELETE'

            @staticmethod
            def list():
                return list(map(lambda c: c.value, OperationType2))

            @classmethod
            def list_roles(cls):
                role_names = [member.value for role, member in cls.__members__.items()]
                return role_names

        logger.info(list(map(str, OperationType2)))
        logger.info(list(map(lambda x: x.value, OperationType2._member_map_.values())))
        logger.info(OperationType2.list())

        class SuperEnum(Enum):    
            @classmethod
            def to_dict(cls):
                return {e.name: e.value for e in cls}
            
            @classmethod
            def keys(cls):
                return cls._member_names_
            
            @classmethod
            def values(cls):
                return list(cls._value2member_map_.keys())
                
        class Roles(SuperEnum):
            ADMIN = 1
            USER = 2
            GUEST = 3

        Roles.to_dict() # {'ADMIN': 1, 'USER': 2, 'GUEST': 3}
        Roles.keys() # ['ADMIN', 'USER', 'GUEST']
        Roles.values() # [1, 2, 3]

        # python main.py

    except Exception as e:
        logger.error(f'Falha Geral: "{str(e)}"')
    finally:
        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()  # time.monotonic()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")


if __name__ == '__main__':
    main()

# python -m pip install --upgrade xxxx
# python main.py
