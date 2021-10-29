from sqlalchemy import  Column, String, Enum

from base import Base
from Models.Rol import Rol

class Usuario_db(Base):
    __tablename__ = 'usuarios'

    id = Column(String(100), primary_key=True)
    nombre_completo = Column(String(100))
    rol = Column('rol',Enum(Rol))
   

    def __init__(self, id, nombre_completo, rol ):
        self.id = id
        self.nombre_completo = nombre_completo
        self.rol = rol
    
    def ver_id(self):
        return self.id
       
    def ver_rol(self):
        return self.rol

    