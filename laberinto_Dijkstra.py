import random, heapq, copy

#Asignacion de valores mediante constantes
CAMINO = 0
EDIFICIO = 1
AGUA = 2
OBSTACULO = 3
INICIO = 4
FIN = 5
RUTA = 6

class CrearLaberinto:
    def __init__(self, filas, columnas):
        if columnas % 2 == 0:
            columnas += 1
        if filas % 2 == 0:
            filas += 1
            
        self.filas = filas
        self.columnas = columnas
        self.laberinto = [[EDIFICIO for _ in range(columnas)] for _ in range(filas)]
    
    def crear_camino(self, x, y):
        
        
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
                case 6:
                    simbolo = "🟥"
            print(simbolo, end="  ")
        print("")                                                                              
        
#Insertar cualquier elemento en el laberinto
def insertar_elementos(laberinto, valor):
    while True:
        try:
            pos_input = input("Ingrese la posicion (columna, fila) separada por la coma: ")
            fila, columna = map(int, pos_input.split(",")) #Separa cada valor tomando un marcador para hacerlo
            if (0 <= columna < len(laberinto[0])) and (0 <= fila < len(laberinto)): #Establece los limites del laberinto
                if ((laberinto[columna][fila] == CAMINO or laberinto[columna][fila] == OBSTACULO or laberinto[columna][fila] == AGUA) ): #Condiciona a que se escriba otro valor unicamente si en el lugar es un camino
                    laberinto[columna][fila] = valor
                    return laberinto, (columna, fila)
                else:
                    print("NO SE PUEDE INSERTAR NINGUN CARACTER EN ESA POSICION PORQUE NO ES UN LUGAR DISPONIBLE. DEBE SER UN CAMINO LIBRE, INTENTELO NUEVAMENTE")
            else:
                print("LA POSICION INGRESADA SALE DE LOS LIMITES DE LA MATRIZ")
        except ValueError:
            print("El formato de ingreso fue incorrecto debe de ser (columna, fila)!!!")

def dijkstra(laberinto, inicio, fin):
    filas = len(laberinto)
    columnas = len(laberinto[0])
    
    direcciones = [(0,1), (0,-1), (1, 0), (-1,0)]
    
    costo = { #Diccionario de costos
        CAMINO: 1,
        INICIO: 1,
        FIN: 1,
        AGUA: 3,
        OBSTACULO: 999999,
        EDIFICIO: None   
    }
    
    #Validacion para las coordenadas de la cola
    def es_valido(f, c):
        if not(0 <= f < filas and 0 <= c < columnas):
            return False
        
        celda = laberinto[f][c]
        
        if celda == EDIFICIO or celda == OBSTACULO:
            return False
        
        return True
    
    distancia = [[float("inf")] * columnas for _ in range(filas)] 
    padre = [[None] * columnas for _ in range(filas)]
    
    #Inicializacion de la cola
    cola = []
    distancia[inicio[0]][inicio[1]] = 0
    heapq.heappush(cola, (0, inicio))
    
    while cola:
        distancia_actual, (f, c) = heapq.heappop(cola)
        #Salta si es un estado viejo
        if distancia_actual != distancia[f][c]:
            continue
        
        if (f, c) == fin: #Si la posicion ya es el fin corta(ya llego al minimo)
            break
        
        for dir_f, dir_c in direcciones:
            nueva_f, nueva_c = f + dir_f, c +dir_c
            if not es_valido(nueva_f, nueva_c):
                continue
            
            celda = laberinto[nueva_f][nueva_c]
            peso = costo.get(celda, 1)
        
            nuevo_peso = distancia_actual + peso
        
            if nuevo_peso < distancia[nueva_f][nueva_c]:
                distancia[nueva_f][nueva_c] = nuevo_peso
                padre[nueva_f][nueva_c] = (f, c)
                heapq.heappush(cola, (nuevo_peso, (nueva_f, nueva_c)))
                
    lab_copia = copy.deepcopy(laberinto)
    #Condicion para cuando no exista camino o esten todos tapados
    if distancia[fin[0]][fin[1]] == float("inf"):
        print("NO EXISTE CAMINO POSIBLE ENTRE INICIO Y FIN")
        return None, lab_copia
    
    #Guardar en una lista utilizable el resultado de la cola
    camino = []
    actual = fin
    while actual is not None:
        camino.append(actual)
        actual = padre[actual[0]][actual[1]]
    
    print(f"Camino encontrado. Pasos: {len(camino) - 1} | Costo total: {distancia[fin[0]][fin[1]]}")    
    
    #Marcamos el camino encontrado
    for(ruta_fila, ruta_columna) in camino:
        if(ruta_fila, ruta_columna) != inicio and (ruta_fila, ruta_columna) != fin:
            lab_copia[ruta_fila][ruta_columna] = RUTA
    
    return camino, lab_copia

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
    print('Ingrese la posicion del INICIO de a uno')
    laberinto, inicio = insertar_elementos(laberinto, INICIO)
    print('Ingrese la posicion del DESTINO de a uno')
    laberinto, fin = insertar_elementos(laberinto, FIN)
    imprimir_laberinto(laberinto)
    
    #Bucle para los obstaculos
    while True:
        camino, lab_copia = dijkstra(laberinto, inicio, fin)
        if camino is None:
            imprimir_laberinto(lab_copia)
            break
        
        if camino:
            imprimir_laberinto(lab_copia)
        
            
        while True:
            try:
                deseo = input("¿Desea ingresar un obstaculo? SI/NO: ").lower()
                if "si" == deseo or deseo == "no":
                    break
                else:
                    print('El valor ingresado debe de ser "SI" o "NO"')               
            except ValueError:
                print('El valor ingresado debe de ser "SI" o "NO"')
        if deseo == "si":
            texto = """
¿Que tipo de objeto desea agregar?
    1-OBSTACULO "🚧"
    2-AGUA "🌊"
    3-BORRAR
    """
            while True:
                try:
                    opcion = int(input(texto))
                    if 1 == opcion:
                        laberinto, _ = insertar_elementos(laberinto, OBSTACULO)
                    elif 2 == opcion:
                        laberinto, _ = insertar_elementos(laberinto, AGUA)
                    elif 3 == opcion:
                        laberinto, _ = insertar_elementos(laberinto, CAMINO)
                    else:
                        print("SOLO PUEDE ELEGIR UNA DE ESTAS 3 OPCIONES")
                        
                    break 
                except ValueError:
                    print('La unicas opciones disponibles son "1" y "2"')
        else:
            break

main()
