import datetime as _dt
import sqlalchemy as _sql
import src.database as _database


class ContactModel(_database.session.Base):
    __tablename__ = "contacts"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    first_name = _sql.Column(_sql.String, index=True)
    last_name = _sql.Column(_sql.String, index=True)
    email = _sql.Column(_sql.String, index=True, unique=True)
    phone_number = _sql.Column(_sql.String, index=True, unique=True)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)

    # def __init__(self, idd: int = 0, first_name: str = None, last_name: str = None, email: str = None, phone_number: str = None) -> None:
    #     self.id = idd
    #     self.first_name = first_name
    #     self.last_name = last_name
    #     self.email = email
    #     self.phone_number = phone_number

    def __repr__(self):
        return f"<Contact(id={self.id}, " \
               f"first_name=\"{self.first_name}\", " \
               f"last_name=\"{self.last_name}\", " \
               f"email=\"{self.email}\", " \
               f"phone_number={self.phone_number})>"
