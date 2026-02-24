import random
import heapq
import copy
from abc import ABC, abstractmethod

#Asignacion de valores mediante constantes
CAMINO = 0
EDIFICIO = 1
AGUA = 2
OBSTACULO = 3
INICIO = 4
FIN = 5
RUTA = 6

class Laberinto:
    """
    Responsabilidad Única(Single Responsability Principle (SRP))
    - Guardar y administrar la matriz del laberinto.
    - Proveer métodos para acceder/modificar celdas de forma segura.
    """
    def __init__(self, filas, columnas):
        if columnas % 2 == 0:
            columnas += 1
        if filas % 2 == 0:
            filas += 1
            
        self.__filas = filas
        self.__columnas = columnas
        self.__matriz = [[EDIFICIO for _ in range(columnas)] for _ in range(filas)]
    
    @property
    def filas(self):
        return self.__filas
    
    @property
    def columnas(self):
        return self.__columnas
    
    def obtener_matriz(self):
        """Abstraccion: devuelve la matriz sin exponer el atributo directamente"""
        return self.__matriz
    
    def dentro_limites(self, fila, columna):
        return 0 <= fila < self.__filas and 0 <= columna < self.__columnas
    
    def obtener_celda(self, fila, columna):
        return self.__matriz[fila][columna]
    
    def asignar_celda(self, fila, columna, valor):
        self.__matriz[fila][columna] = valor
    
    def copiar(self):
        """Devuelve una copia profunda del laberinto."""
        nuevo = copy.deepcopy(self)
        return nuevo

