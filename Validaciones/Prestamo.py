from typing import List

class Condicion:
    __condiciones: List 

    def __init__(self):
        self.__condiciones = []

    def cumplir_condicion(self, message: str, excepcion: Exception = None):
        if excepcion is not None:
            excepcion_name = self.__devolver_excepcion(excepcion)
            self.__condiciones.append({excepcion_name: str(excepcion)})
            return

        self.__condiciones.append({'Atencion': message})

    def devolver_errores(self):
        return self.__errors

    def __devolver_excepcion(self, exception: Exception):
        return type(exception).__name__


class Prestamo_de_libros:
    def __init__(self, usuario_cant_de_prestamos, cant_copias_disponibles):
        self.usuario_cant_de_prestamos = usuario_cant_de_prestamos
        self.cant_copias_disponibles = cant_copias_disponibles


    def validar_prestamo (self, condicion: Condicion):
        self.__maximo_numero_libros_permitidos(condicion)
        self.__unidades_disponibles_libro(condicion) 


    def __maximo_numero_libros_permitidos(self, condicion : Condicion):
        if self.usuario_cant_de_prestamos == 3:
            condicion.cumplir_condicion('Ha superado la máxima cantidad de prestamos')
             
    
    def __unidades_disponibles_libro(self, condicion: Condicion):
        if self.cant_copias_disponibles < 1:
            condicion.cumplir_condicion('No hay unidades disponibles del libro solicitado')
            
   
    
