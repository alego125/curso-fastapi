from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.schemas import Tokendata

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Esta funcion recibe un diccionario en caso de que queramos encriptar data directamente en jwt por eso lo primero que recibe es un diccionario con la informacion del usuario

def create_access_token(data: dict):
    # Realiza un acopia de la data que enviamos para encriptar
    to_encode = data.copy()
    #Le indicamos que el tiempo de expiracion es de los minutos seteados al comienzo
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Añadimos al diccionario copiado una nueva llave que es exp el cual contiene el tiempo de expiracion del token
    to_encode.update({"exp": expire})
    # Luego genera el jwt con el metodo encode de jwt, pasandole primero el diccionario con la informacion a codificar, la secretKey y el algoritmo que se va a utilizar HS256 en este caso
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Por ultimo devuelve el jwt
    return encoded_jwt

# Funcion encargada de verificar el token
def verify_token(token:str, credentials_exception):
    try:
        # Esto lo que hace es decodigficar el token , le pasa la secret key declarada y el algoritmo de cifrado
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # En la llave sub habiamos colocado el username por lo cual con get y la llave sub obtenemos el username
        username: str = payload.get("sub")
        if username is None:
            # Si no existe el username es por que la llave no existe y el usuario no esta autenticado y devuelve un credential exeption que se recibe de parametro
            raise credentials_exception
        # Luego de esto mediante el Token data del modelo que habiamos generado en schemas devovlemos un username, el username sera el usernname del modelo por eso es username=username
        token_data = Tokendata(username=username)
    except JWTError:
        # En caso de que ocurra cualquier otra cosa se envia este error que es el declarado en oauth con el 401 no autorizado
        raise credentials_exception