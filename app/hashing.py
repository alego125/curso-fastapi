from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

class Hash:

    # Metodo para encriptar la contraseña
    def hash_password(password):
        # Devolvemos la contraseña ya hasheada
        return pwd_context.hash(password)

    # Creamos el metodo que se va a encargar de verificar la contraseña, el mismo recibe el password de la base de datos en forma de hash y el password de el usuario que envio el cual no esta encriptado y servira pra verificar si es igual al encriptado o no 
    def verify_password(plain_password, hashed_password):
        # Retornamos loq ue nos devuelve el metodo verify de el objeto pwd_context al cual le pasamos primero la contraseña encriptada de la base de datos y luego le pasamos el password que nos envia el usuario y este metodo se encarga de verificar si coinciden o no devolviendonos el resultado
        return pwd_context.verify(plain_password, hashed_password)