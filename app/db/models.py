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