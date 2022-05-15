import time
from typing import Dict
#import jwt
from jose import JWTError, jwt


JWT_SECRET = "070ca90e58cd94dd24405fef93dabc4026023b989c98e257f022e13b00c19c2c"
JWT_ALGORITHM = jwt.ALGORITHMS.HS512  # jwt.ALGORITHMS.HS256  # "HS256"


def token_response(token: str):
    return {"access_token": token}


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {"user_id": user_id, "expires": time.time() + 600}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str) -> dict:
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return decoded_token if decoded_token["expires"] >= time.time() else {}
