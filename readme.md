# Dos formas de correr fastApi server

    1) uvicorn main:app
    2) Agregar las lineas de codigo
        if __name__ == "__main__":
            uvicorn.run("main:app", port=8000, reload=True) el reload es para que actualice los cambios automaticamente

        Y luego correr en la terminal main.py

- Importamos pydentic
  from pydantic import BaseModel
  Esta es una libreria que nos permite escribir los datos en un modelo para luego usarlo, esta libreria viene ya instalada dentro de fastapi

- Tipo de dato opcional
  from typing import Optional
  Se importa la libreria yluego para usarla por ejemplo
  class User(BaseModel):
  id:str
  nombre:str
  apellido:str
  direccion:Optional[str]
  -> Con esto estamos diciendo que en el modelo la direccion puede o no enviarse asi de esta manera no generamos conflictos

### Aclaracion
- Para las peticiones de tipo GET podemos enviarle query parameters para por ejemplo buscar un id en una base de datos, pero si queremos hacer lo mismo con un parametro de tipo request body a partir de un modelo no vamos a poder, en ese caso si o si tenemos que usar una peticion de tipo post ya uqe las de tipo get no permiten el envio de request body

## Para ordenar el codigo

Creamos los routers que se van a encargar de la redireccion en nuestra api, para esto creamos una carpeta app y dentro de esta carpeta una llamada routers con su respectivo archivo **init**.py

# Manejo de base de datos PostgreSQL con psycopg2

- Primero instalamos psycopg2 con pip isntall psycopg2
~~~
import psycopg2

connection = psycopg2.connect(
host="localhost",
user="postgres",
password="admin",
database="postgres",
port="5432"
)
~~~
Para que se hagan autocomit automaticamente a la base ed datos
connection.autocommit = True
~~~
def crear_tabla():
cursor = connection.cursor()
query = "CREATE TABLE usuario(nombre varchar(30), correo varchar(30), direccion varchar(30))"

    try:
        cursor.execute(query)
    except:
        print("La tabla usuario ya existe")

    cursor.close()

def insertar_datos(nombre, correo, direccion):
cursor = connection.cursor()
query = f""" INSERT INTO usuario(nombre, correo, direccion) VALUES('{nombre}','{correo}','{direccion}') """
try:
cursor.execute(query)
except:
print("La tabla usuario no existe")

    cursor.close()

def actualizarInformacion():
cursor = connection.cursor()
query = """ UPDATE usuario SET nombre='Andres' WHERE nombre='Alejandro' """
try:
cursor.execute(query)
except:
print("La tabla usuario no existe")

    cursor.close()

def eliminarTabla():
cursor = connection.cursor()
query = "DROP TABLE usuario"
try:
cursor.execute(query)
except:
print("La tabla usuario no existe")

    cursor.close()

def eliminarEntrada(nombre):
cursor = connection.cursor()
query = f"DELETE FROM usuario WHERE nombre='{nombre}'"
try:
cursor.execute(query)
except:
print("La tabla usuario no existe")

    cursor.close()

insertar_datos('alejandro','ale.gomez@gmail.com','pichincha 45')
actualizarInformacion()
#eliminarEntrada('alejandro')
~~~
# Creacion de conexiones y configuraciones de la base de datos

1. Creamos carpeta db dentro de app
2. Dentro de db creamos un archivo py models para colocar los modelos de la base de datos y luego otro database para la informacion de conexion de la case de dato

Para la conexion de la base de datos usamos las siguientes importaciones
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Luego lo que hacemos es colocar la url seteada para la conexion que contenga toda la informacion
~~~
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:conteraseña@localhost:5432/nombreBaseDeDatos"
~~~
Seguido seteamos en el engine o motor de base de datos los datos de conexion en la url de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

- Este engine es el encargado de interactuar con la base de datos
- Luego de esto tendremos un session que sera el responsable de que nosotros sepamos como estan los datos actualmente
  SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
- Por ultimo declaramos nuestro base, con el cual vamos a comenzar a crear nuestros modelos el cual vamos a utilizar dentro de models
  Base = declarative_base()

### Luego de esto anterior debemos crear las tablas dentro de database.py
~~~
from email.policy import default
from app.db.database import Base
~~~
# Importamos los tipode datos a usar en sqlalchemy
~~~
from sqlalchemy import DATE, Column, Integer, String, Boolean, DateTime
from datetime import datetime

class User(Base):
**tablename**="user"
id = Column(Integer, primary_key=True, autoincrement=True)
nombre = Column(String)
apellido = Column(String)
direccion = Column(String)
telefono = Column(Integer)
correo = Column(String)
creacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
estado = Column(Boolean)
~~~
### Una vez creada las tablas en main.py
~~~
{
"username": "alejogo56",
"password": "anubis90",
"nombre": "Alejandro",
"apellido": "Gomez",
"direccion": "9 de Julio 48",
"telefono": 2604538424,
"correo": "alejandro.gomez969@gmail.com",
"creacion": "2022-07-02T15:10:48.476718"
}
~~~
- Ls consultas a la base de datos van a ir dentro de la carpeta repository en un archivo user.py iran todas las consulatas a la base de datos user

## Pasos a seguir

1.  crear proyecto
2.  instalar pip install virtualenv (si no esta instalado)
3.  Ejecuto para crear entorno virtual en carpeta principal -> virtualenv venv
4.  Inicio virtual env -> venv/Script/activate
5.  Creo archivo -> requirements.txt y dentro coloco (fastapi,uvicorn,psycopg2,SQLAlchemy,python-dotenv)
6.  Creo el archivo en la raiz del programa main.py
    a) Dentro de este archivo llamos a fastAPI, creo las tablas del proyecto en la base de datos e inicializo el programa - Por ejemplo
    <pre><code>
    from fastapi import FastAPI
    import uvicorn
    from app.routers import user
    from app.db.database import Base,engine

             def crearTablas():
                 # Creamos la tabla con el o los modelos que se tienen en base por esto es tan iomportante que los modelos hereden de Base a la hora de declararlos en database.py y luego le indicamos con create_all y bind el engine
                 Base.metadata.create_all(bind=engine)
             crearTablas()

             app = FastAPI()
             # Incluimos el router dentro de nuestra app
             app.include_router(user.router)


             if __name__ == "__main__":
                 uvicorn.run("main:app", port=8000, reload=True)
         </pre></code>

7.  Creo carpetas app, core
8.  Dentro de app:
    - Creo carpetas db, repository, routers y un archivo schemas.py
    - Dentro de db creo dos archivos **init**.py, database.py, models.py - Dentro de database.py creamos todas las configuraciones de la base de datos
    - Por ejemplo:
        <pre><code>
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker
        from core.config import settings

                 # Declaramos una constante que es la que se encargara de hacer la conexion
                 # SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost:5432/postgres"
                 SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
                 engine = create_engine(SQLALCHEMY_DATABASE_URL)
                 SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
                 Base = declarative_base()


                 # Funcion que devuelve la sesion de la base de datos, luego de que hace todo el proceso cierra la conexion
                 def get_db():
                     db = SessionLocal()
                     try:
                         #Devuelve un objeto de tipo session maker
                         yield db
                     finally:
                         db.close()
                         
     Luego dentro de models.py, creamos los modelos que se guardaran dentro de la base de datos
    * Por ejemplo:
             <pre><code>
                 from app.db.database import Base
                 # Importamos los tipode  datos a usar en sqlalchemy
                 from sqlalchemy import Column, Integer, String, Boolean, DateTime
                 from datetime import datetime
                 from sqlalchemy.schema import ForeignKey
                 from sqlalchemy.orm import relationship

                 class User(Base):
                     __tablename__="user"
                     id = Column(Integer, primary_key=True, autoincrement=True)
                     username = Column(String, unique=True)
                     password = Column(String)
                     nombre = Column(String)
                     apellido = Column(String)
                     direccion = Column(String)
                     telefono = Column(String)
                     correo = Column(String, unique=True)
                     creacion =  Column(DateTime, default=datetime.now, onupdate=datetime.now)
                     estado = Column(Boolean, default=False) # Colocamos el estado por default para que la persona lo active por verificacion
                     # Ingicamos mediante relationship que existe una relacion de esta tabla con la de usuario
                     venta = relationship("Venta", backref="user", cascade="delete,merge")


                 class Venta(Base):
                     __tablename__ = "venta"
                     id = Column(Integer, primary_key=True, autoincrement=True)
                     # Este campo sera un entero pero una clave foranea de la tabla user y relacionando el id de esta
                     # Con delete cascade quiere decir que si se borra el usuario las ventas asociadas a este tambien se elmininan
                     usuario_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
                     venta = Column(Integer)
                     ventas_productos = Column(Integer)

