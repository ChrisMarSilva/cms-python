import fastapi as _fastapi
from fastapi.security import OAuth2PasswordRequestForm
import sqlalchemy.orm as _orm
import src.services as _services
import src.schemas as _schemas
import src.database as _database
from src.config.config_hashing import Hash
import src.config.config_token as _token
import src.config.config_oauth2 as _oauth2
from src.config.config_auth_bearer import JWTBearer
from src.config.config_auth_handler import signJWT


router = _fastapi.APIRouter(prefix="/auth", tags=['auth'])


@router.post("/login", status_code=_fastapi.status.HTTP_200_OK)
async def get_login(request: OAuth2PasswordRequestForm = _fastapi.Depends(),db: _orm.Session = _fastapi.Depends(_database.base.get_db)):
    try:
        db_user = await _services.UserService.get_user_by_email(db=db, email=request.username)
        if not db_user:
            raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
        if not Hash.verify(db_user.hashed_password, request.password):
            raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_404_NOT_FOUND, detail=f"Incorrect password")
        access_token = _token.create_access_token(data={"sub": db_user.email, "id": db_user.id})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/token")
async def get_token(current_user: _schemas.User = _fastapi.Depends(_oauth2.get_current_user)):
    try:
        return {"token-id": current_user.id, "token-email": current_user.username}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/logado", status_code=_fastapi.status.HTTP_200_OK)
async def get_logado(current_user: _schemas.User = _fastapi.Depends(_oauth2.get_current_user)):
    try:
        return {"logado-id": current_user.id, "logado-email": current_user.username}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/loginteste", status_code=_fastapi.status.HTTP_200_OK)
async def get_login_teste():
    try:
        access_token = signJWT("email@gmail.com")
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/tokenteste")
async def get_token_teste(current_user: _schemas.User = _fastapi.Depends(JWTBearer())):
    try:
        return {"token-id": "get_teste"}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

