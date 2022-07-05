from fastapi import APIRouter, Depends, status
from app.db.database import get_db
from typing import List
from sqlalchemy.orm import Session
from app.schemas import Login
from app.repositiry import auth
from fastapi.security import OAuth2PasswordRequestForm

# Definimos nuestro router
router = APIRouter(
    prefix = "/login",
    tags = ["Login"]
)


# En este caso como response model devolvemos una lista de showuser ya que este endpoint devuelve una lista de valores
@router.post('/', status_code=status.HTTP_200_OK)
# Le indicamos que la session va a ser igual a lo que devuelva get_db que es en realidad la sesion de la bse de datos
def login(usuario:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    # REcibimos la informacion de autenticacion
    auth_token = auth.auth_user(usuario, db)
    # Retornamos la informacion de autenticacion 
    return auth_token