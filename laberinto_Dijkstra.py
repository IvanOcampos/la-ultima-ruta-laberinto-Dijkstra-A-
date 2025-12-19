import random

#Asignacion de valores
camino_libre = 0
edificio = 1
agua = 2
temp_zone = 3
inicio = 4
fin = 5

#Crecion del laberinto
def crear_laberinto(fila, columna):
    laberinto = [[edificio for _ in range(columna)] for _ in range(fila)]
    print('Ingrese la posicion de la entrada de a uno')
    insertar_elementos(laberinto, inicio)
    print('Ingrese la posicion de la salida de a uno')
    insertar_elementos(laberinto, fin)
    return laberinto

#Impresion del laberinto
def imprimir_laberinto(laberinto):
    for i in laberinto:
        print(*i)
        
#Insertar elementos
def insertar_elementos(laberinto, valor):
    pos = (int(input()), int(input()))
    y, x = pos
    laberinto[x][y] = valor
    return laberinto


laberinto = crear_laberinto(fila = int(input("Ingrese la cantidad de filas: ")), columna = int(input("Ingrese la cantidad de columnas: ")))
imprimir_laberinto(laberinto)