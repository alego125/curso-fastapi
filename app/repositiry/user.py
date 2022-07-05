from sqlalchemy.orm import Session
from app.db import models
from app.schemas import UpdateUser, User
from fastapi import HTTPException, status
from app.hashing import Hash

def crear_usuario(usuario:User, db:Session):
    # Agregamos un try catch para capturar la excepcion o error de la peticion y motrar el correspondiente mensaje
    try:
    #decimos que tiene la estructura del la clase user
        usuario = usuario.dict()
        nuevo_usuario = models.User(
            username = usuario['username'],
            password = Hash.hash_password(usuario['password']),
            nombre = usuario['nombre'],
            apellido = usuario['apellido'],
            direccion = usuario['direccion'],
            telefono = usuario['telefono'],
            correo = usuario['correo']
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
    except Exception as e:
        raise HTTPException(
            # Pasamos el status code
            status_code=status.HTTP_409_CONFLICT,
            # Le pasamos el detalle del error con un mensaje e imprimimos la e que contiene el error en si
            detail = f"Error creando usuario {e}"
        )

def obtener_usuario(user_id:int, db:Session):
    # Mediante un query param traemos un solo elemento, esto es asi por que esta consulta puede traer varios elementos que coincidan para eso usamos first(), este caso no sera ya uqe solo puede existir un id pero se puede dar el caso que hayan mas de un resultado y solo queramos el primero que coincida
    usuario = db.query(models.User).filter(models.User.id == user_id).first()
    if not usuario:
        # Si no se enceuntra el usuario mandamos el sigueinte error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id}"
        )
    # Si lo encontro entonces retorno el query
    return usuario


def obtener_usuarios(db:Session):
    data = db.query(models.User).all() # Obtenemos todos los campos de el modelo USers en la session que es db
    return data


def eliminar_usuario(user_id:int, db:Session):
    # El .first() no podemos colocarlo a la query ya que de esta manera no nos va a funcionar el borrado
    usuario = db.query(models.User).filter(models.User.id == user_id)
    if not usuario.first():
         # Si no se enceuntra el usuario mandamos el sigueinte error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id} por lo tanto no se elimina"
        )
    usuario.delete(synchronize_session=False) # Eliminamos el usuario y le decimos que no sincronice la sesion ya que la eliminacion queremos que lleve a cabo con el commit
    db.commit()
    return {'respuesta':'Usuario eliminado correctamente'}

def actualizar_ususario(user_id:int, updateUser:UpdateUser, db:Session):
    usuario = db.query(models.User).filter(models.User.id == user_id)
    
    if not usuario.first():
        # Si no se enceuntra el usuario mandamos el sigueinte error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe el usuario con el id {user_id} por lo tanto no se puede actualizar"
        )
    
    # Usamos un update y le pasamos el usuario en forma de diccionario y le decimos excluede unset para que solo actualice los que estan llegando nada mas
    usuario.update(updateUser.dict(exclude_unset=True))
    db.commit()
    return {'respuesta':'Usuario actualizado correctamente'}