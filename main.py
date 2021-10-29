from flask import Flask
from base import Session
session = Session()

from Routes import consulta_id, routes_libros, routes_users, routes_prestamos


app = Flask(__name__)

@app.route ('/libros/id', methods=['GET'])
def respuesta_id():
    return consulta_id.idlibros()


@app.route ('/libros', methods=['GET', 'POST', 'PUT', 'DELETE'])
def respuesta_libros():
    return routes_libros.request_libros()
    

@app.route ('/usuarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def respuesta_usuarios():
    return routes_users.request_users()

@app.route ('/libros/prestamos', methods=['GET', 'POST', 'PUT', 'DELETE'])
def respuesta_prestamos():
    return routes_prestamos.request_prestamos()
    

if __name__ == "__main__":
    app.run(debug=True)