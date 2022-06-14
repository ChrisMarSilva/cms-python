from loguru import logger
import time
import datetime as dt
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import select
from dotenv import load_dotenv


Base = declarative_base()


class User(Base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)
    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"


def teste_01_sqlalchemy_insert(engine: sqlalchemy.engine.Engine) -> None:

    from sqlalchemy.orm import Session
    with Session(bind=engine) as session:
        spongebob = User( name="spongebob", fullname="Spongebob Squarepants", addresses=[Address(email_address="spongebob@sqlalchemy.org")])
        sandy = User(name="sandy", fullname="Sandy Cheeks", addresses=[Address(email_address="sandy@sqlalchemy.org"), Address(email_address="sandy@squirrelpower.org")])
        patrick = User(name="patrick", fullname="Patrick Star")
        session.add_all([spongebob, sandy, patrick])
        session.commit()


def teste_01_sqlalchemy_select(engine: sqlalchemy.engine.Engine) -> None:

    from sqlalchemy.orm import Session
    session = Session(bind=engine)

    stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))
    for user in session.scalars(stmt):
        logger.info(user)

    stmt = (select(Address).join(Address.user).where(User.name == "sandy").where(Address.email_address == "sandy@sqlalchemy.org"))
    sandy_address = session.scalars(stmt).one()
    logger.info(sandy_address)

    stmt = select(User).where(User.name == "patrick")
    patrick = session.scalars(stmt).one()
    patrick.addresses.append(Address(email_address="patrickstar@sqlalchemy.org"))
    logger.info(patrick)

    session.close()


def teste_01_sqlalchemy_alter(engine: sqlalchemy.engine.Engine) -> None:

    from sqlalchemy.orm import Session
    session = Session(bind=engine)

    stmt = (select(Address).join(Address.user).where(User.name == "sandy").where(Address.email_address == "sandy@sqlalchemy.org"))
    sandy_address = session.scalars(stmt).one()
    logger.info(sandy_address)
    sandy_address.email_address = "sandy_cheeks@sqlalchemy.org"

    session.commit()
    session.close()


def teste_01_sqlalchemy_delete(engine: sqlalchemy.engine.Engine) -> None:

    from sqlalchemy.orm import Session
    session = Session(bind=engine)

    stmt = (select(Address).join(Address.user).where(User.name == "sandy").where(Address.email_address == "sandy_cheeks@sqlalchemy.org"))
    sandy_address = session.scalars(stmt).one()
    sandy = session.get(User, 2)
    sandy.addresses.remove(sandy_address)
    session.flush()

    stmt = select(User).where(User.name == "patrick")
    patrick = session.scalars(stmt).one()
    logger.info(patrick)
    session.delete(patrick)

    session.commit()
    session.close()


def teste_02_sqlalchemy_insert(engine: sqlalchemy.engine.Engine) -> None:

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    user = User(name="patrick", fullname="Patrick Star")
    session.add(user)
    logger.info(f"{session.new=}")

    session.add(User(name="cms", fullname="Chris Star"))
    session.add(User(name="sei la", fullname="SeiLa Star"))
    logger.info(f"{session.new=}")

    session.commit()
    logger.info(f"{session.new=}")

    session.close()


def teste_02_sqlalchemy_select(engine: sqlalchemy.engine.Engine) -> None:

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    logger.info("user")
    # user = session.query(User).filter(User.name == 'patrick').first()
    user = session.query(User).filter_by(name='patrick').first()
    logger.info(user)
    logger.info(user.name)
    
    logger.info("users")
    users = session.query(User).order_by(User.id)
    for user in users:
        logger.info(user)

    session.close()


def teste_02_sqlalchemy_alter(engine: sqlalchemy.engine.Engine) -> None:

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    logger.info("name alter")
    user = session.query(User).filter_by(name='patrick').first()
    logger.info(f"name old: {user.name}")
    logger.info(f"{session.dirty=}")
    user.name = f"{user.name} #2"
    logger.info(f"name new: {user.name}")
    logger.info(f"{session.dirty=}")

    session.commit()
    
    user = session.query(User).filter_by(name='patrick #2').first()
    logger.info(f"name atual: {user.name}")

    session.close()


def teste_02_sqlalchemy_delete(engine: sqlalchemy.engine.Engine) -> None:

    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()

    user = session.query(User).first()
    logger.info(f"name delete: {user.name}")
    session.delete(user)
    session.commit()

    session.close()


def main() -> None:
    try:

        logger.info(f'Inicio') 
        start_time = time.perf_counter()  # time.time()  # time.perf_counter()  # time.perf_counter_ns()  # time.process_time()

        logger.info('version', sqlalchemy.__version__ )

        engine = create_engine("sqlite://", echo=True, future=True)
        # engine = create_engine("sqlite:///banco.db", echo=True, future=True)

        Base.metadata.create_all(bind=engine)
        
        # logger.info(f"teste_01")
        # teste_01_sqlalchemy_insert(engine=engine)
        # teste_01_sqlalchemy_select(engine=engine)
        # teste_01_sqlalchemy_alter(engine=engine)
        # teste_01_sqlalchemy_delete(engine=engine)
        
        # logger.info(f"teste_02")
        # teste_02_sqlalchemy_insert(engine=engine)
        # teste_02_sqlalchemy_select(engine=engine)
        # teste_02_sqlalchemy_alter(engine=engine)
        # teste_02_sqlalchemy_delete(engine=engine)

        end_time = time.perf_counter() - start_time  # time.time() # time.perf_counter() # time.perf_counter_ns() # time.process_time()
        logger.info(f"Fim - Done in {end_time:.2f}s - {dt.timedelta(seconds=end_time)}")

    except Exception as e:
        logger.error(f'Falha Geral(main): "{str(e)}"')


if __name__ == '__main__':
    main()

# python -m pip install --upgrade SQLAlchemy
# python main.py