c) Dentro de repository creo un archivo user.py - dentro de este archivo armamos todas las funciones que contendran la logica de manejos de datos entre los modelos y la base de datos
* Por ejemplo:
    <pre><code>
    from sqlalchemy.orm import Session
    from app.db import models
    from app.schemas import UpdateUser, User

                 def crear_usuario(usuario:User, db:Session):
                     #decimos que tiene la estructura del la clase user
                     usuario = usuario.dict()
                     nuevo_usuario = models.User(
                         username = usuario['username'],
                         password = usuario['password'],
                         nombre = usuario['nombre'],
                         apellido = usuario['apellido'],
                         direccion = usuario['direccion'],
                         telefono = usuario['telefono'],
                         correo = usuario['correo']
                     )
                     db.add(nuevo_usuario)
                     db.commit()
                     db.refresh(nuevo_usuario)

                 def obtener_usuario(user_id:int, db:Session):
                     # Mediante un query param traemos un solo elemento, esto es asi por que esta consulta puede traer varios elementos que coincidan para eso usamos first(), este caso no sera ya uqe solo puede existir un id pero se puede dar el caso que hayan mas de un resultado y solo queramos el primero que coincida
                     usuario = db.query(models.User).filter(models.User.id == user_id).first()
                     if not usuario:
                         return {'respuesta':'Usuario no encontrado!!'} # En caso de que no se encuentre el id
                     # Si lo encontro entonces retorno el query
                     return usuario


                 def obtener_usuarios(db:Session):
                     data = db.query(models.User).all() # Obtenemos todos los campos de el modelo USers en la session que es db
                     return data


                 def eliminar_usuario(user_id:int, db:Session):
                     # El .first() no podemos colocarlo a la query ya que de esta manera no nos va a funcionar el borrado
                     usuario = db.query(models.User).filter(models.User.id == user_id)
                     if not usuario.first():
                         return {'respuesta':'Usuario no encontrado!!'}
                     usuario.delete(synchronize_session=False) # Eliminamos el usuario y le decimos que no sincronice la sesion ya que la eliminacion queremos que lleve a cabo con el commit
                     db.commit()
                     return {'respuesta':'Usuario eliminado correctamente'}

                 def actualizar_ususario(user_id:int, updateUser:UpdateUser, db:Session):
                     usuario = db.query(models.User).filter(models.User.id == user_id)

                     if not usuario.first():
                         return {'respuesta':'Usuario no encontrado'}

                     # Usamos un update y le pasamos el usuario en forma de diccionario y le decimos excluede unset para que solo actualice los que estan llegando nada mas
                     usuario.update(updateUser.dict(exclude_unset=True))
                     db.commit()
                     return {'respuesta':'Usuario actualizado correctamente'}

d) Dentro de routers colocamos el archivo **init**.py, user.py - Dentro del archivo user.py definimos todos nuestros endpoints
* Por ejemplo:
   <pre><code>
    from fastapi import APIRouter, Depends
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
                 @router.get('/', response_model=List[ShowUser])
                 # Le indicamos que la session va a ser igual a lo que devuelva get_db que es en realidad la sesion de la bse de datos
                 def obtener_usuarios(db:Session = Depends(get_db)):
                     response = user.obtener_usuarios(db)
                     return response



                 @router.post('/crear-usuario')
                 def crear_usuario(usuario:User, db:Session = Depends(get_db)): # Al indicar que el parametro es de tipo User le
                     user.crear_usuario(usuario, db)
                     return {'mensaje':'Usuario creado correctamente'}


                 # Para query param puedo utilizar get
                 # Con response model le decimos a la api que queremos que nos devuelva solo lo que tenemos en el response model
                 @router.get('/{user_id}', response_model=ShowUser)
                 def obtener_usuario(user_id:int, db:Session = Depends(get_db)):
                     usuario = user.obtener_usuario(user_id, db)
                     return usuario

                 @router.delete('/{user_id}')
                 def eliminar_usuario(user_id:int, db:Session = Depends(get_db)):
                     response = user.eliminar_usuario(user_id, db)
                     return response

                 #Acutalizar
                 @router.patch('/{user_id}')
                 def actualizazr_usuario(user_id:int, updateUser:UpdateUser, db:Session = Depends(get_db)):
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

e) Dentro de schemas.py armamos los modelos para mostrar y guardar la informacion de la base de datos 
- por ejemplo:
    <pre><code>
    from datetime import datetime
    from pydantic import BaseModel
    from typing import Optional

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

1.  En la raiz del programa creo un archivo .env

    a) Dentro del archivo .env coloco las variables de entorno de la siguiente manera - Por ejemplo
    POSTGRES_DB = postgres
    POSTGRES_USER = postgres
    POSTGRES_PASSWORD=admin
    POSTGRES_SERVER=localhost
    POSTGRES_PORT=5432

2.  Dentro de la carpeta core tenemos el archivo \__init_.py, config.py
   
    a) Dentro del archivo config.py - Dentro de este archivo configuramos los settings para configurar la base de datos
    - Por ejemplo:
    <pre><code>
    import os
    from dotenv import load_dotenv
    from pathlib import Path

                #Lo primero que debemos hacer es ubicar donde esta nuestro .env
                env_path = Path('.') / '.env' # Esto lo que hace es volver una carpeta atras donde esta el archivo .env
                load_dotenv(dotenv_path=env_path) # Cargamos el archivo de .env a travez del env_path

                # Creamos la clase que contiene todas las constantes con la informacion requerida para conectarse y operar con la base de datos
                class Settings:
                    PROJECT_NAME:str = "PROYECTO-FAST-API"
                    PROJECT_VERSION:str = "1.0"
                    POSTGRES_USER:str = os.getenv('POSTGRES_USER')
                    POSTGRES_DB:str = os.getenv('POSTGRES_DB')
                    POSTGRES_PASSWORD:str = os.getenv('POSTGRES_PASSWORD')
                    POSTGRES_SERVER:str = os.getenv('POSTGRES_SERVER')
                    POSTGRES_PORT:str = os.getenv('POSTGRES_PORT')
                    DATABASE_URL = f"postgresql://{POSTGRES_DB}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

                # Guardamos una instancia de la clase settings en una variable para luego importarla en otro modulo para ser usuada
                settings = Settings()

Notas:

- Cada vez que queramos ejecutar el programa python main.py en la raiz del programa
- Cada vez que queramos instalar un modulo o libreria nueva pip install -r requirements.txt

### Como integrar alembic a nuestro proyecto

Esta es una libreria para poder realizar migraciones a nuestra base de datos, es decir que es una libreria que nos va a permitir realizar actualizaciones a las estructuras de la base de datos a medidas que estamos programando y con el servidor arriba.

-> Lo primero que debemos hacer es colocar alembic dentro del requirements.txt, seguidamente ejecutamos el pip install -r requirements.txt para instalar esta nueva libreria

-> Seguido a esto lo que hacemos es ejecutar en la raiz del proyecto el sigueinte comando, alembic init migrations, esto lo que hara es crear un archivo alembic.ini y una carpeta migrations con un archivo env.py y otra carpeta llamada versions.

