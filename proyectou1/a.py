import pygame
import heapq

# Configuraciones iniciales
ANCHO_VENTANA = 500
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        """
        Inicializa un Nodo con su posición en la cuadrícula, su ancho y el total de filas.
        Inicializa también los valores de distancia desde el nodo de inicio (g), heurística (h)
        y costo total estimado (f) en infinito y el padre en None.
        """
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.g = float('inf')  # Distancia desde el nodo de inicio
        self.h = float('inf')  # Heurística (distancia estimada al objetivo)
        self.f = float('inf')  # g + h, costo total estimado
        self.padre = None

    def get_pos(self):
        """
        Devuelve la posición (fila, columna) del nodo en la cuadrícula.
        """
        return self.fila, self.col

    def es_pared(self):
        """
        Verifica si el nodo es una pared.
        
        Un nodo es considerado una pared si su color es Negro.
        """
        return self.color == NEGRO

    def es_inicio(self):
        """
        Verifica si el nodo es el de inicio.
        
        El nodo es considerado de inicio si su color es Naranja.
        """
        return self.color == NARANJA

    def es_fin(self):
        """
        Verifica si el nodo es el de fin.
        
        El nodo es considerado de fin si su color es Púrpura.
        """
        return self.color == PURPURA
      
    def __lt__(self, other):
        """
        Compara dos nodos según su costo total estimado (f).

        El nodo con menor costo total estimado es considerado "menor".
        Esto se utiliza para que la cola de prioridad (heap) devuelva el nodo con menor costo total estimado primero.

        :param other: El otro nodo para comparar.
        :return: True si self.f < other.f, False en caso contrario.
        """
        return self.f < other.f

    def restablecer(self):
        """
        Restablece el color del nodo a Blanco, lo que significa que no es un nodo de inicio, fin o pared.
        """
        self.color = BLANCO

    def hacer_inicio(self):
        """
        Marca el nodo como nodo de inicio.
        
        El nodo es considerado de inicio si su color es Naranja.
        """
        self.color = NARANJA

    def hacer_pared(self):
        """
        Marca el nodo como pared.
        
        El nodo es considerado una pared si su color es Negro.
        """
        self.color = NEGRO

    def hacer_fin(self):
        
        """
        Marca el nodo como nodo de fin.
        
        El nodo es considerado de fin si su color es Púrpura.
        """
        self.color = PURPURA

    def hacer_cerrado(self):
        """
        Marca el nodo como "cerrado" en la búsqueda.
        
        Un nodo es considerado "cerrado" cuando ha sido explorado y no se
        requiere volver a explorarlo.
        """
        self.color = ROJO

    def hacer_abierto(self):
        """
        Marca el nodo como "abierto" en la búsqueda.
        
        Un nodo es considerado "abierto" cuando ha sido agregado a la cola de prioridad
        y está pendiente de ser explorado.
        """
        self.color = VERDE

    def hacer_camino(self):
        """
        Marca el nodo como parte del camino encontrado.
        
        El nodo es dibujado de color Azul para indicar que es parte del camino
        encontrado por el algoritmo de búsqueda.
        """
        self.color = AZUL

    def dibujar(self, ventana):
        """
        Dibuja el nodo en la ventana.

        Parameters:
        ventana (pygame.display): Ventana en la que se dibujará el nodo
        """
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

