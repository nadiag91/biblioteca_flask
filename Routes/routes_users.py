from flask import request, jsonify, make_response, request
from base import Session

from Models.Model_Usuario_db import Usuario_db
from Routes.routes_libros import devolver_rol
from Validaciones.Usuario import Usuario_validacion, Notification
from Usuario import Usuario, Errores

from class_Suma import Suma

import uuid


def request_users():
    body_request = request.json
    id_usuario = body_request['id_usuario']
    try:
        rol_usuario = devolver_rol(id_usuario)
    except IndexError:
        return make_response(jsonify({'Respond': 'Error en id de usuario'}), 400)
    
    if(request.method == 'GET'):
        if rol_usuario == 'administrador':
            lista_usuarios = devolver_usuario()
            return make_response(jsonify(mostrar_usuarios(lista_usuarios)), 200)

    if(request.method == 'POST'):
        if rol_usuario == 'administrador':
            return nuevo_usuario(body_request)
          
      
    if(request.method == 'PUT'):  
        if rol_usuario == 'administrador':
            modif_libros_en_uso(body_request)
            return make_response(jsonify({'Respond':'Datos actualizados'}), 200)

    if(request.method == 'DELETE'):  
        if rol_usuario == 'administrador':
            borrar_usuario(body_request )
            return make_response(jsonify({'Respond':'Deleted'}), 200)

    else: 
        return make_response(jsonify({'Respond':'Acceso Denegado'}), 400)


#GET
def devolver_usuario():
    session = Session()
    lista_usuarios = session.query(Usuario_db).all()
    session.close()
    return lista_usuarios

def mostrar_usuarios(lista_usuarios):
    usuarios_encontrados = []
    for usuario in lista_usuarios:
        diccionario_usuarios = {'id' : usuario.id, \
        'nombre_completo' : usuario.nombre_completo, \
        'rol' : usuario.rol.name}
        usuarios_encontrados.append(diccionario_usuarios)
    return usuarios_encontrados

#GET suma
def devolver_suma():
    valor1=Suma(2,3)
    resultado = valor1.sumar_valores()
    return resultado



#POST
def nuevo_usuario(body):
    nuevo_usuario = Usuario(nombre_completo=body['nombre_completo'], rol = body['rol'])
    return nuevo_usuario.crear_nuevo_usuario()


#PUT
def modif_libros_en_uso(body):
    session = Session()
    id = body['id']
    nombre_completo = body['nombre_completo']
    session.query(Usuario_db).filter( Usuario_db.id == id ).update(nombre_completo)
    session.commit()
    session.close()


#DELETE
def borrar_usuario(body):
    session = Session()
    id = body['id']
    session.query(Usuario_db).filter(Usuario_db.id == id).delete()
    session.commit()
    session.close()