Dentro del archivo alembic.ini nos vamos a encontrar con con una linea como la siguiente sqlalchemy.url = driver://user:pass@localhost/dbname, esta linea es la que la tenemos que editar con la informacion de nuestra base de datos, pero como el archivo alembic es un archivo .ini no se pueden realizar importaciones para poderla editar, para esto vamos a proseguir con el siguiente paso que es realizar las modificaciones desde el archivo env.py dentro de la carpeta migrations, pero antes debemos eliminar lo que tenga la variable sqlalchemy.url del archivo alembic.ini para dejarlo de la sigueinte manera sqlalchemy.url = , ya que luego vamos a acceder a esta variable y la vamos a modificar.

-> Dentro del archivo env.py agregamos las lineas siguientes
from core.config import settings
Asi como arriba accedemos a config ahora podemos acceder a config de arriba y a set main option para editar un variable de las que contiene, como primer parametro le colocamos el nombre de la variable a editar, seguidamente le pasamos el valor de config settings que contiene la direccion de la url nuestra para realizar la edicion de la misma **(antes deberiamos haber importado from core.config import settings)**

* config.set_main_option('sqlalchemy.url',settings.DATABASE_URL)

-> Otra configuracion que necesitamos es que reconoza los modelos que tenemos en nuestra app en db , models, esto es para que luego se pueda realizar las migraciones, para esto comentamos en el archivo env.py, la siguiente linea **target_metadata = None**, y descomentamos las dos lineas siguientes que se encuentra arriba
~~~
from myapp import mymodel
target_metadata = mymodel.Base.metadata,
~~~
y debemos modificar estas lineas para que nos quede
~~~
from app.db.models import Base
target_metadata = Base.metadata
~~~
Basicamente lo que hacemos es indicarle donde se encuentran los modelos de nuestra app para la base de datos en este caso en models Base, entonces esto lo que va a hacer es encargarse de reconocer los modelos y si aestos tienen algun cambio entonces hara sus respectiva migracion.

Luego de esto debemos irnos al archivo main.py y eliminar las lineas que creaban todas las tablas es decir las siguientes lineas.
~~~
def crearTablas(): # Creamos la tabla con el o los modelos que se tienen en base por esto es tan iomportante que los modelos hereden de Base a la hora de declararlos en database.py y luego le indicamos con create_all y bind el engine
Base.metadata.create_all(bind=engine)
crearTablas()
~~~
Como podemos observar la linea de arriba **Base.metadata.create_all(bind=engine)**, es la misma que usamos en **target_metadata = Base.metadata**, con la diferencia que en el archiv main creabamos todas las tablas y aca solamente usamos metadata para que reconozca cambios en models base para migrar a la base de datos automaticamente, pero con esto no acaba aqui ahora solo nos falta un paso mas.

Se deben ejecutar los siguientes comandos para que las migraciones se lleven a cabo:
~~~
- alembic revision --autogenerate -m "Nombre de la revision como sifura un comit aqui"
~~~
Esto nos creara un atabla en la base de datos llamada alembic_version en la cual se van a guardar las versiones que vamos teneindo segun las modificaciones que realizamos, tambien nos va a generar un archivo en la carpeta de versions en el cual se tiene la informacion de las mograciones de las tablas hechas.

Hasta este punto solamente se ha creado la tabla de versiones en la base de adtos y la informacion del archivo .py de versions con la informacion de las migraciones a realizar, seguidamente lo que hace falta es realizar esas migraciones con el siguiente comando para que se vea reflejados los cambios en la base de datos.
~~~
- alembic upgrade heads
~~~
Con esto seria todo, ahora con solo relizar una modificacion en los models dentro de la carpeta db y luego ejecutando estos dos comandos, primero alembic revision.. y luego alembic upgrade.. solamente con esto ya tenemos actualizada nuestra base de datos con los cambios que le hayamos hecho a los modelos por mas pequeños que sean. Hay que recordar colcoar el mensaje cuando ejecutemos la primer linea para identificar en la revision o version que fue lo que se modifico en la base de datos y asi llevar un mejor registro de los cambios que esta valla sufriendo a lo largo del tiempo. Esto es como relaizar un commit de git. Todo esto nos va a servir para mantener una consistencia en los datos.
___
Nota: Si agregamos una nueva columna sin indicar valor por default de esta, la creacion automatica de la nueva columna por defecto la tomara como null en la base de datos
___
### Excepciones HTTP y status codes (aplicados a nuestro codigo)

