# import os
# from datetime import datetime, timedelta
# from hashlib import algorithms_available
# from typing import Any, Optional
#
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt
# from passlib.context import CryptContext
# from sqlalchemy.orm import Session
#
# from app.config import settings
#
# from .users import get_user_by_username
#
# ALGORITHM: str = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
#
# pwd_context: Any = CryptContext(schemes=["pbkdf2_sha512"], deprecated="auto")
# oauth2_scheme: Any = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def get_hash_password(password: str) -> Any:
#     return pwd_context.hash(password)
#
#
# def verify_password(plain_password, hashed_password) -> Any:
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def authenticate_user(db: Session, username: str, password: str) -> Any:
#     user = get_user_by_username(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(
#     data: dict, expires_delta: Optional[timedelta] = None
# ) -> Any:
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(
#         to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
#     )
#     return encoded_jwt

#
# from typing import Any, Generator
# 
# from fastapi import Depends, HTTPException, status
# from jose import JWTError, jwt
# from sqlalchemy.orm import Session
#
# from app import schemas
# from app.config import settings
# from app.db.session import SessionLocal
#
# from .security import ALGORITHM, oauth2_scheme
# from .users import get_user_by_username
#
# def get_current_user(
#     db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
# ) -> Any:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(
#             token, settings.SECRET_KEY, algorithms=[ALGORITHM]
#         )
#         username: str = payload.get("sub")
#         token_data = schemas.TokenData(username=username)
#     except JWTError:  # pragma: no cover
#         raise credentials_exception
#     user = get_user_by_username(db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# def get_current_active_user(
#     current_user: schemas.User = Depends(get_current_user),
# ) -> Any:
#     if current_user.disabled:
#         raise HTTPException(status_code=401, detail="Inactive user")
#     return current_user