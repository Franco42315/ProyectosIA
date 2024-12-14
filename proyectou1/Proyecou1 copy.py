import pygame  # Importa la biblioteca pygame para manejar gráficos y eventos.
import heapq  # Importa heapq para gestionar una lista de prioridades (cola de prioridad) en el algoritmo A*.
import time   # Importa time para manejar pausas en la ejecución del código.

# Configuración de la ventana

ANCHO_VENTANA = 500  # Define el ancho de la ventana en píxeles.
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))  # Crea una ventana cuadrada.
pygame.display.set_caption("Visualización de Nodos con A*")  # Título de la ventana.

pygame.font.init()  # Inicializa los módulos de fuente de pygame.
FUENTE = pygame.font.SysFont('Arial', 12)  # Fuente para mostrar texto en pantalla.


# Definición de colores en RGB
BLANCO = (255, 255, 255)  # Color blanco para nodos sin estado.
NEGRO = (0, 0, 0)         # Color negro para nodos que son "pared".
GRIS = (128, 128, 128)     # Gris para las líneas de la cuadrícula.
VERDE = (0, 255, 0)        # Verde para los nodos abiertos (explorables).
ROJO = (255, 0, 0)         # Rojo para los nodos cerrados (ya evaluados).
NARANJA = (255, 165, 0)    # Naranja para el nodo de inicio.
PURPURA = (128, 0, 128)    # Púrpura para el nodo de fin.
AZUL = (0, 0, 255)         # Azul para el camino final encontrado.
AMARILLO = (255, 255, 0)   # Color opcional para otros elementos.
CYAN = (0, 255, 255)       # Cyan para uso opcional.

# Representación de la cuadrícula

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        # Posición y atributos iniciales del nodo
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        # Valores para el algoritmo A*
        self.g = float('inf')  # Costo desde el inicio hasta el nodo
        self.h = float('inf')  # Heurística estimada hasta el nodo final
        self.f = float('inf')  # Costo total estimado (g + h)
        self.padre = None      # Nodo predecesor para reconstruir el camino

# Métodos de Nodo para definir y vefificar el estado del nodo

    def get_pos(self):
        return self.fila, self.col  # Retorna la posición en la cuadrícula.

    def es_pared(self):
        return self.color == NEGRO  # Verifica si el nodo es una pared.

    def es_inicio(self):
        return self.color == NARANJA  # Verifica si el nodo es el inicio.

    def es_fin(self):
        return self.color == PURPURA  # Verifica si el nodo es el final.

    def restablecer(self):
        self.color = BLANCO  # Restablece el color del nodo.

    def hacer_inicio(self):
        self.color = NARANJA  # Define el nodo como inicio.

    def hacer_pared(self):
        self.color = NEGRO  # Define el nodo como una pared.

    def hacer_fin(self):
        self.color = PURPURA  # Define el nodo como final.

    def hacer_cerrado(self):
        if not self.es_inicio() and not self.es_fin():
            self.color = ROJO  # Define el nodo como cerrado.

    def hacer_abierto(self):
        if not self.es_inicio() and not self.es_fin():
            self.color = VERDE  # Define el nodo como abierto.

    def hacer_camino(self):
        if not self.es_inicio() and not self.es_fin():
            self.color = AZUL  # Define el nodo como parte del camino final.

# Dibujar el nodo en la ventana con los valores g, h y f

    def dibujar(self, ventana):      
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))  # Dibuja el nodo.
        # Si el nodo tiene valores, muestra los costos g, h, y f.
        if self.g != float('inf') and self.h != float('inf') and self.f != float('inf'):
            texto_g = FUENTE.render(f'g:{self.g}', True, NEGRO)
            texto_h = FUENTE.render(f'h:{self.h}', True, NEGRO)
            texto_f = FUENTE.render(f'f:{self.f}', True, NEGRO)
            ventana.blit(texto_g, (self.x + 2, self.y + 2))
            ventana.blit(texto_h, (self.x + 2, self.y + 14))
            ventana.blit(texto_f, (self.x + 2, self.y + 26))

    def __lt__(self, other):
        return self.f < other.f  # Define el operador '<' en base al valor f.

# Funciones para manejar la cuadrícula y dibujar la interfaz
def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas  # Calcula el tamaño de cada nodo.
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)  # Crea un nodo por cada posición.
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas  # Dibuja las líneas de la cuadrícula.
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)  # Rellena el fondo de la ventana en blanco.
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)  # Dibuja cada nodo en la ventana.
    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()  # Actualiza la ventana.

# Obtener la posición en la cuadricula a partir del clic del usuario

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas  # Calcula el tamaño de cada nodo.
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col


# Heurística de Manhattan para el algoritmo A* ###########################

def heuristica(nodo1, nodo2):
    x1, y1 = nodo1.get_pos()
    x2, y2 = nodo2.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)  # Distancia Manhattan

# Reconstrucción del camino final encontrado por el algoritmo A* ####################

def reconstruir_camino(nodo_actual, dibujar, ventana, grid, filas, ancho):
    camino = []
    while nodo_actual.padre:
        camino.append(nodo_actual.get_pos())  # Agrega cada nodo hasta llegar al inicio.
        nodo_actual = nodo_actual.padre
    camino.reverse()  # Invierte el camino para mostrar desde inicio a fin.
    print("Camino final encontrado:", camino)
    for pos in camino:
        fila, col = pos
        grid[fila][col].hacer_camino()  # Muestra el camino en azul.
        dibujar()
        pygame.display.update()
        time.sleep(0.5)  # Pausa para visualizar el camino

