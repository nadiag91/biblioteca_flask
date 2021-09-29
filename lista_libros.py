

libro1 = [1, 'nombre1', 'autor1']
libro2 = [2, 'nombre2', 'autor2']
lista_libros = [libro1, libro2]

lista_productos = []

for libro in lista_libros:
    diccionario = {'id' : libro[0], 'name' : libro[1], 'author' : libro[2]}
    lista_productos.append(diccionario)


print (lista_productos)