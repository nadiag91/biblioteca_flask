from flask import request, jsonify, make_response, request
from base import Session

from Models.Libro_db import Libro_db
from Models.Model_Usuario_db import Usuario_db


def request_libros():
    body_request = request.json
    id_usuario = body_request['id_usuario']
    rol_usuario = devolver_rol(id_usuario)
   
    
    if(request.method == 'GET'):
        if rol_usuario == 'administrador' or 'socio':
            try:
                lista_libros = devolver_libros()
                return make_response(jsonify(mostrar_libros(lista_libros)), 200)
            except:
                raise Exception
        
    if(request.method == 'POST'):
        if rol_usuario == 'administrador':
            try:
                agregar_libro(body_request)
            except KeyError:
                return make_response(jsonify({'Respond':'Error en valores ingresados'}), 400)
            else:
                return make_response(jsonify({'Respond': 'Libro agregado'}), 200)
            
    if(request.method == 'PUT'): 
        if rol_usuario == 'administrador':  
            modif_disponibilidad(body_request)
            return make_response(jsonify({'Respond':'Estado de libro modificado'}), 200)

    if(request.method == 'DELETE'):  
        if rol_usuario == 'administrador':
            borrar_libro(body_request)
            return make_response(jsonify({'Respond':'Deleted'}), 200)
    
    else: 
        return make_response(jsonify({'Respond':'Acceso Denegado'}), 400)


#ROL
def devolver_rol(id_usuario: str):
    try: 
        session = Session()
        rol_usuario = list(session.query(Usuario_db).filter(Usuario_db.id == id_usuario).all())
        session.close()                             
        return rol_usuario[0].rol.name 
    except IndexError:
        return make_response(jsonify({'Respond': 'Usuario no encontrado'}), 400)

        

#GET
def devolver_libros():
    session = Session()
    lista_libros = session.query(Libro_db).all()
    session.close()
    return lista_libros

def mostrar_libros(lista_libros):
    libros_encontrados = []
    for libro in lista_libros:
        diccionario_libros = {'id' : libro.id, \
        'nombre_libro' : libro.nombre, \
        'autor' : libro.autor, \
        'disponibilidad' : libro.disponibilidad.name}
        libros_encontrados.append(diccionario_libros)
    return libros_encontrados
        

#POST
def agregar_libro(body):
    session = Session()
        
    id = body['id_libro'],
    nombre = body['nombre_libro'],
    autor =body['autor'],
    disponibilidad = body['disponibilidad']
        
    session.add(Libro_db(id, nombre, autor, disponibilidad))
    session.commit()
    session.close()        
       
#PUT
def modif_disponibilidad(body):
    session = Session()
    disponibilidad = body['disponibilidad']
    id_libro = body['id']
    session.query(Libro_db).filter(Libro_db.id == id_libro).update(disponibilidad)
    session.commit()
    session.close()

#DELETE
def borrar_libro(body):
    session = Session()
    id = body['id']
    session.query(Libro_db).filter(Libro_db.id == id).delete()
    session.commit()
    session.close()

