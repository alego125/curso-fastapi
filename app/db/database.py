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