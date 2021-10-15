from flask import request, jsonify, make_response, request
from base import Session

from Models.Libro import Libro
from Models.Usuario import Usuario

#VER ERROR PARA OBTENER ROL CON ID CONFORMADO POR NUMEROS Y LETRAS
def request_libros():
    body_request = request.json
    id_usuario = body_request['id_usuario']
    try:
        rol_usuario = devolver_rol(id_usuario)
    except IndexError:
        return make_response(jsonify({'Respond': 'Error en id de usuario'}), 400)
    
    
    if(request.method == 'GET'):
        if rol_usuario == 'administrador' or 'socio':
            lista_libros = devolver_libros()
            return make_response(jsonify(mostrar_libros(lista_libros)), 200)
        
    if(request.method == 'POST'):
        if rol_usuario == 'administrador':
            try:
                agregar_libro()
            except KeyError:
                return make_response(jsonify({'Respond':'Error en valores ingresados'}), 400)
            else:
                return make_response(jsonify({'Respond': 'Libro agregado'}), 200)
            
    if(request.method == 'PUT'): 
        if rol_usuario == 'administrador':  
            modif_disponibilidad()
            return make_response(jsonify({'Respond':'Estado de libro modificado'}), 200)

    if(request.method == 'DELETE'):  
        if rol_usuario == 'administrador':
            borrar_libro()
            return make_response(jsonify({'Respond':'Deleted'}), 200)
    
    else: 
        return make_response(jsonify({'Respond':'Acceso Denegado'}), 400)


def devolver_rol(id_usuario: str):
    session = Session()
    rol_usuario = list(session.query(Usuario).filter(Usuario.id == id_usuario).all())
    session.close()                             
    return rol_usuario[0].rol.name   
        

#GET
def devolver_libros():
    session = Session()
    lista_libros = session.query(Libro).all()
    session.close()
    return lista_libros

def mostrar_libros(lista_libros):
    libros_encontrados = []
    for libro in lista_libros:
        diccionario_libros = {'id' : libro.id, 'nombre_libro' : libro.nombre, 'autor' : libro.autor}
        libros_encontrados.append(diccionario_libros)
    return libros_encontrados
        

#POST
def agregar_libro():
    session = Session()
    body_request = request.json
    params = {
        'id' : body_request['id_libro'],
        'nombre' : body_request['nombre_libro'],
        'autor' : body_request['autor'],
        'disponibilidad' : body_request['disponibilidad']
        }
    session.add( 
        Libro(body_request['id_libro'], body_request['nombre_libro'], body_request['autor'], body_request['disponibilidad'])
    )
    session.commit()
    session.close() 
        
       
#PUT
def modif_disponibilidad():
    session = Session()
    body_request = request.json  
    session.query(Libro).filter(Libro.id == body_request['id']) \
    .update({'disponibilidad' : body_request['disponibilidad'] })
            
    session.commit()
    session.close()

#DELETE
def borrar_libro():
    session = Session()
    body_request = request.json
    session.query(Libro).filter(Libro.id == body_request['id']).delete()
    session.commit()
    session.close()

