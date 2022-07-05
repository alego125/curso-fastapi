from pyexpat import model
from sqlalchemy.orm import Session
from app.db import models
from fastapi import HTTPException, status
from app.hashing import Hash
from app.token import create_access_token

# Creamos la funcion que se va a encargar de filtrar los usuarios
def auth_user(usuario, db:Session):
    
    # Filtramos de la base de datos aquellos que coincida el username de la base de datos con lo que trae el modelo y con first nos devuelve el primero que encuentra
    user = db.query(models.User).filter(models.User.username == usuario.username).first()
    if not user:
        # Si no existe usuario con el username indicado entonces lanzamos el error o exception
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario indicado {usuario.username} por lo tanto no se realiza el login"
        )
    
    # Le pasamos el password que le enviamos y el user.password es lo que traemos de la base de datos
    if not Hash.verify_password(usuario.password, user.password):
        # Si las contraseñas de la base de datos no coinciden entonces enviamos la excepcion
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contraseña incorrecta"
        )

    # Si llegamos hasta aqui quiere decir que se ha verificado que la contraseña y el usuario coinciden
    # Ahora usamos el jwt
    # Creamos la variable con la inforamcion del usuario pero en forma ded token
    access_token = create_access_token(
        data={"sub": usuario.username}
    )
    # Retorna mos el token de acceso y el tipo de token que sera bearer
    return {"access_token": access_token, "token_type": "bearer"}