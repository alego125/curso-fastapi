# Este testclient lo que hara es hacer una peticion de tipo request por ejemplo a la api y esta nos devuelve un si o un no
from email import header
from urllib import response
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

def test_obtener_usuarios():
    
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
    

def test_delete_database():
    # Obtenemos la ruta de la base de datos
    db_path = os.path.join(os.path.dirname(__file__),'test.db')
    # Mediante el metodo de os remode eliminamos la base de datos
    os.remove(db_path)