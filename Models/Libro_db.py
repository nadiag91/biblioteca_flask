from sqlalchemy import  Column, String, Integer, Enum

from base import Base
from base import Session
session = Session()


class Libro_db(Base):
    __tablename__ = 'libros'

    id = Column('id',Integer, primary_key=True)
    nombre = Column('nombre',String(100))
    autor = Column('autor',String(100))
    num_de_copias = Column('num_copias',Integer)

    def __init__(self, id, nombre, autor, num_de_copias):
        self.id = id
        self.nombre = nombre
        self.autor = autor
        self.num_de_copias = num_de_copias

    def ver_nombre (self):
        return self.nombre




    
