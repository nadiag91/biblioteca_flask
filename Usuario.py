from typing import List

from sqlalchemy.log import echo_property
from Routes.routes_libros import devolver_libros
from Validaciones.Usuario import Notification
from Models.Model_Usuario_db import Usuario_db
from flask import jsonify, make_response, request
from base import Session

#guardar en atributo el mensaje de error y devolverlo para obtener la respuesta 
import uuid

class Usuario:
    def __init__(self, nombre_completo, rol):
        self.id = str(uuid.uuid4())
        self.nombre_completo = nombre_completo
        self.rol = rol
        self.errores = Errores()

    def crear_nuevo_usuario(self):
        self.__validar_nombre()
        errores_encontrados = self.__verificar_errores()
        if len(errores_encontrados) == 0:
            return self.__persistir_usuario()
        else:
            return make_response(jsonify(self.errores.get_error_message()), 400)

        

    def __validar_nombre(self):
        if self.nombre_completo is None:
            self.errores.guardar_errores('Debe completarse el nombre')
            return
        if len(self.nombre_completo) < 4:
            self.errores.guardar_errores('El nombre no puede tener menos de 4 caracteres')

    def __verificar_errores(self):
        devolver_errores = self.errores.get_error_message()
        return devolver_errores  

    

    def __persistir_usuario(self):
        session = Session()   
        id = self.id
        nombre_completo = self.nombre_completo
        rol = self.rol
        session.add(Usuario_db(id, nombre_completo, rol))
        session.commit()
        session.close()
        return make_response(jsonify({'Respond' : 'Usuario cargado exitosamente'}), 200)
        


class Errores:
    __errores : List

    def __init__(self):
        self.__errores = []
        
        
    def guardar_errores(self, message:str, excepcion: Exception = None):
        if excepcion is not None:
            exception_name = self.__obtener_nombre_error(excepcion)
            self.__errores.append({exception_name: str(excepcion)})
            return

        self.__errores.append({'error': message})

    def get_error_message(self):
        return self.__errores

    def __obtener_nombre_error(self, exception: Exception):
        return type(exception).__name__

        

