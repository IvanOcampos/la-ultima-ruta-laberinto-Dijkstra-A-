import random

#Asignacion de valores
camino_libre = 0
edificio = 1
agua = 2
temp_zone = 3
inicio = 4
fin = 5

#Crecion del laberinto
def crear_laberinto(filas, columnas):
    laberinto = [[camino_libre for _ in range(columnas)] for _ in range(filas)]
    print('Ingrese la posicion deL INICIO de a uno')
    insertar_elementos(laberinto, inicio)
    print('Ingrese la posicion del DESTINO de a uno')
    insertar_elementos(laberinto, fin)
    return laberinto

#Impresion del laberinto
def imprimir_laberinto(laberinto):
    for i in range(len(laberinto)):
        for j in range(len(laberinto[i])):
            match laberinto[i][j]:
                case 0:
                    simbolo = "🟩"
                case 1:
                    simbolo = "🏢"
                case 2:
                    simbolo = "🌊"
                case 3:
                    simbolo = "🚧"
                case 4:
                    simbolo = "🧍"
                case 5:
                    simbolo = "🏁"
            print(simbolo, end="  ")
        print("")                                                                              
        
#Insertar elementos
def insertar_elementos(laberinto, valor):
    while True:
        try:
            pos_input = input("Ingrese la posicion (columna, fila) separada por la coma: ")
            fila, columna = map(int, pos_input.split(","))
            if (0 <= columna < len(laberinto[0])) and (0 <= fila < len(laberinto)):
                if (laberinto[columna][fila] == camino_libre):
                    laberinto[columna][fila] = valor
                    return laberinto
                else:
                    print("NO SE PUEDE INSERTAR NINGUN CARACTER EN ESA POSICION PORQUE NO ES UN LUGAR DISPONIBLE O UN CAMINO LIBRE, INTENTELO NUEVAMENTE")
            else:
                print("LA POSICION INGRESADA SALE DE LOS LIMITES DE LA MATRIZ")
        except ValueError:
            print("El formato de ingreso fue incorrecto debe de ser (columna, fila)!!!")


laberinto = crear_laberinto(filas = int(input("Ingrese la cantidad de filas: ")), columnas = int(input("Ingrese la cantidad de columnas: ")))
imprimir_laberinto(laberinto)

#print(len(laberinto)) #cantidad de filas
#print(len(laberinto[0])) #cantidad de columnas 