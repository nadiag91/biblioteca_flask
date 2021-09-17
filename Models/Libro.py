from sqlalchemy import  Column, String, Integer, Date
from sqlalchemy.sql.sqltypes import BOOLEAN

from base import Base

class Libro(Base):
    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    autor = Column(String(100))
    disponibilidad = BOOLEAN

    def __init__(self, id, nombre, autor, disponibilidad):
        self.id = id
        self.nombre = nombre
        self.autor = autor
        self.disponibilidad = disponibilidad

    def ver_nombre (self):
        return self.nombre

    def ver_disponibilidad (self):
        return self.disponibilidad
