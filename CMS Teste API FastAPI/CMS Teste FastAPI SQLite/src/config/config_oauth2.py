from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import src.config.config_token as _token
import src.schemas as _schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return _token.verify_token(data, credentials_exception)


async def get_current_active_user(current_user: _schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
