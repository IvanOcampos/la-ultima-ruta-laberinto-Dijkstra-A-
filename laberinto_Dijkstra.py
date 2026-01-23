import random

#Asignacion de valores mediante constantes
CAMINO = 0
EDIFICIO = 1
AGUA = 2
OBSTACULO = 3
INICIO = 4
FIN = 5

#Crecion del laberinto
def crear_laberinto(filas, columnas):
    # Garantizamos que siempre sea impar para que tenga paredes 
    if columnas % 2 == 0:
        columnas += 1
    if filas % 2 == 0:
        filas += 1
        
    laberinto = [[EDIFICIO for _ in range(columnas)] for _ in range(filas)]
    
    
    def crear_camino(x, y):
        laberinto[y][x] = CAMINO
        
        direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcciones)
        
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            
            if (1 <= nx < columnas -1) and (1 <= ny < filas -1) and (laberinto[ny][nx] == EDIFICIO):
                #Romper el muro entre la celda actual y la siguiente
                laberinto[y + dy//2][x + dx//2] = CAMINO
                crear_camino(nx, ny)

    crear_camino(1, 1)
    
    #Creacion de mas caminos
    for y in range(1, filas -1):
        for x in range(1, columnas - 1):
            if laberinto[y][x] == EDIFICIO and random.random() < 0.5:
                laberinto[y][x] = CAMINO
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
        
#Insertar cualquier elemento en el laberinto
def insertar_elementos(laberinto, valor):
    while True:
        try:
            pos_input = input("Ingrese la posicion (columna, fila) separada por la coma: ")
            fila, columna = map(int, pos_input.split(",")) #Separa cada valor tomando un marcador para hacerlo
            if (0 <= columna < len(laberinto[0])) and (0 <= fila < len(laberinto)): #Establece los limites del laberinto
                if ((laberinto[columna][fila] == CAMINO) ): #Condiciona a que se escriba otro valor unicamente si en el lugar es un camino
                    laberinto[columna][fila] = valor
                    return laberinto
                else:
                    print("NO SE PUEDE INSERTAR NINGUN CARACTER EN ESA POSICION PORQUE NO ES UN LUGAR DISPONIBLE. DEBE SER UN CAMINO LIBRE, INTENTELO NUEVAMENTE")
            else:
                print("LA POSICION INGRESADA SALE DE LOS LIMITES DE LA MATRIZ")
        except ValueError:
            print("El formato de ingreso fue incorrecto debe de ser (columna, fila)!!!")

#def dijkstra(laberinto):
    

def main():
    #Validacion de entrada para el tamaño del laberinto
    while True:
        try:
            filas  = int(input("Ingrese la cantidad de filas: "))
            columnas = int(input("Ingrese la cantidad de columnas: "))
            if (filas > 0) or (columnas > 0):
                break
            else:
                print("Los numeros deben de ser mayores a 0. Intentelo nuevamente")
        
        except ValueError:
            print("El valor ingresado debe de ser un numero entero mayor a 0")

    laberinto = crear_laberinto(filas, columnas)
    imprimir_laberinto(laberinto)
    print('Ingrese la posicion deL INICIO de a uno')
    insertar_elementos(laberinto, INICIO)
    print('Ingrese la posicion del DESTINO de a uno')
    insertar_elementos(laberinto, FIN)
    imprimir_laberinto(laberinto)

main()
#print(len(laberinto)) #cantidad de filas
#print(len(laberinto[0])) #cantidad de columnas 