
from flask import Flask, request, jsonify, make_response, request
from base import Session
session = Session()

from Models.Libro import Libro
from Models.Usuario import Usuario
from Models.Prestamos import Prestamos

from Routes import consulta_id, routes_libros

app = Flask(__name__)

@app.route ('/libros/id', methods=['GET'])
def respuesta_id():
    return consulta_id.idlibros()


@app.route ('/libros', methods=['GET', 'POST', 'PUT', 'DELETE'])
def respuesta_libros():
    return routes_libros.request_libros()
    


@app.route ('/usuarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def consulta_usuarios():
    if(request.method == 'GET'):
            session.execute("SELECT * FROM usuarios")
            session.close()
            return make_response(jsonify({'Respond':'Listado de Usuarios'}), 200)

    if(request.method == 'POST'):
        body_request = request.json
        params = {
        'id' : body_request['id'],
        'nombre' : body_request['nombre'],
        'autor' : body_request['autor']
        }

        agregar_libro = Libro(body_request['id'], body_request['nombre'], body_request['autor'])
        session.add(agregar_libro)
        
        session.commit()
        session.close()
        return make_response(jsonify({'Respond':'Libro agregado'}), 200)
      
    if(request.method == 'PUT'):  
        body_request = request.json
        
        session.query(Libro).filter( Libro.id == body_request['id']) \
        .update({'disponibilidad' : body_request['disponibilidad']})
             
        session.commit()
        session.close()
        return make_response(jsonify({'Respond':'Estado de libro modificado'}), 200)

    if(request.method == 'DELETE'):  
        body_request = request.json
        
        session.query(Libro).filter(Libro.id == body_request['id']).delete()
        session.commit()
        session.close()
        return make_response(jsonify({'Respond':'Deleted'}), 200)
    
if __name__ == "__main__":
    app.run(debug=True)