class GeneradorLaberinto:
    """
    Responsabilidad única:
    - Generar laberintos usando DFS
    """
    def __init__(self, probabilidad_camino_extra = 0.5):
        self.__probabilidad = probabilidad_camino_extra
    
    def __crear_camino(self, laberinto, x, y):
        laberinto.asignar_celda(y, x, CAMINO)
        
        direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcciones)
        
        for dx, dy in direcciones:
            ny, nx = dy + y, dx + x
            
            if (1 <= nx < laberinto.columnas - 1) and (1 <= ny < laberinto.filas - 1) and (laberinto.obtener_celda(ny, nx) == EDIFICIO):
                laberinto.asignar_celda(y + dy // 2, x + dx // 2, CAMINO)
                self.__crear_camino(laberinto, nx, ny)
                
    def generar(self, filas, columnas):
        laberinto = Laberinto(filas, columnas)
        
        #Genera el camino principal
        self.__crear_camino(laberinto, 1, 1)
        
        #Creacion de mas caminos
        for y in range(1, laberinto.filas -1):
            for x in range(1, laberinto.columnas -1):
                if laberinto.obtener_celda(y, x) == EDIFICIO and random.random() < self.__probabilidad:
                    laberinto.asignar_celda(y, x, CAMINO)
        return laberinto

class ImpresorLaberinto:
    """
    Responsabilidad única:
    - Mostrar el laberinto en pantalla
    """
    def __init__(self):
        self.__simbolos = {
            CAMINO : "🟩",
            EDIFICIO : "🏢",
            AGUA : "🌊",
            OBSTACULO : "🚧",
            INICIO : "🧍",
            FIN : "🏁",
            RUTA : "🟥"
        }
        
    def imprimir(self, laberinto):
        matriz = laberinto.obtener_matriz()
        
        for fila in matriz:
            for celda in fila:
                print(self.__simbolos.get(celda, "?"), end="  ")
            print("")                                                                              

class EditorLaberinto:
    """
    Responsabilidad única:
    - Insertar elementos dentro del laberinto con validación.
    """        
    
    def insertar(self, laberinto, fila, columna, valor):
        if not laberinto.dentro_limites(fila, columna):
            raise ValueError("LA POSICION INGRESADA ESTA FUERA DE LOS LIMITES DE LA MATRIZ")

        celda_actual = laberinto.obtener_celda(fila, columna)
        
        if celda_actual in (CAMINO, OBSTACULO, AGUA):
            laberinto.asignar_celda(fila, columna, valor)
            return(fila, columna)
        
        raise ValueError("NO SE PUEDE INSERTAR EN ESA POSICION PORQUE NO ES UN CAMINO DISPONIBLE")

class BuscadorCamino(ABC):
    """
    Abstracción:
    - Define un contrato para cualquier algoritmo de búsqueda.
    """
    
    @abstractmethod
    def buscar(self, laberinto, inicio, fin):
        pass

class BuscadorDijkstra(BuscadorCamino):
    """
    Herencia: hereda de BuscadorCamino
    Polimorfismo: implementa buscar() a su manera
    """
    
    def __init__(self):
        self.__costos = {
            CAMINO: 1,
            INICIO: 1,
            FIN: 1,
            AGUA: 3,
            OBSTACULO: 999999,
            EDIFICIO: None
        }
        
    def __es_valido(self, laberinto, fila, columna):
        if not laberinto.dentro_limites(fila, columna):
            return False
            
        celda = laberinto.obtener_celda(fila, columna)
            
        if celda == EDIFICIO or celda == OBSTACULO:
            return False
            
        return True
    
    def buscar(self, laberinto, inicio, fin):
        filas = laberinto.filas
        columnas = laberinto.columnas
        
        direcciones = [(0,1), (1,0), (-1,0), (0, -1)]    
        
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
                if not self.__es_valido(laberinto, nueva_f, nueva_c):
                    continue
                
                celda = laberinto.obtener_celda(nueva_f,nueva_c)
                peso = self.__costos.get(celda, 1)
            
                nuevo_peso = distancia_actual + peso
            
                if nuevo_peso < distancia[nueva_f][nueva_c]:
                    distancia[nueva_f][nueva_c] = nuevo_peso
                    padre[nueva_f][nueva_c] = (f, c)
                    heapq.heappush(cola, (nuevo_peso, (nueva_f, nueva_c)))
         
        #Copia del laberinto para no marcar el original            
        lab_copia = copy.deepcopy(laberinto)
        
        #Condicion para cuando no exista camino o esten todos tapados
        if distancia[fin[0]][fin[1]] == float("inf"):
            return None, lab_copia
        
        #Guardar en una lista utilizable el resultado de la cola
        camino = []
        actual = fin
        while actual is not None:
            camino.append(actual)
            actual = padre[actual[0]][actual[1]]
        
        #print(f"Camino encontrado. Pasos: {len(camino) - 1} | Costo total: {distancia[fin[0]][fin[1]]}")    
        print(f"Costo total: {distancia[fin[0]][fin[1]]}")
        
        #Marcamos el camino encontrado
        for(ruta_fila, ruta_columna) in camino:
            if(ruta_fila, ruta_columna) != inicio and (ruta_fila, ruta_columna) != fin:
                lab_copia.asignar_celda(ruta_fila, ruta_columna, RUTA)
        
        return camino, lab_copia

class AplicacionLaberinto:
    """
    Responsabilidad única:
    - Controlar el flujo del programa (menús, interacción con usuario)
    Usa composicion: depende de varias clases
    """
    
    def __init__(self, generador, impresor, editor, buscador):
        self.__generador = generador
        self.__impresor = impresor
        self.__editor = editor
        self.__buscador = buscador
        
    def __leer_tamaño(self):
        #Validacion de entrada para el tamaño del laberinto
        while True:
            try:
                filas = int(input("Ingrese la cantidad de filas: "))
                columnas = int(input("Ingrese la cantidad de columnas: "))
                
                if filas > 4 and columnas > 4:
                    return filas, columnas
                
                print("Los numeros tienen que ser mayores a 4. Intentelo nuevamente")
            
            except ValueError:
                print("El valor ingresado debe de ser un numero mayor a 4")
                
    def __leer_posicion(self):
        while True:
            try:
                pos_input = input("Ingrese la posicion (columna, fila) separa por coma: ")
                columna, fila = map(int, pos_input.split(","))
                return fila, columna
            except ValueError:
                print("Formato incorrecto. Debe ser columna, fila (ej: 3,5)")
    
    def __insertar_elemento_interactivo(self, laberinto, valor):
        while True:
            try:
                fila, columna = self.__leer_posicion()
                pos = self.__editor.insertar(laberinto, fila, columna, valor)
                return pos
            except ValueError as e:
                print(e)
            
    def ejecutar(self):
        while True:
            filas, columnas = self.__leer_tamaño()
            
            laberinto = self.__generador.generar(filas, columnas)
            
            self.__impresor.imprimir(laberinto)
            
            print("\n Ingrese la posicion del INICIO: ")
            inicio = self.__insertar_elemento_interactivo(laberinto, INICIO)
            
            print("\n Ingrese la posicion del FIN: ")
            fin = self.__insertar_elemento_interactivo(laberinto, FIN)
            
            self.__impresor.imprimir(laberinto)
            
            while True:
                camino, lab_con_ruta = self.__buscador.buscar(laberinto, inicio, fin)
                
                if camino is None:
                    print("\nNO EXISTE CAMINO POSIBLE ENTRE INICIO Y FIN")
                    self.__impresor.imprimir(lab_con_ruta)
                    break
                
                print(f"\nCamino encontrado. Pasos: {len(camino) - 1}")
                self.__impresor.imprimir(lab_con_ruta)
                
                deseo = input("\nDesea ingresar un obstaculo? SI/NO: ").lower()
                
                if deseo != "si":
                    break
                
                texto = """
¿Que tipo de objeto desea agregar?
    1-OBSTACULO "🚧"
    2-AGUA "🌊"
    3-BORRAR
                """
                
                while True:
                    try:
                        opcion = int(input(texto))
                        
                        if opcion == 1:
                            self.__insertar_elemento_interactivo(laberinto, OBSTACULO)
                        elif opcion == 2:
                            self.__insertar_elemento_interactivo(laberinto, AGUA)
                        elif opcion == 3:
                            self.__insertar_elemento_interactivo(laberinto, CAMINO)
                        else:
                            print("SOLO PUEDE ELEGIR 1, 2 o 3")
                            continue
                        
                        break
                    except ValueError:
                        print("Debe ingresar un numero valido.")
                        
def main():
    generador = GeneradorLaberinto()
    impresor = ImpresorLaberinto()
    editor = EditorLaberinto()
    
    #Polimorfismo: podrías cambiar el algoritmo sin cambiar la app
    buscador = BuscadorDijkstra()
    
    app = AplicacionLaberinto(generador, impresor, editor, buscador)
    
    app.ejecutar()
    
main()