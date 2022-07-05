from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.token import verify_token

# OAuth2PasswordRequestForm lo que hace es obtener las credecnciales que ingresamos para autorizar

# En tokenUrl le pasamos la url donde se hace la validacion del token que es login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verificamos el token pasandolo a al fucnion verify token y ademas las credential exeptions en caso de que no encuentre el usuario
    return verify_token(token, credentials_exception)