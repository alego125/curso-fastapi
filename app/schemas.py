from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Union

#User model
class User(BaseModel): #Schema
    username:str
    password:str
    nombre:str
    apellido:str
    direccion:Optional[str]
    telefono:int
    correo:str
    creacion:datetime = datetime.now() # Le colocamos la fecha por defecto si no se envia nada de ahora

# Creamos schema con valores None para que no sean requeridos y se puedan usar en un update sin problemas de manera parcial
class UpdateUser(BaseModel):    
    # Al colocarle None lo que sucede es que si no se coloca valor es como si no existe el campo del modelo directamente entonces se puede usar perfectamente apra actualizaciones parciales de informacion 
    username:str = None
    password:str = None
    nombre:str = None
    apellido:str = None
    direccion:str = None
    telefono:int = None
    correo:str = None


# Creamos un modelo que sera el que se muestre como response model a la hora de hacer una peticion a la base de datos
class ShowUser(BaseModel):
    username:str
    nombre:str
    apellido:str
    correo:str
    class Config():
        # Configuro la clase para que reconozca el orm de sqlalchemy en este caso y pueda devolver esta informacion
        orm_mode = True


# CLase modelo para la informacion que enviamos del login
class Login(BaseModel):
    username:str
    password:str

# Modelos para el token
class Token(BaseModel):
    access_token:str
    token_type:str

class Tokendata(BaseModel):
    username: Union[str,None] = None