def crear_grid(filas, ancho):
    """
    Crea una grilla de nodos con la cantidad de filas y columnas
    especificadas y el ancho especificado.

    Parameters:
    filas (int): Número de filas en la grilla
    ancho (int): Ancho de la ventana en píxeles

    Returns:
    list: La grilla de nodos, donde cada nodo es un objeto de la clase Nodo
    """
    
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    """
    Dibuja las lineas que dividen la grilla en la ventana.

    Parameters:
    ventana (pygame.display): Ventana en la que se dibujará la grilla
    filas (int): Número de filas en la grid
    ancho (int): Ancho de la ventana en píxeles
    """
    
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    """
    Dibuja la grilla en la ventana. Primero limpia la ventana de cualquier contenido
    previo y luego dibuja cada nodo en la grilla y las lineas que lo dividen.
    """
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    """
    Convierte una posición de click en pantalla en una posición en la grid.

    Parameters:
    pos (tuple): Posición del click en pantalla como (y, x)
    filas (int): Número de filas en la grid
    ancho (int): Ancho de la ventana en píxeles

    Returns:
    tuple: Posición en la grid como (fila, columna)
    """
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def heuristica(nodo1, nodo2):
    # Distancia Manhattan
    """
    Calcula la distancia de Manhattan entre dos nodos.

    :param nodo1: El primer nodo.
    :param nodo2: El segundo nodo.
    :return: La distancia de Manhattan entre los dos nodos.
    """
    x1, y1 = nodo1.get_pos()
    x2, y2 = nodo2.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruir_camino(nodo_actual, dibujar):
    """
    Reconstruye el camino desde el nodo actual hasta el nodo de inicio.

    :param nodo_actual: El nodo actual en el camino.
    :param dibujar: La función para dibujar el camino.
    """
    while nodo_actual.padre:
        nodo_actual.hacer_camino()
        nodo_actual = nodo_actual.padre
        dibujar()

def algoritmo_a_star(dibujar, grid, inicio, fin):
    # Inicializar el nodo de inicio
    """
    Implementación del algoritmo A* para encontrar el camino más corto entre dos nodos en una grilla.

    Args:
        dibujar (function): Función para dibujar la grilla y los nodos.
        grid (list of list of Nodo): Grilla de nodos.
        inicio (Nodo): Nodo de inicio.
        fin (Nodo): Nodo de fin.

    Returns:
        bool: True si se encontró un camino, False de lo contrario.
    """
    inicio.g = 0
    inicio.h = heuristica(inicio, fin)
    inicio.f = inicio.g + inicio.h

    open_list = []
    heapq.heappush(open_list, (inicio.f, inicio))
    open_set = {inicio}

    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        nodo_actual = heapq.heappop(open_list)[1]
        open_set.remove(nodo_actual)

        if nodo_actual == fin:
            reconstruir_camino(fin, dibujar)
            return True

        for vecino in obtener_vecinos(nodo_actual, grid):
            if vecino.es_pared():
                continue

            temp_g = nodo_actual.g + 1  # Suponemos que el costo entre nodos adyacentes es 1

            if temp_g < vecino.g:
                vecino.padre = nodo_actual
                vecino.g = temp_g
                vecino.h = heuristica(vecino, fin)
                vecino.f = vecino.g + vecino.h

                if vecino not in open_set:
                    heapq.heappush(open_list, (vecino.f, vecino))
                    open_set.add(vecino)
                    vecino.hacer_abierto()

        dibujar()

        if nodo_actual != inicio:
            nodo_actual.hacer_cerrado()

    return False

def obtener_vecinos(nodo, grid):
    """
    Devuelve una lista con los vecinos de un nodo en una grid.
    
    El orden de los vecinos es: abajo, arriba, derecha, izquierda.
    
    :param nodo: El nodo del que se desean obtener los vecinos.
    :type nodo: Nodo
    :param grid: La grid en la que se encuentra el nodo.
    :type grid: list[list[Nodo]]
    :return: Una lista con los vecinos del nodo.
    :rtype: list[Nodo]
    """
    vecinos = []
    filas = len(grid)
    x, y = nodo.get_pos()

    if x < filas - 1:  # Abajo
        vecinos.append(grid[x + 1][y])
    if x > 0:  # Arriba
        vecinos.append(grid[x - 1][y])
    if y < filas - 1:  # Derecha
        vecinos.append(grid[x][y + 1])
    if y > 0:  # Izquierda
        vecinos.append(grid[x][y - 1])

    return vecinos

def main(ventana, ancho):
    FILAS = 11
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True
    iniciado = False

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and inicio and fin and not iniciado:
                    for fila in grid:
                        for nodo in fila:
                            nodo.g = float('inf')
                            nodo.h = float('inf')
                            nodo.f = float('inf')
                            nodo.padre = None
                    algoritmo_a_star(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)
                    iniciado = True

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