Para conocer mas de los codigos de estado podemos ver la pagina (https://umbraco.com/knowledge-base/http-status-codes), aqui tendremos una lista de todos los codigos de http que podemos tener y de su significado.

Para comenzar lo primero que tenemos que hacer es importar desde fastApi status. Luego lo que debemos hacer en donde colocamos la ruta debemos colocar un parametro llamado **status_code=numeroCodigo**, esto lo hacemos dentro de routers en donde tengamos los endpoints de nuestra app 
- Ejemplo
~~~
@router.get('/', response_model=List[ShowUser], status_code=status.HTTP_200_OK)
~~~
Como podemos ver colocamos en el parametro status code con la ayuda de status y la variable que contiene el codigo un codigo de error o aceptacion o rechazo segun sea el caso de cada uno, pero debemos tener en cuenta que esto que estamos haciendo en la seccion de la ruta con el parametro status code es para el caso de que todo salga bien con la peticion dentro del endpoint, en caso de que algo salga mal hacemos lo siguiente:

-> Dentro del archivo en la carpeta **repository** llamado **user.py** que contiene todas las clases con la informacion de creacion eliminacion etc para nuestros endpoint debemos realizar las siguientes modificaciones 

- Ejemplo:
~~~
#Primero traemos las librerias que vamosa usar para mostrar los errores de http

from fastapi import HTTPException, status

        # Agregamos un try catch para capturar la excepcion o error de la peticion y motrar el correspondiente mensaje
        CREAR USUARIO
        def crear_usuario(usuario:User, db:Session):
            #decimos que tiene la estructura del la clase user
            try:
                usuario = usuario.dict()
                nuevo_usuario = models.User(
                    username = usuario['username'],
                    password = usuario['password'],
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
~~~
Luego hacemos lo mismo con las demas funciones apra cada operacion de los end points
~~~
            OBTENER USUARIO
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

            ELIMINAR USUARIO
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

            ACTUALIZAR USUARIO
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
~~~
Y asi podemos realizar respuestas http tanto si las operaciones se realizan correctamente como si no lo hacen

## Colocacion de hash a nuestras contraseñas

1. Primero lo que tenemos que hacer es agregar al requirements.txt **passlib[bcrypt]** y ejecutar el requirement.txt para instalar la libreria

2. Luego en el archivo user.py deentro de repository agregamos las sigueintes lineas
~~~
   from passlib.context import CryptContext
   pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
~~~
*   Con esto lo que hacemos es crear el objeto con el cual vamos ahora a hashear la contraseña

Para hashear la contraseña solo basta con hacer lo siguiente, en la funcion del archivo user.py donde creamos el susuario colocamos lo sigueinte 
- Ejemplo:
~~~
def crear_usuario(usuario:User, db:Session): # Agregamos un try catch para capturar la excepcion o error de la peticion y motrar el correspondiente mensaje
try:
#decimos que tiene la estructura del la clase user
usuario = usuario.dict()
REALIZAMOS LA ENCRIPTACION DE LA CONTRASEÑA CON LO QUE LE PASMOS EN EL JSON DE ENTRADA
password_hash = pwd_context.hash(usuario['password'])
nuevo_usuario = models.User(
username = usuario['username'],
PASAMOS LA VARIABLE CON LA CONSTRASEÑA HASHEADA AL PARAMETRO PASSWORD PARA QUE SE GUARDE EL HASH EN LA BASE DE DATOS
password = password_hash,
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
raise HTTPException( # Pasamos el status code
status_code=status.HTTP_409_CONFLICT, # Le pasamos el detalle del error con un mensaje e imprimimos la e que contiene el error en si
detail = f"Error creando usuario {e}"
)
~~~
Ahora lo que hacemos a continuacion es mover la encriptacion a un archivo especifico que se encaraga de todo lo referido al hash de contraseña para esto realizamos las modificaciones sigueintes
1) en el archivo hashing.py luego de crearlo en la ruta de la carpeta app, dentro de este colocamos las sigueintes lineas
    - Ejemplo:
    ~~~
            from passlib.context import CryptContext

            pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

            class Hash:

                # Metodo para encriptar la contraseña
                def hash_password(password):
                    # Devolvemos la contraseña ya hasheada
                    return pwd_context.hash(password)
    ~~~
2)  Luego lo que hacemos es modificar en repository la creacion del usuario para que use esta clase creada para la encriptacion de la sigueinte manera
    - Ejemplo:
        ~~~
            from app.hashing import Hash

            def crear_usuario(usuario:User, db:Session):
                # Agregamos un try catch para capturar la excepcion o error de la peticion y motrar el correspondiente mensaje
                try:
                #decimos que tiene la estructura del la clase user
                    usuario = usuario.dict()
                    nuevo_usuario = models.User(
                        username = usuario['username'],
                        DIRECTAMENTE LLAMAMOS A LA CLASE HASH Y AL METODO HASH PASSWORD QUE CREAMOS AL CUAL LE PASAMOS EL PASSWORD OBTENIDO DEL MODELO ENVIADO POR ELE USUARIO Y ESTE METODO SE ENCARGA DE ENCRIPTAR LA CONTRASEÑA Y DEVOLVERLA
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
        ~~~
## Verificacion de la contraseña

1.  Lo primero que hacemos es crear un archivo auth.py dentro de la carpeta de routes
2.  Dentro de auth lo que hacemos primero que nada es colocar las lineas de armado de a ruta principal e importamos las librerias
    ~~~
    from fastapi import APIRouter, Depends, status
    from typing import List
    from sqlalchemy.orm import Session

    Definimos nuestro router

    router = APIRouter(
    prefix = "/login",
    tags = ["Login"]
    )
    ~~~
3.  Seguidamente declaramos o agregamos a nuestra app este nuevo router auth creado, para esto nos vamos al archivo main.py y agregamos lo siguiente
    #### IMPORTAMOS AUTH DE ROUTER Y LO AGREGAMOS A LA APP
    ~~~
    from app.routers import auth
    app.include_router(auth.router)
    ~~~
4.  Creamos un login model dentro del archivo schemas dentro de la carpeta app

    - EJemplo
      ~~~
      #CLase modelo para la informacion que enviamos del login

      class Login(BaseModel):
      username:str
      password:str
      ~~~
5.  Creamos dentro del archivo hashing.py un nuevo metodo dentro de la clase Hash que sirva apra verificar la contraseña
    - Ejemplo: 
    ~~~
    # Creamos el metodo que se va a encargar de verificar la contraseña, el mismo recibe el password de la base de datos en forma de hash y el password de el usuario que envio el cual no esta encriptado y servira pra verificar si es igual al encriptado o no, plain_password es el password que recibe del usuario, hashed_password es el password que recibe de la base de datos
    def verify_password(plain_password, hashed_password): # Retornamos lo que nos devuelve el metodo verify de el objeto pwd_context al cual le pasamos segundo la contraseña encriptada de la base de datos y primero le pasamos el password que nos envia el usuario y este metodo se encarga de verificar si coinciden o no devolviendonos el resultado, Si conincide nos devuelve True y en caso contrario False
    return pwd_context.verify(plain_password, hashed_password)
    ~~~
6.  Creamos el filtro para saber si el usuario existe para esto creamos un archivo auth.py dentro de la carpeta repository

    - Ejemplo:
      ~~~
      from pyexpat import model
      from sqlalchemy.orm import Session
      from app.db import models
      from fastapi import HTTPException, status
      from app.hashing import Hash

      # Creamos la funcion que se va a encargar de filtrar los usuarios

      def auth_user(usuario, db:Session): # Convertimos a diccionario el modelo recibido
      usuario = usuario.dict() # Filtramos de la base de datos aquellos que coincida el username de la base de datos con lo que trae el modelo y con first nos devuelve el primero que encuentra
      user = db.query(models.User).filter(models.User.username == usuario['username']).first()
      if not user: # Si no existe usuario con el username indicado entonces lanzamos el error o exception
      raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f"No existe el usuario indicado {usuario['username']} por lo tanto no se realiza el login"
      )

            if not Hash.verify_password(usuario['password'], models.User.password):
                # Si las contraseñas de la base de datos no coinciden entonces enviamos la excepcion
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Contraseña incorrecta"
                )
        ~~~
7.  Por ultimo lo que hacemos es generar el endpoint del login dentro del archivo auth.py dentro de la carpeta routes
    - Ejemplo: 
    ~~~
    # En este caso como response model devolvemos una lista de showuser ya que este endpoint devuelve una lista de valores
    @router.post('/', status_code=status.HTTP_200_OK) # Le indicamos que la session va a ser igual a lo que devuelva get_db que es en realidad la sesion de la bse de datos
    def login(usuario:Login,db:Session = Depends(get_db)):
    LLAMAMOS A AUTH_USER QUE ES EL FILTRO PARA VERIFICAR SI EXISTE EL USUARIO Y LA CONTRASEÑA SI ES ASI ENTONCES DEVUELVE EL LOGIN CONRRECTO, SI NO SALTARA EL RISE DENTRO DE AUTH_USER DEL ERROR OCACIONADO
    auth.auth_user(usuario, db)
    return {'respuesta':'login aceptado'}
    ~~~
## Implementacion de JWT

1. PRimero lo que hacemos es agegar al requirements.txt la libreria **python-jose[cryptography]**, y seguido a esto ejecutamos __pip install -r requirements.txt__

2. Luego creamos un nuevo archivo llamado token.py dentro de app el cual contendra la informacion y seteos para la generacion correcta del jwt

- Ejemplo:
  ~~~
  from jose import JWTError, jwt

  SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
  ALGORITHM = "HS256"
  ACCESS_TOKEN_EXPIRE_MINUTES = 30

  Esta funcion recibe un diccionario en caso de que queramos encriptar data directamente en jwt por eso lo primero que recibe es un diccionario con la informacion del usuario

  def create_access_token(data: dict): # Realiza un acopia de la data que enviamos para encriptar
  to_encode = data.copy()
  #Le indicamos que el tiempo de expiracion es de los minutos seteados al comienzo
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Añadimos al diccionario copiado una nueva llave que es exp el cual contiene el tiempo de expiracion del token
  to_encode.update({"exp": expire}) # Luego genera el jwt con el metodo encode de jwt, pasandole primero el diccionario con la informacion a codificar, la secretKey y el algoritmo que se va a utilizar HS256 en este caso
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # Por ultimo devuelve el jwt
  return encoded_jwt
  ~~~
1.  Creamos la sigueinte clase dentro de schemas.py dentro de la carpeta app
    -Ejemplo:  
    ~~~
     from typing import Union

    # Modelos para el token

    class Token(BaseModel):
    access_token:str
    token_type:str

    class Tokendata(BaseModel):
    username: Union[str,None] = None
    ~~~
2.  Realizamos luego de las verificaciones del usuario y contraseña la crecion del token con la informacion del usuario para reotnar y enviar esto lo hacemos es la funcion auth_user dentro de auth.py en la carpeta repository

    - Ejemplo:
      ~~~
      from pyexpat import model
      from sqlalchemy.orm import Session
      from app.db import models
      from fastapi import HTTPException, status
      from app.hashing import Hash
      from app.token import create_access_token

        # Creamos la funcion que se va a encargar de filtrar los usuarios

        def auth_user(usuario, db:Session): # Convertimos a diccionario el modelo recibido
        usuario = usuario.dict() # Filtramos de la base de datos aquellos que coincida el username de la base de datos con lo que trae el modelo y con first nos devuelve el primero que encuentra
        user = db.query(models.User).filter(models.User.username == usuario['username']).first()
        if not user: # Si no existe usuario con el username indicado entonces lanzamos el error o exception
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe el usuario indicado {usuario['username']} por lo tanto no se realiza el login"
        )

            # Le pasamos el password que le enviamos y el user.password es lo que traemos de la base de datos
            if not Hash.verify_password(usuario['password'], user.password):
                # Si las contraseñas de la base de datos no coinciden entonces enviamos la excepcion
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Contraseña incorrecta"
                )

            LUEGO Y SOLO SI PASO LOANTERIOR SE EJECUTA LA SECCION ESTA QUE ES LA CREACION Y RETORNO DEL TOKEN CON LA INFORAMCION DE USUARIO

            # Si llegamos hasta aqui quiere decir que se ha verificado que la contraseña y el usuario coinciden
            # Ahora usamos el jwt
            # Creamos la variable con la inforamcion del usuario pero en forma ded token
            access_token = create_access_token(
                data={"sub": user.username}
            )
            # Retorna mos el token de acceso y el tipo de token que sera bearer
            return {"access_token": access_token, "token_type": "bearer"}
        ~~~
