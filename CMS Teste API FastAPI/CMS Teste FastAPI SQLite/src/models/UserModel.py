import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import src.database as _database


#user_tag = _sql.Table('user_tag', _database.session.Base.metadata, _sql.Column('user_id', _sql.Integer, _sql.ForeignKey('users.id')))


class UserModel(_database.session.Base):
    __tablename__ = "users"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    email = _sql.Column(_sql.String, unique=True, index=True)
    hashed_password = _sql.Column(_sql.String)
    is_active = _sql.Column(_sql.Boolean, default=True)
    posts = _orm.relationship("PostModel", back_populates="owner", uselist=True, foreign_keys="[PostModel.owner_id]")  # , lazy="joined" , secondary=user_tag,

    # def __init__(self, idd: int = 0, email: str = None, hashed_password: str = None, is_active: bool = None) -> None:
    #     self.id = idd
    #     self.email = email
    #     self.hashed_password = hashed_password
    #     self.is_active = is_active

    def __repr__(self):
        return f"<UserModel(id={self.id}, " \
               f"email=\"{self.email}\", " \
               f"hashed_password=\"{self.hashed_password}\", " \
               f"is_active=\"{self.is_active}\", " \
               f"posts={str(self.posts)})>"
