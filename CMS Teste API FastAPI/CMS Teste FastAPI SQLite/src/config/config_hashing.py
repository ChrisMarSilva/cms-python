from passlib.context import CryptContext


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:

    @classmethod
    def bcrypt(cls, password: str):
        return pwd_cxt.hash(password)

    @classmethod
    def verify(cls, hashed_password: str, plain_password: str):
        return pwd_cxt.verify(secret=plain_password, hash=hashed_password)