3.  Por ultimo hacemos el retorno en el endpont, en el archivo auth.py dentro de la carpeta routers
    - Ejemplo
      ~~~
      # En este caso como response model devolvemos una lista de showuser ya que este endpoint devuelve una lista de valores
      
      @router.post('/', status_code=status.HTTP_200_OK)
      
      # Le indicamos que la session va a ser igual a lo que devuelva get_db que es en realidad la sesion de la bse de datos
      
      def login(usuario:Login,db:Session = Depends(get_db)):
      SE RECIBE EL TOKEN CON LA INFROMACION Y FINALMENTE SE RETORNA PARA MOSTRARLO # REcibimos la informacion de autenticacion
      
      auth_token = auth.auth_user(usuario, db) # Retornamos la informacion de autenticacion
      
      return auth_token
      ~~~
## Proteccion de rutas

1.  Primero lo que tenemos que hacer es añadir el depends y el current user a las rutas protegidas, pero a su vez este current_user lo que hace es llamar a la funcion cone ste mismo nombre que recibe el token y lo que hace es validar presisamente si el token es valido o no. Para todo esto creamos primero en app un nuevo archivo oauth.py

2.  Dentro de este lo que hacemos es crear la siguiente funcion get current user
    - Ejemplo:
    ~~~
    from fastapi import Depends, HTTPException, status
    from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
    from app.token import verify_token

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
    ~~~
3.  en token.py creamos una nueva funcion llamada verify_token y lo que hace basicamente es veridicar el token
    - Ejemplo: 
    ~~~
    # Importamos el schema
    from app.schemas import Tokendata # Funcion encargada de verificar el token
    def verify_token(token:str, credentials_exception):
    try: # Esto lo que hace es decodigficar el token , le pasa la secret key declarada y el algoritmo de cifrado
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # En la llave sub habiamos colocado el username por lo cual con get y la llave sub obtenemos el username
    username: str = payload.get("sub")
    if username is None: # Si no existe el username es por que la llave no existe y el usuario no esta autenticado y devuelve un credential exeption que se recibe de parametro
    raise credentials_exception # Luego de esto mediante el Token data del modelo que habiamos generado en schemas devovlemos un username, el username sera el usernname del modelo por eso es username=username
    token_data = Tokendata(username=username)
    except JWTError: # En caso de que ocurra cualquier otra cosa se envia este error que es el declarado en oauth con el 401 no autorizado
    raise credentials_exception
    ~~~
4.  Ahora lo que hacemos es validar el current user para saber si tiene los permisos para esto en la ruta le pasamos **current_user: User = Depends(get_current_user)**

Esto quiere decir que current_user va a ser un modelo USer y depende de get_current_user

Entonces ahora si queremos proteger una ruta lo que hacemos es colocar la linea de arriba
- Ejemplo

        def crear_usuario(usuario:User, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
        agregamos current user y asi para cada uno de los endpint dentro de routes user.py
---        
Nota: modificaciones

-> auth.py de repository

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

-> en auth.py de routers

    # En este caso como response model devolvemos una lista de showuser ya que este endpoint devuelve una lista de valores
    @router.post('/', status_code=status.HTTP_200_OK)
    # Le indicamos que la session va a ser igual a lo que devuelva get_db que es en realidad la sesion de la bse de datos
    # Le decimos que el usuario seria de tipo OAuth2PasswordRequestForm y le colocamos un igual a Depends() esto es por que la inforamcion de inicio de sesion se tomara del formulario de autenticacion de OAuth y vendra en formato este por lo cual en auth.py de repository ahora en vez de usar usuario['password'] por ejemplo debemos usar usuario.password con notacion del punto y ya no es necesario convertir la inforamcion a diccionario de python para trabajar con esta
    def login(usuario:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
        # REcibimos la informacion de autenticacion
        auth_token = auth.auth_user(usuario, db)
        # Retornamos la informacion de autenticacion
        return auth_token

    La infromacion de JWT la podemos conseguir en los siguientes links
    https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/
    https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
----
## Realizacion de tests para creacion de usuarios

Los test los realizaremos con pytest, este lo que hace al ejecutarlo en consola es irse a la carpeta llamada test y buscar los archivos que comiencen con la parabra test, y luego ejecuta todas las funciones que comincen por test

1) Creamos una carpeta en la raiz del programa llamada test, luego creamos un archivo llamado test_api.py por ejemplo
2) Colocamos en el requirements.txt pytest que es la libreria de python para hacer test, y ademas el modulo requests para que pytest pueda realizar las peticiones, luego instalamos con pip install -r requirements.txt
3) Creamos los test dentro del archivo test_api.py, lo hacemos de la sigueinte manera
   
   - Ejemplo:
        ~~~
        # Este testclient lo que hara es hacer una peticion de tipo request por ejemplo a la api y esta nos devuelve un si o un no
        from fastapi.testclient import TestClient
        # Traemos sys y os para poder tomar con os la ruta raiz y con sys agregarla al path para poder usarla
        import sys
        import os

        # Ahora lo que hacemos es agregar una ruta al archivo esto es para que poueda encontrar el main, si no lo colocamos entonces no lo encontrara ya que lo buscara en la ruta actual y el main esta en la raiz del programa 
        sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
        # Luego declaramos un cliente y le pasamos nuestra aplicacion app, para eso importamos nuestra app desde main
        from main import app
        cliente = TestClient(app)


        # Ejecutamos nuestro primer caso de prueba
        def test_crear_usuario():
            # Creamos la informacion que le vamos a enviar a la paticion
            usuario = {
                        "username": "pablito",
                        "password": "123",
                        "nombre": "pablo",
                        "apellido": "martinez",
                        "direccion": "string",
                        "telefono": 0,
                        "correo": "pablito@gmail.com",
                        "creacion": "2022-07-04T08:52:05.083577"
                    }
            # Creamos una variable response que contendra la peticion en este caso de tipo post la misma lleva la ruta y el json con la infrmacion de la peticion para que pase esta info a la api y esta la interprete
            response = cliente.post('/user/', json=usuario)

            # Mediante assert le decimos que el status code tiene que ser igual a 201 si es correcta la peticion si no es asi se envia un error
            assert response.status_code == 201

            # Imprimimos lo que trae response, con dir(response) imprimimos tots los metodo que tiene este response, y por ultimo el status code de response
            # print(response, dir(response), "status: ", response.status_code)
            # Con el metodo json() lo que hacemos es traer la informacion que devuelve la peticion en forma de json
            # print(response.json())

            # PAra ser mas especifico podemos decir con un assert que lo que nos devuelva en la llave respuesta del json debera ser lo que nosotros le hayamos colocado como mensaje de respuesta por ejemplo
            assert response.json()['respuesta'] == 'Usuario creado correctamente'
    ~~~

Al ejecutar pytest en consola este busca la carpeta que diga test y luego los archivos que comiencen con test, seguidamente las funciones y si pasa estas dira que estas pasan si no estas diran que no pasan los test.

Nota: Si queremos ejecutar pytest y queremos mostrar los print dentro tenemos que colocar **pytest -s**

