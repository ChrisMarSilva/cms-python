from typing import Iterator
import sqlalchemy.orm as _orm
import src.models as _models


class ContactRepository:

    # def __init__(self) -> None:
    #     ...

    @classmethod
    async def get_all(cls, db: _orm.Session) -> Iterator[_models.ContactModel]:
        return db.query(_models.ContactModel).all()

    @classmethod
    async def get_by_id(cls, db: _orm.Session, contact_id: int) -> _models.ContactModel:
        return db.query(_models.ContactModel).filter(_models.ContactModel.id == contact_id).first()

    @classmethod
    async def create(cls, db: _orm.Session, contact: _models.ContactModel) -> _models.ContactModel:
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact

    @classmethod
    async def update(cls, db: _orm.Session, contact: _models.ContactModel) -> _models.ContactModel:
        db.commit()
        db.refresh(contact)
        return contact

    @classmethod
    async def delete_by_id(cls, db: _orm.Session, contact: _models.ContactModel) -> None:
        db.delete(contact)
        db.commit()
