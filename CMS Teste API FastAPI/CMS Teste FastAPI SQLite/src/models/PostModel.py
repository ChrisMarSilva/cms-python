import datetime as _dt
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import src.database as _database


#post_tag = _sql.Table('post_tag', _database.session.Base.metadata, _sql.Column('tag_id', _sql.Integer, _sql.ForeignKey('posts.id')))

class PostModel(_database.session.Base):
    __tablename__ = "posts"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String, index=True)
    content = _sql.Column(_sql.String, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"), nullable=False)
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    date_last_updated = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow)
    owner = _orm.relationship("UserModel", back_populates="posts", foreign_keys=[owner_id]) #

    # def __init__(self, idd: int = 0, title: str = None, content: str = None, owner_id: int = 0) -> None:
    #     self.id = idd
    #     self.title = title
    #     self.content = content
    #     self.owner_id = owner_id

    def __repr__(self):
        return f"<Post(id={self.id}, " \
               f"title=\"{self.title}\", " \
               f"content=\"{self.content}\", " \
               f"owner_id={self.owner_id})>"
