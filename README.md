# 🧩 La Última Ruta: Laberinto con Dijkstra y A\*

## 📌 Descripción

Este proyecto implementa un sistema de generación y resolución de
laberintos utilizando algoritmos de búsqueda de caminos, principalmente
**Dijkstra** y preparado para **A\***.

El enfoque está basado en **Programación Orientada a Objetos (POO)**,
aplicando buenas prácticas de diseño como separación de
responsabilidades, encapsulamiento y composición.

------------------------------------------------------------------------

## 🎯 Objetivos

-   Implementar un generador de laberintos basado en DFS
-   Resolver el camino óptimo utilizando Dijkstra
-   Diseñar una arquitectura extensible para nuevos algoritmos (como
    A\*)
-   Aplicar principios SOLID en un caso práctico

------------------------------------------------------------------------

## 🏗️ Arquitectura del Proyecto

El sistema está dividido en componentes desacoplados mediante
**composición**:

### Laberinto

-   Gestiona la estructura de datos (matriz)
-   Controla acceso y modificaciones

### GeneradorLaberinto

-   Genera el laberinto utilizando DFS
-   Permite variabilidad mediante caminos adicionales

### ImpresorLaberinto

-   Encargado de la visualización en consola

### EditorLaberinto

-   Inserta elementos dinámicos:
    -   Inicio
    -   Fin
    -   Obstáculos
    -   Agua

### BuscadorCamino (Abstracto)

-   Define la interfaz para algoritmos de búsqueda

### BuscadorDijkstra

-   Implementa búsqueda de costo mínimo
-   Maneja pesos por tipo de celda

### AplicacionLaberinto

-   Orquesta el flujo del programa
-   Coordina los distintos componentes

------------------------------------------------------------------------

## 🧠 Principios de Diseño Aplicados

-   **SRP (Single Responsibility Principle)**: Cada clase tiene una
    única responsabilidad
-   **Encapsulamiento**: Protección de atributos internos
-   **Abstracción**: Interfaces claras entre componentes
-   **Polimorfismo**: Posibilidad de intercambiar algoritmos de búsqueda
-   **Composición**: Construcción del sistema a partir de objetos

------------------------------------------------------------------------

## ⚙️ Algoritmos

### Dijkstra

Algoritmo de búsqueda de caminos óptimos en grafos con pesos positivos.

-   Complejidad: O((V + E) log V)
-   Garantiza el costo mínimo

### A\* (Extensión)

Permite optimizar la búsqueda usando heurísticas:

f(n) = g(n) + h(n)

------------------------------------------------------------------------

## ▶️ Ejecución

``` bash
python main.py
```

------------------------------------------------------------------------

## 📊 Ejemplo de Salida

-   Laberinto generado aleatoriamente
-   Ruta óptima marcada
-   Costo total del recorrido

------------------------------------------------------------------------

## 🚀 Posibles Mejoras

-   Implementación completa de A\*
-   Visualización gráfica
-   Exportación de resultados
-   Pruebas unitarias
-   Configuración dinámica de costos

------------------------------------------------------------------------

## 📌 Notas

Este proyecto fue desarrollado como práctica de estructuras de datos,
algoritmos y diseño orientado a objetos.
