
from flask import Flask, request, jsonify, make_response, request
from base import Session
session = Session()

from Models.Libro import Libro
from Models.Usuario import Usuario
from Models.Prestamos import Prestamos

app = Flask(__name__)

@app.route ('/libros/id', methods=['GET'])
def consulta_idlibros():
    if(request.method == 'GET'):
        value = request.args['id']
        try:
            respuesta = list(session.query(Libro).filter(Libro.id == value))    
            nombre_libro = respuesta[0].nombre                
            if len(respuesta) != 0:
                return make_response(jsonify({'Respond': 'El nombre del libro es' + nombre_libro }), 200)
            else:
                return make_response(jsonify({'Respond':'Libro no encontrado'}), 400)
        
        except:
            print('Excepcion predeterminada')
    
    session.close()       
  

@app.route ('/libros', methods=['GET', 'POST', 'PUT', 'DELETE'])
def consulta_libros():
    if(request.method == 'GET'):

        session.execute("SELECT * FROM Libros")
        session.commit()
        session.close()
        return make_response(jsonify({'Respond':'Users'}), 200)
     
    if(request.method == 'POST'):
        body_request = request.json

        {
        'id' : body_request['id'],
        'nombre' : body_request['nombre'],
        'autor' : body_request['autor'],
        'disponibilidad' : body_request['disponibilidad']
        }

        #agrega un libro al registro
        agregar_libro = Libro(body_request['id'], body_request['nombre'], body_request['autor'], body_request['disponibilidad'])
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


@app.route ('/usuarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def consulta_usuarios():
    if(request.method == 'GET'):
            session.execute("SELECT * FROM usuarios")
            session.commit()
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