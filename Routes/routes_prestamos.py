from flask import request, jsonify, make_response, request
from Models.Libro_db import Libro_db
from Models.Model_Usuario_db import Usuario_db
from Routes.routes_users import validar_usuario
from Validaciones.Prestamo import Condicion, Prestamo_de_libros

from base import Session

from Models.Prestamos_db import Prestamos_db
from Routes.routes_libros import devolver_rol

import uuid


def request_prestamos():
    body_request = request.json
    id_usuario = body_request['id_usuario']
    try:
        rol_usuario = devolver_rol(id_usuario)
    except IndexError:
        return make_response(jsonify({'Respond': 'Error en id de usuario'}), 400)
    
    if(request.method == 'GET'):
        if rol_usuario == 'administrador': 
            libro_consultado = consultar_libro(body_request)
            return verif_si_existe_libro(libro_consultado)

    if(request.method == 'POST'):
        if rol_usuario == 'administrador':
            cumplir_condiciones = validar_condiciones_para_prestamo(body_request)   
            if len(cumplir_condiciones) == 0:
                return make_response(jsonify(({'Respond' : 'Registro exitoso'}), (registro_exitoso(body_request))), 200)
            else:
                return make_response(jsonify(cumplir_condiciones), 400)

    if(request.method == 'PUT'): 
        if rol_usuario == 'administrador':  
            modif_estado_prestamo(body_request)
            return make_response(jsonify({'Respond':'Préstamo devuelto exitosamente'}), 200)


#GET
def consultar_libro(body):
    session = Session()
    nombre_libro = body['nombre_libro']

    ejemplares_libro = session.query(Libro_db).filter(Libro_db.disponibilidad, Libro_db.nombre == nombre_libro).all()
    session.close()
    return ejemplares_libro
   
def verif_si_existe_libro(libro_consultado):
    if len(libro_consultado) != 0:
        return make_response(jsonify(estado_libro(libro_consultado)), 200)
    else:
        return make_response(jsonify({'Respond' : 'Libro no encontrado'}), 400)

def estado_libro(libro_consultado):
    libro_ejemplares = []
    for libro in libro_consultado:
        datos = {'nombre_libro' : libro.nombre, 'estado': libro.disponibilidad.name}
        libro_ejemplares.append(datos)
    return libro_ejemplares


#POST
def validar_condiciones_para_prestamo(body):
    condicion = Condicion ()
    libros_en_uso = ver_libros_en_uso_usuario(body)
    
    usuario_cant_de_prestamos = len(libros_en_uso)
    unidades_totales, unidades_prestadas = verif_numero_copias(body)
    
    cant_copias_disponibles = obtener_num_unidades_disp_libro(unidades_totales, unidades_prestadas)
    nuevo_prestamo = Prestamo_de_libros(usuario_cant_de_prestamos, cant_copias_disponibles)
    nuevo_prestamo.validar_prestamo(condicion)
    devolver_condiciones = condicion.cumplir_condicion()
    return devolver_condiciones

    
def ver_libros_en_uso_usuario(body):
    session = Session()
    id_socio = body['id_socio']
    libros_en_uso = session.query(Prestamos_db).filter((Prestamos_db.id_usuario == id_socio) & (Prestamos_db.estado == 'prestado')).all()
    session.close()
    return libros_en_uso
   

def maximo_numero_libros_permitidos(libros_en_uso):
    if len(libros_en_uso) < 3:
        return True
    return False

def verificar_libro_unidades_disp(body):
    unidades_totales, unidades_prestadas = verif_numero_copias(body)
    unidades_disponibles = obtener_num_unidades_disp_libro(unidades_totales, unidades_prestadas)
    return validar_copias_disp(unidades_disponibles)
    

def verif_numero_copias(body):
    session = Session()
    id_libro = body['id_libro']
    copias_totales_libro = session.query(Libro_db).filter((Libro_db.id == id_libro) & (Libro_db.num_de_copias)).all()
    num_copias_prestadas = session.query(Prestamos_db).filter((Prestamos_db.id_libro == id_libro) & (Prestamos_db.estado  == 'prestado')).all()

    for datos in copias_totales_libro:
        unidades_totales = datos.num_de_copias
     
    unidades_prestadas = len(num_copias_prestadas)
    return unidades_totales, unidades_prestadas

def obtener_num_unidades_disp_libro(unidades_totales, unidades_prestadas):
    unidades_disponibles = unidades_totales - unidades_prestadas
    return unidades_disponibles

def validar_copias_disp(unidades_disponibles):
    if unidades_disponibles >= 1:
        return True 
    return False         

    
def devolver_libro_y_usuario(body):
    session = Session()
    id_libro = body['id_libro']
    id_socio = body['id_socio']
    libro = session.query(Libro_db).filter((Libro_db.id == id_libro)).all()
    usuario = session.query(Usuario_db).filter((Usuario_db.id == id_socio)).all()
    session.close()
    for datos in libro:
        nombre_libro = datos.nombre
    
    for datos in usuario:
        nombre_usuario = datos.nombre_completo
    
        return nombre_usuario, nombre_libro

def realizar_registro(body):
    nombre_usuario, nombre_libro = devolver_libro_y_usuario(body)
    session = Session()
    id_libro = body['id_libro']
    id_socio = body['id_socio']
        
    myuuid = str(uuid.uuid4()) 
    estado = 'prestado'
    session.add(Prestamos_db(myuuid, id_libro, id_socio, nombre_libro, nombre_usuario , estado))
    session.commit()
    session.close()
    return myuuid

def registro_exitoso(body):
    session = Session()
    id_prestamo = realizar_registro(body)
    nuevo_prestamo = session.query(Prestamos_db).filter(Prestamos_db.id == id_prestamo).all()
    valores_cargados = []
    for valor in nuevo_prestamo:
        nombre_datos = {'id_prestamo' : valor.id, 'id_libro' : valor.id_libro, 'id_usuario' : valor.id_usuario, 'nombre_libro' : valor.libro, \
        'nombre_usuario' : valor.usuario, 'estado_libro' : valor.estado.name}
        valores_cargados.append(nombre_datos)
    return valores_cargados


#PUT
def modif_estado_prestamo(body):
    session = Session()
    id_libro = body['id_libro']
    id_socio = body['id_socio']
   
    session.query(Prestamos_db).filter(Prestamos_db.id_libro == id_libro, Prestamos_db.id_usuario == id_socio) \
    .update({Prestamos_db.estado : 'devuelto'})
    
    session.commit()
    session.close()







    


    




    