4) Creamos un archivo en la raiz llamado prueba.py
5) Colocamos la configuracion para crear una base de datos sqlite3 especial para realizar las pruebas de nuestro test y asi no modificar la base de datos de produccion con los tests, para esto agregamos en nuestro archivo test_api las lineas siguientes 

    ~~~
    # Este testclient lo que hara es hacer una peticion de tipo request por ejemplo a la api y esta nos devuelve un si o un no
    from fastapi.testclient import TestClient
    # Traemos sys y os para poder tomar con os la ruta raiz y con sys agregarla al path para poder usarla
    import sys
    import os
    from psycopg2 import connect
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Ahora lo que hacemos es agregar una ruta al archivo esto es para que poueda encontrar el main, si no lo colocamos entonces no lo encontrara ya que lo buscara en la ruta actual y el main esta en la raiz del programa 
    sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
    # Luego declaramos un cliente y le pasamos nuestra aplicacion app, para eso importamos nuestra app desde main
    from main import app
    ------------------------------------------------
    # Importamos Base de models para tener losmodelos de las base de datos
    from app.db.models import Base

    # Creamos el path que contiene el archivo test.db, es decir mediante join unimos el directorio actual con test.db, asi como hicimos arriba con el directorio raiz
    db_path = os.path.join(os.path.dirname(__file__),'test.db')
    # Ahroa creamos el archivo de sqlite
    db_uri = "sqlite:///{}".format(db_path)
    # Con todo esto de arriba le decimos que la ruta de sqlite sera la definida arriba con el nombre de la base de datos

    # Declaramos la constante que contendra la url dela base de datos
    SQLALCHEMY_DATABASE_URL = db_uri

    # Ahora lo que hacemos es crear nuestro engine mediante create_engine el cual recibe la url de la base de datos y una serie de argumentos en en nuestro caso le enviamos uno y en valor False
    engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
    # Declaramos un objeto de tipo sessionmamaker
    TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
    # Ahora con los modelos de Base creamos todas las tablas de nuestra base de datos, pasandole a create_all en bind el engine test
    Base.metadata.create_all(bind=engine_test)
    -----------------------------------------
    cliente = TestClient(app)


    # Ejecutamos nuestro primer caso de prueba
    def test_crear_usuario():
        # Creamos la informacion que le vamos a enviar a la paticion
        usuario = {
                    "username": "pablito",
                    "password": "123",
                    "nombre": "pablo",
                    "apellido": "martinez",
                    "direccion": "string",
                    "telefono": 0,
                    "correo": "pablito@gmail.com",
                    "creacion": "2022-07-04T08:52:05.083577"
                }
        # Creamos una variable response que contendra la peticion en este caso de tipo post la misma lleva la ruta y el json con la infrmacion de la peticion para que pase esta info a la api y esta la interprete
        # response = cliente.post('/user/', json=usuario)

        # Mediante assert le decimos que el status code tiene que ser igual a 201 si es correcta la peticion si no es asi se envia un error
        # assert response.status_code == 201

        # Imprimimos lo que trae response, con dir(response) imprimimos tots los metodo que tiene este response, y por ultimo el status code de response
        # print(response, dir(response), "status: ", response.status_code)
        # Con el metodo json() lo que hacemos es traer la informacion que devuelve la peticion en forma de json
        # print(response.json())

        # PAra ser mas especifico podemos decir con un assert que lo que nos devuelva en la llave respuesta del json debera ser lo que nosotros le hayamos colocado como mensaje de respuesta por ejemplo
        # assert response.json()['respuesta'] == 'Usuario creado correctamente'
    ~~~
6) Ahora lo que haremos es crear las pruebas primero creando una nueva fucnion insertar usuario prueba que lo que hara es ejecutar una consulta sql, y luego otra funcion test_delete_database que lo que hara es una vez realizados los test borra la base de datos
    - Ejemplo
        ~~~
        # Este testclient lo que hara es hacer una peticion de tipo request por ejemplo a la api y esta nos devuelve un si o un no
        from fastapi.testclient import TestClient
        # Traemos sys y os para poder tomar con os la ruta raiz y con sys agregarla al path para poder usarla
        import sys
        import os
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        # Ahora lo que hacemos es agregar una ruta al archivo esto es para que poueda encontrar el main, si no lo colocamos entonces no lo encontrara ya que lo buscara en la ruta actual y el main esta en la raiz del programa 
        sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
        # Luego declaramos un cliente y le pasamos nuestra aplicacion app, para eso importamos nuestra app desde main
        from main import app
        # Importamos Base de models para tener losmodelos de las base de datos
        from app.db.models import Base
        # Traemos la clase Hash para realizar el hasheado de la contraseña
        from app.hashing import Hash
        from app.db.database import get_db

        # Creamos el path que contiene el archivo test.db, es decir mediante join unimos el directorio actual con test.db, asi como hicimos arriba con el directorio raiz
        db_path = os.path.join(os.path.dirname(__file__),'test.db')
        # Ahroa creamos el archivo de sqlite
        db_uri = "sqlite:///{}".format(db_path)
        # Con todo esto de arriba le decimos que la ruta de sqlite sera la definida arriba con el nombre de la base de datos

        # Declaramos la constante que contendra la url dela base de datos
        SQLALCHEMY_DATABASE_URL = db_uri

        # Ahora lo que hacemos es crear nuestro engine mediante create_engine el cual recibe la url de la base de datos y una serie de argumentos en en nuestro caso le enviamos uno y en valor False
        engine_test = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False})
        # Declaramos un objeto de tipo sessionmamaker
        TestingSessionLocal = sessionmaker(bind=engine_test, autocommit=False, autoflush=False)
        # Ahora con los modelos de Base creamos todas las tablas de nuestra base de datos, pasandole a create_all en bind el engine test
        Base.metadata.create_all(bind=engine_test)

        cliente = TestClient(app)

        def insertar_usuario_prueba():

            # hassheamos la constraseña y luego la pasamos hasheada en la query
            password_hash = Hash.hash_password('1234')    

            engine_test.execute(
                f"""
                    INSERT INTO user (username,password, nombre, apellido, direccion, telefono, correo)
                    VALUES
                    ('santi','{password_hash}','santiago','martinez','pichincha 23','2314124','santi@gmail.com')
                """
            )
        insertar_usuario_prueba()

        def override_get_db():
            db = TestingSessionLocal()
            try:
                #Devuelve un objeto de tipo session maker
                yield db
            finally:
                db.close()

        # Ahora lo que debemos hacer es hacer override de get_db que esta en database con esta funcion nueva de aca acciba, para eso debemos hacer lo sigueinte. Lo que hacemos es reemplazar la conexion de nuestra base de datos por la conexion esta overrride get db 
        app.dependency_overrides[get_db] = override_get_db
        # Igualamos lo que tiene get_db con lo la nueva funcion que declaramos arriba override_get_db


        # Ejecutamos nuestro primer caso de prueba
        def test_crear_usuario():
            # Creamos la informacion que le vamos a enviar a la paticion
            usuario = {
                        "username": "pablito",
                        "password": "123",
                        "nombre": "pablo",
                        "apellido": "martinez",
                        "direccion": "string",
                        "telefono": 0,
                        "correo": "pablito@gmail.com",
                        "creacion": "2022-07-04T08:52:05.083577"
                    }
            # Creamos una variable response que contendra la peticion en este caso de tipo post la misma lleva la ruta y el json con la infrmacion de la peticion para que pase esta info a la api y esta la interprete
            response = cliente.post('/user/crear-usuario', json=usuario)
            # Mediante assert le decimos que el status code tiene que ser igual a 201 si es correcta la peticion si no es asi se envia un error
            assert response.status_code == 201

            # Imprimimos lo que trae response, con dir(response) imprimimos tots los metodo que tiene este response, y por ultimo el status code de response
            # print(response, dir(response), "status: ", response.status_code)
            # Con el metodo json() lo que hacemos es traer la informacion que devuelve la peticion en forma de json
            # print(response.json())

            # PAra ser mas especifico podemos decir con un assert que lo que nos devuelva en la llave respuesta del json debera ser lo que nosotros le hayamos colocado como mensaje de respuesta por ejemplo
            assert response.json()['respuesta'] == 'Usuario creado correctamente'

        def test_delete_database():
            # Obtenemos la ruta de la base de datos
            db_path = os.path.join(os.path.dirname(__file__),'test.db')
            # Mediante el metodo de os remode eliminamos la base de datos
            os.remove(db_path)
    ~~~
