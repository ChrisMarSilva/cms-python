import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import sqlalchemy.ext.declarative as _declarative
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
#import databases


SQLALCHEMY_DATABASE_URL = "sqlite:///./webapp.db"
engine = _sql.create_engine(url=SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True, connect_args={"check_same_thread": False})
SessionLocal = _orm.sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=_orm.Session)
Base = _declarative.declarative_base()

SQLALCHEMY_DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./webapp.db"
#database = databases.Database(url=SQLALCHEMY_DATABASE_URL_ASYNC)
engine_async = create_async_engine(url=SQLALCHEMY_DATABASE_URL_ASYNC, future=True, echo=True, pool_pre_ping=True, connect_args={"check_same_thread": False})
SessionAsync = _orm.sessionmaker(bind=engine_async, autoflush=False, autocommit=False, expire_on_commit=False, class_=AsyncSession)



'''





import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import sqlalchemy.ext.declarative as _declarative
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
#import databases



# SQLALCHEMY_DATABASE_URL = "sqlite:///./webapp.db"
# engine = _sql.create_engine(url=SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True, connect_args={"check_same_thread": False})

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:pass@localhost:3306/banco'
engine = _sql.create_engine(url=SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = _orm.sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=_orm.Session)
Base = _declarative.declarative_base()

# SQLALCHEMY_DATABASE_URL_ASYNC = "sqlite+aiosqlite:///./webapp.db"
# #database = databases.Database(url=SQLALCHEMY_DATABASE_URL_ASYNC)
# engine_async = create_async_engine(url=SQLALCHEMY_DATABASE_URL_ASYNC, future=True, echo=False, pool_pre_ping=True, connect_args={"check_same_thread": False})
# SessionAsync = _orm.sessionmaker(bind=engine_async, autoflush=False, autocommit=False, expire_on_commit=False, class_=AsyncSession)


'''