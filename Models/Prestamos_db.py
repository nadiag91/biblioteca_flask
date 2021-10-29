from sqlalchemy import  Column, String, Integer
from sqlalchemy.sql.sqltypes import VARCHAR, Enum
from Models.Estado import Estado

from base import Base

class Prestamos_db(Base):
    __tablename__ = 'prestamos'

    id = Column('id', VARCHAR, primary_key=True)
    id_libro = Column('id_libro', VARCHAR)
    id_usuario = Column('id_usuario', VARCHAR)
    libro = Column('libro', String(100))
    usuario = Column('usuario', String(100))
    estado = Column('estado', Enum(Estado))
    
    
    def __init__(self, id, id_libro, id_usuario, libro, usuario, estado):
        self.id = id
        self.id_libro = id_libro
        self.id_usuario = id_usuario
        self.libro = libro
        self.usuario = usuario
        self.estado = estado