7) Ahora lo que debemos hacer a continuacion es colocar la parte de del test para las autenticaciones de usuario, para eso hacemos los sigueintes agregados en el archivo 
    - Ejemplo
        ~~~
        def test_obtener_usuario():
    
        response = cliente.get('/user/')
        assert response.status_code == 401

        # Armamos un diccionario con la informacion de inicio de sesion
        usuario = {
            "username":"pablito",
            "password":"123"
        }

        # Realizamos la peticion para hacer login pasandole en data la informacion del diccionario ususario para inicio de sesion
        response_token = cliente.post('/login/', data=usuario)
        # Validamos que el status code sea 200 ok, y que el token type que trae la variable response token sea bearer
        assert response_token.status_code == 200
        assert response_token.json()['token_type'] == 'bearer'
        # print(response_token.status_code, response_token.json()['token_type'])

        # Seteamos los headers para colocar el token para iniciar sesion 
        headers = {
            "Authorization":f"Bearer {response_token.json()['access_token']}"
        }

        # Hacemos la peticion get a user pero ahora enviandole los heaaders
        response = cliente.get('/user/', headers=headers)
        # Vemos lo que nos devuelve response que es la lista de usuarios
        # print(response.json())
        # Verificamos que devuelva un 200 ok 
        assert response_token.status_code == 200
        # Corroboramos que la longitud del json que creamos sea igual a 2 ya que son 2 los usuarios que se deben haber creado
        assert len(response_token.json()) == 2
        ~~~
8) Ahora veremos como implementar el test de obtener un usuario especifico, eliminar usuario y actualizar usuario
   - Ejemplo:
        ~~~
        def test_obtener_usuario():
        usuario = {
            "username":"pablito",
            "password":"123"
        }
        response_token = cliente.post('/login/', data=usuario)
        assert response_token.status_code == 200
        assert response_token.json()['token_type'] == 'bearer'
        headers = {
            "Authorization":f"Bearer {response_token.json()['access_token']}"
        }

        response1 = cliente.get('/user/1', headers=headers)
        assert response1.status_code == 200
        # Verificamos que el primer usuario tenga el username que le habiamos colocado santi
        assert response1.json()['username'] == 'santi'
        response2 = cliente.get('/user/2', headers=headers)
        # Verificamos que el segundo usuario tenga el username que le habiamos colocado pablito
        assert response2.json()['username'] == 'pablito'
        assert response2.status_code == 200

    def test_delete_user():
        usuario = {
            "username":"pablito",
            "password":"123"
        }
        response_token = cliente.post('/login/', data=usuario)
        assert response_token.status_code == 200
        assert response_token.json()['token_type'] == 'bearer'
        headers = {
            "Authorization":f"Bearer {response_token.json()['access_token']}"
        }

        # hacemos la peticion para eliminar el usuario 1 y luego el 2 que creamos
        response1 = cliente.delete('/user/1', headers=headers)
        # Verificamos en cada eliminacion que status code sea 200 ok y que la respuesta sea usuario eliminado correctamente para verificar que la prueba paso
        assert response1.status_code == 200
        assert response1.json()['respuesta'] == 'Usuario eliminado correctamente'

        # Verificamos que se haya eliminado haciendo una peticion get al usuario
        response_get1 = cliente.get('/user/1', headers=headers)
        assert response_get1.json()['detail'] == 'No existe el usuario con el id 1'
    
        # Eliminamos solo un usuario ya que no vamos a poder actualizar luego de esto nada por que no vemos a tener usuario en la base de datos

    def test_actualizar_usuario():
        usuario = {
            "username":"pablito",
            "password":"123"
        }
        response_token = cliente.post('/login/', data=usuario)
        assert response_token.status_code == 200
        assert response_token.json()['token_type'] == 'bearer'
        headers = {
            "Authorization":f"Bearer {response_token.json()['access_token']}"
        }

        # Solo vamos a actualizar el username nada mas
        usuario = {
                    "username": "hongitoPablito",
                }

        # Actualizamos el usuario 2 ya que no tenemos usuario 1 por que lo eliminamos en el test anterior
        response = cliente.patch('/user/2',json=usuario, headers=headers)
        # Corroboramos que en respuesta del json venga el mensaje de creado correctamente
        assert response.json()['respuesta'] == 'Usuario actualizado correctamente'

        # Ahora hacemos una peticion get al usuario para ver si ejectivamente se actualiza
        response_user = cliente.get('/user/2', headers=headers)
        # Verificamos que username valga loque le habiamos dicho que tenia que valer
        assert response_user.json()['username'] == 'hongitoPablito'
        # Y ademas el nombre deberia seguir siendo el mismo no tendria que haber cambiado por lo cual hacemos esa prueba
        assert response_user.json()['nombre'] == 'pablo'
        ~~~
9) Ahora veremos como implementar coverage.py en las pruebas, este lo que hara es ver que partes del codigo no se ejecutan y se deberian ejecutar, es decir veremos las partes que no hemos probado del codigo en los test convencionales como por ejemplo los mensaje de error en el caso de que un usuario no exista o se quiera eliminar un usuario que no existe o cuando no enviamos el token del jwt
   1)  Lo primero que debemos hacer es instalar coverage para esto lo agegamos como covergar en los requirements.txt y luego los ejecutamos como pip install -r requirements.txt
   2)  Luego lo que hacemos es correr el coverage con el comando coverage run -m pytest, esto nos va a generar un archivo .coverage pero que es un archivo que no podemos leer por eso lo que hacemos es lo sigueinte
   3)  Ejecutamos el comando coverage html para generar un archivo con los html y demas donde tenemos un index.html el cual ejecutamos y nos abre una tabla con los test que tenemos y el porcentaje de cobertura que hemos acaparado, marcandonos los test que nos faltarian en las partes del codigo que no han ejecutado, con lo cual nos fijamos y luego realizamos los test pertinentes hasta cubrir el 100% de las partes del codigo. Los test los hacemos de la misma manera que hemos venido haciendolo hasta ahora
    - Ejemplo:
        ~~~
        def test_no_encuentra_usuario():
        usuario = {
            "username":"hongitoPablito",
            "password":"123"
        }
        response_token = cliente.post('/login/', data=usuario)
        assert response_token.status_code == 200
        assert response_token.json()['token_type'] == 'bearer'
        headers = {
            "Authorization":f"Bearer {response_token.json()['access_token']}"
        }

        # Solo vamos a actualizar el username nada mas
        usuario = {
                    "username": "hongitoPablito",
                }
        # Colocamos un usuario que no existe para validar el mensaje de error
        response = cliente.patch('/user/12',json=usuario, headers=headers)
        assert response.json()['detail'] == 'No existe el usuario con el id 12 por lo tanto no se puede actualizar'

    def test_no_encuentra_usuario_eliminar():
        usuario = {
            "username":"hongitoPablito",
            "password":"123"
        }
        response_token = cliente.post('/login/', data=usuario)
        assert response_token.status_code == 200
        assert response_token.json()['token_type'] == 'bearer'
        headers = {
            "Authorization":f"Bearer {response_token.json()['access_token']}"
        }

        # Colocamos un usuario que no existe para validar el mensaje de error
        response = cliente.delete('/user/12', headers=headers)
        assert response.json()['detail'] == 'No existe el usuario con el id 12 por lo tanto no se elimina'
                    
    def test_error_crear_usuario():
        usuario = {
                    "username": "pablito",
                    "password": "123",
                    "nombre": "pablo",
                    "apellido": "martinez",
                    "direccion": "string",
                    "telefono": 0,
                    "correo": "pablito@gmail.com",
                    "creacion": "2022-07-04T08:52:05.083577"
                }
        # verificamos que al crear un usuario duplicado salte el error de conflicto
        response = cliente.post('/user/crear-usuario', json=usuario)
        assert response.status_code == 409
    ~~~
