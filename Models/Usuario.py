from sqlalchemy import  Column, String, Integer, Date

from base import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre_completo = Column(String(100))
    libros_en_uso = Column(String(100))
   

    def __init__(self, id, nombre_completo, libros_en_uso ):
        self.id = id
        self.nombre_completo = nombre_completo
        self.libros_en_uso = libros_en_uso
       
