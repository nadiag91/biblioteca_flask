from sqlalchemy import  Column, String, Integer, Date

from base import Base

class Prestamos(Base):
    __tablename__ = 'prestamos'

    id = Column(Integer, primary_key=True)
    id_libro = Column(Integer)
    id_usuario = Column(Integer)
    nombre_libro = Column(String(100))
    nombrecompleto_usuario = Column(String(100))
    
    
    def __init__(self, id, id_libro, id_usuario, nombre_libro, nombrecompleto_usuario ):
        self.id = id
        self.id_libro =id_libro
        self.id_usuario = id_usuario
        self.nombre_libro = nombre_libro
        self.nombrecompleto_usuario = nombrecompleto_usuario