Ahora asi de esta manera nosotros hemos cubierto mas del 95% de las pruebas de codigo que es mas que suficiente para lanzar alo a produccion

## Subir proyecto a github

1) Lo primero que vamos a hacer es crear un git ignote para no incluir archivos basura en nuestro repositorio, para esto tenemos un archivo prearmado con los gitignores para copiar dentro de .gitignore
   ~~~
   # Byte-compiled / optimized / DLL files
    __pycache__/
    *.py[cod]
    *$py.class

    # C extensions
    *.so

    # Distribution / packaging
    .Python
    build/
    develop-eggs/
    dist/
    downloads/
    eggs/
    .eggs/
    lib/
    lib64/
    parts/
    sdist/
    var/
    wheels/
    share/python-wheels/
    *.egg-info/
    .installed.cfg
    *.egg
    MANIFEST

    # PyInstaller
    #  Usually these files are written by a python script from a template
    #  before PyInstaller builds the exe, so as to inject date/other infos into it.
    *.manifest
    *.spec

    # Installer logs
    pip-log.txt
    pip-delete-this-directory.txt

    # Unit test / coverage reports
    htmlcov/
    .tox/
    .nox/
    .coverage
    .coverage.*
    .cache
    nosetests.xml
    coverage.xml
    *.cover
    *.py,cover
    .hypothesis/
    .pytest_cache/
    cover/

    # Translations
    *.mo
    *.pot

    # Django stuff:
    *.log
    local_settings.py
    db.sqlite3
    db.sqlite3-journal

    # Flask stuff:
    instance/
    .webassets-cache

    # Scrapy stuff:
    .scrapy

    # Sphinx documentation
    docs/_build/

    # PyBuilder
    .pybuilder/
    target/

    # Jupyter Notebook
    .ipynb_checkpoints

    # IPython
    profile_default/
    ipython_config.py

    # pyenv
    #   For a library or package, you might want to ignore these files since the code is
    #   intended to run in multiple environments; otherwise, check them in:
    # .python-version

    # pipenv
    #   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
    #   However, in case of collaboration, if having platform-specific dependencies or dependencies
    #   having no cross-platform support, pipenv may install dependencies that don't work, or not
    #   install all needed dependencies.
    #Pipfile.lock

    # poetry
    #   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
    #   This is especially recommended for binary packages to ensure reproducibility, and is more
    #   commonly ignored for libraries.
    #   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
    #poetry.lock

    # pdm
    #   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
    #pdm.lock
    #   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
    #   in version control.
    #   https://pdm.fming.dev/#use-with-ide
    .pdm.toml

    # PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
    __pypackages__/

    # Celery stuff
    celerybeat-schedule
    celerybeat.pid

    # SageMath parsed files
    *.sage.py

    # Environments
    # .env
    .venv
    env/
    venv/
    ENV/
    env.bak/
    venv.bak/
    entorno/

    # Spyder project settings
    .spyderproject
    .spyproject

    # Rope project settings
    .ropeproject

    # mkdocs documentation
    /site

    # mypy
    .mypy_cache/
    .dmypy.json
    dmypy.json

    # Pyre type checker
    .pyre/

    # pytype static type analyzer
    .pytype/

    # Cython debug symbols
    cython_debug/

    # PyCharm
    #  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
    #  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
    #  and can be added to the global gitignore or merged into this file.  For a more nuclear
    #  option (not recommended) you can uncomment the following to ignore the entire idea folder.
    #.idea/
    ~~~
2) Ahora lo siguiente es iniciar git con el comando git init, seguido hascemos git add ., y a continuacion git commit -m "repositorio en git", a continuacion creamos un repo en hithub agregamos el git remote en el proyecto y hacemos push para subir todo a la nube

## Creamos base de datos en heroku psotgresql

1) Nos vamos a heroku verificamos que tengamos la cuanta si no la tenemos la creamos, luego inicamos sesion, verificamos que tengamos menos de 5 proyectos si no nos dejara crear mas, y finalmente creamos nueva app, le colocamos un nombre que no haya sido usado
2) Luego nos vamos a resourse y despues en la barra de busqueda poenmos heroku postgresql y la selseleccionamos, luego nos aparece una ventana seleccionamos el plan free y submit order para finalizar
3) Seguidamente debemos ver las credenciales de esta base de datos para usarlas en nuestra aplicacion, para esto le damos click a la aplicacion, una vez que se abre la ventana de la base de datos nos vamos a la pestaña de settings y luego ponemos en view en database credentials y aca vamos a tener algo como lo siguiente
   ~~~
        Host
        ec2-44-198-82-71.compute-1.amazonaws.com
        Database
        d3rvasl9224c30
        User
        qcrlviipwolmfv
        Port
        5432
        Password
        69013571b34f1be101ceec171ace4b5b33cf10425517f4f97b2d0c1287341e53
        URI
        postgres://qcrlviipwolmfv:69013571b34f1be101ceec171ace4b5b33cf10425517f4f97b2d0c1287341e53@ec2-44-198-82-71.compute-1.amazonaws.com:5432/d3rvasl9224c30
        Heroku CLI
        heroku pg:psql postgresql-polished-53757 --app fast-api-proyecto-udemy
    ~~~
4)  Luego de todo esto lo proximo es hacer la prueba de la base de datos con el gestor local para ver si esta funcionando para eso abrimos dbeaver y creamos una nueva conexion pasando los parametros antes vistos
5) Eliminamos la carpeta migrations y el archivo alembic.ini
6) Nos vamos al archivo .env y dentro de este comentamos las varaibles de entorno que tenemos y las copiamos a las comentadas le ponemos variables de entorno base de datos local y luego a las otras le colcoamos base de datos en heroku. A estas ultimas le ponemos las credenciales con los valores de heroku
7) Luego del paso anterior debemos realizar nuevamente las migraciones con el comando alembic init migrations por eso eliminamos los archivos de alembic.ini y la carpeta de migrations ya que ahora se deberan crear con los nuevos datos de las variables de entorno. Nota: Recordar tener siempre activado el entorno virtual venv/Sripts/avtivate
8) Nos vamos a alembic.ini y modificamos la linea de sqlalchemy.url dejandola vacia
9) Luego debemos copiar el siguiente codigo antes de la funcion run_migrations_offline
    ~~~
    from core.config import settings

    config = context.config
    config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    from app.db.models import Base
    target_metadata = Base.metadata
    ~~~
Este codigo de arriba ya fue explicado en los inicios del curso, Pero basicamanete loq ue hace es ir a core setting y traer todas las settings y con el database url nos busca en el alembic ini y colocarle la database_url y por ultimo lo que hara es crear todos los modelos de las tablas

10) Luego ejecutamos las migraciones con los comandos alembic revision --autogenerate -m "crear modelos", y luego ejecutamos otro comando alembic upgrade heads. Para finalizar hacemos add, commit y push del proyecto en github

## Despliegue de la app en heroku
1) Descargamos heroku CLI
2) probamos si tenemos heroku con el comando heroku en la terminal, nos tiene que aparecer un listado de acciones a realizar eso queire decir que lo tenemos instalado
3) Ejecutamos el comando heroku login, presionamos cualquier tecla menos la q y se nos abre el navegador para iniciar sesion en heroku luego cerramos y ya estamos dentro
4) Creamos un archivo Procfile, este es un archivo que interpreta heroku
5) Comentamos las lineas siguientes en el main.py 
   ~~~
   if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
   ~~~
6) Seguidamente en el Proc file colocamos las siguientes lineas
    ~~~
    Colocamos web luego el servidor en este caso uvicorn, luego el main donde esta la app, seguido el host 0.0.0.0 que quiere decir que se pueden recibir peticiones de cualquier lugar, seguido le pasamos el puerto pero como heroku le envia el mismo en forma de variable de entorno entonces la tenemos que poner como tal en el apartado de port
    
    web: uvicorn main:app --host:0.0.0.0 --port=${POST:-5000}

    Esta linea de aca arriba es lo mismo que haciamos en el main con el if __name__ ... etc

    ~~~
7) Seguido a esto guardamos todo y hacemos add ., commit, y push a github