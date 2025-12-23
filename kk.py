import random

# Definición de constantes
CAMINO = 0
EDIFICIO = 1
ENTRADA = 4
SALIDA = 5


def generar_laberinto_dinamico(filas, columnas, complejidad=0.1):
    # 1. Crear rejilla llena de paredes
    # Usamos dimensiones impares para que las paredes queden bien definidas
    f, c = filas, columnas
    laberinto = [[EDIFICIO for _ in range(c)] for _ in range(f)]

    def cavar(r, col):
        laberinto[r][col] = CAMINO
        # Direcciones: Arriba, Abajo, Izquierda, Derecha (moviendo de a 2)
        direcciones = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(direcciones)

        for dr, dc in direcciones:
            nr, nc = r + dr, col + dc
            # Verificar si la nueva posición está dentro del mapa y es pared
            if 0 <= nr < f and 0 <= nc < c and laberinto[nr][nc] == EDIFICIO:
                # Quitar la pared intermedia
                laberinto[r + dr//2][col + dc//2] = CAMINO
                cavar(nr, nc)

    # 2. Empezar a cavar desde una posición aleatoria (siempre impar)
    cavar(1, 1)

    # 3. CREAR MÚLTIPLES CAMINOS (Braiding)
    # Rompemos paredes extra según el factor de complejidad
    for i in range(1, f - 1):
        for j in range(1, c - 1):
            if laberinto[i][j] == EDIFICIO:
                if random.random() < complejidad:
                    laberinto[i][j] = CAMINO

    return laberinto

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

# Uso del generador
f = 8#int(input("Filas: "))
c = 8#int(input("Columnas: "))
# Complejidad 0.1 significa que romperá el 10% de las paredes restantes
mi_laberinto = generar_laberinto_dinamico(f, c, complejidad=0.2)
mi_laberinto[1][1] = ENTRADA
mi_laberinto[6][3] = SALIDA
imprimir_laberinto(mi_laberinto)