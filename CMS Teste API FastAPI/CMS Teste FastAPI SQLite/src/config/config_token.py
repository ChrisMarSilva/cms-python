from datetime import datetime, timedelta
from jose import JWTError, jwt
import src.schemas as _schemas


SECRET_KEY = "070ca90e58cd94dd24405fef93dabc4026023b989c98e257f022e13b00c19c2c"
ALGORITHM = jwt.ALGORITHMS.HS512  # jwt.ALGORITHMS.HS256  # "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    str_decode_token = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    return str_decode_token if str_decode_token["expires"] >= datetime.time else None


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload:
            raise credentials_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        idd: str = payload.get("id")
        if idd is None:
            raise credentials_exception
        token_data = _schemas.TokenData(id=int(idd), username=email)
        return token_data
    except JWTError:
        raise credentials_exception
