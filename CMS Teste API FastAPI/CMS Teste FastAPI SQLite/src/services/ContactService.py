import sqlalchemy.orm as _orm
from typing import Iterator
import src.models as _models
import src.schemas as _schemas
import src.repositories as _repositories
import src.services as _services


class ContactService(_services.BaseService):

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    async def get_all_contacts(cls, db: _orm.Session) -> Iterator[_schemas.Contact]:
        #self.logger.debug("get_all_contacts")
        contacts = await _repositories.ContactRepository.get_all(db)
        return list(map(_schemas.Contact.from_orm, contacts))

    @classmethod
    async def get_contact(cls, db: _orm.Session, contact_id: int) -> _models.ContactModel:
        #self.logger.debug("get_contact")
        return await _repositories.ContactRepository.get_by_id(db, contact_id)

    @classmethod
    async def create_contact(cls, db: _orm.Session, contact: _schemas.CreateContact) -> _schemas.Contact:
        #self.logger.debug("create_contact")
        contact = _models.ContactModel(**contact.dict())
        contact = await _repositories.ContactRepository.create(db, contact)
        return _schemas.Contact.from_orm(contact)

    @classmethod
    async def update_contact(cls, db: _orm.Session, contact_data: _schemas.CreateContact, contact: _models.ContactModel) -> _schemas.Contact:
        #self.logger.debug("update_contact")
        contact.first_name = contact_data.first_name
        contact.last_name = contact_data.last_name
        contact.email = contact_data.email
        contact.phone_number = contact_data.phone_number
        contact = await _repositories.ContactRepository.update(db, contact)
        return _schemas.Contact.from_orm(contact)

    @classmethod
    async def delete_contact(cls, db: _orm.Session, contact: _models.ContactModel) -> None:
        #self.logger.debug("delete_contact")
        return await _repositories.ContactRepository.delete_by_id(db, contact)
