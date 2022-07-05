from fastapi import APIRouter, Depends, status
from app.oauth import get_current_user
from app.schemas import User, ShowUser, UpdateUser
from app.db.database import get_db
from typing import List
from sqlalchemy.orm import Session
from app.repositiry import user

# Definimos nuestro router
router = APIRouter(
    prefix = "/user",
    tags = ["Users"]
)

# En este caso como response model devolvemos una lista de showuser ya que este endpoint devuelve una lista de valores
@router.get('/', response_model=List[ShowUser], status_code=status.HTTP_200_OK)
# Le indicamos que la session va a ser igual a lo que devuelva get_db que es en realidad la sesion de la bse de datos
def obtener_usuarios(db:Session = Depends(get_db),  current_user: User = Depends(get_current_user)):
    response = user.obtener_usuarios(db)
    return response



@router.post('/crear-usuario', status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario:User, db:Session = Depends(get_db)): # Al indicar que el parametro es de tipo User le 
    user.crear_usuario(usuario, db)
    return {'respuesta':'Usuario creado correctamente'}


# Para query param puedo utilizar get
# Con response model le decimos a la api que queremos que nos devuelva solo lo que tenemos en el response model
@router.get('/{user_id}', response_model=ShowUser, status_code=status.HTTP_200_OK)
def obtener_usuario(user_id:int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    usuario = user.obtener_usuario(user_id, db)
    return usuario

@router.delete('/{user_id}', status_code=status.HTTP_200_OK)
def eliminar_usuario(user_id:int, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = user.eliminar_usuario(user_id, db)
    return response

#Acutalizar
@router.patch('/{user_id}', status_code=status.HTTP_200_OK)
def actualizazr_usuario(user_id:int, updateUser:UpdateUser, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = user.actualizar_ususario(user_id, updateUser, db)
    return response


"""

#Acutalizar
@router.put('/')
def actualizazr_usuario(updateUser:User):
    for index, user in enumerate(usuarios):
        if user['id'] == updateUser.id:
            # Ahora actualizamos la infroamcion del elemento del arreglo con la informacion recibida
            usuarios[index]['id'] = updateUser.dict()['id']
            usuarios[index]['nombre'] = updateUser.dict()['nombre']
            usuarios[index]['apellido'] = updateUser.dict()['apellido']
            usuarios[index]['direccion'] = updateUser.dict()['direccion']
            usuarios[index]['telefono'] = updateUser.dict()['telefono']
            return {'respuesta':'Usuario actualizado correctamente'}
    return {'respuesta':'Usuario no encontrado'}"""