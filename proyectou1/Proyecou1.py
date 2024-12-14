import pygame
import heapq
import time

# Configuraciones iniciales
ANCHO_VENTANA = 500
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos con A*")

# Inicializar Pygame Font
pygame.font.init()
FUENTE = pygame.font.SysFont('Arial', 12)

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)
AMARILLO = (255, 255, 0)
CYAN = (0, 255, 255)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
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
        Marca el nodo como una pared.
        
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
        if not self.es_inicio() and not self.es_fin():
            self.color = ROJO

    def hacer_abierto(self):
        """
        Marca el nodo como "abierto" en la búsqueda.
        
        Un nodo es considerado "abierto" cuando ha sido agregado a la cola de prioridad
        y está pendiente de ser explorado.
        """
        if not self.es_inicio() and not self.es_fin():
            self.color = VERDE

    def hacer_camino(self):
        """
        Marca el nodo como parte del camino encontrado.
        
        El nodo es dibujado de color Azul para indicar que es parte del camino
        encontrado por el algoritmo de búsqueda.
        """
        if not self.es_inicio() and not self.es_fin():
            self.color = AZUL

    def dibujar(self, ventana):      
        """
        Dibuja el nodo en la ventana.

        El nodo es dibujado con su color actual y, si ha sido explorado,
        se dibujan también sus valores g, h y f en la esquina superior izquierda.
        """
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))
        if self.g != float('inf') and self.h != float('inf') and self.f != float('inf'):
            texto_g = FUENTE.render(f'g:{self.g}', True, NEGRO)
            texto_h = FUENTE.render(f'h:{self.h}', True, NEGRO)
            texto_f = FUENTE.render(f'f:{self.f}', True, NEGRO)
            ventana.blit(texto_g, (self.x + 2, self.y + 2))
            ventana.blit(texto_h, (self.x + 2, self.y + 14))
            ventana.blit(texto_f, (self.x + 2, self.y + 26))

    def __lt__(self, other):
        """
        Compara dos nodos según su costo total estimado (f).

        El nodo con menor costo total estimado es considerado "menor".
        Esto se utiliza para que la cola de prioridad (heap) devuelva el nodo con menor costo total estimado primero.

        :param other: El otro nodo para comparar.
        :return: True si self.f < other.f, False en caso contrario.
        """
        return self.f < other.f

def crear_grid(filas, ancho):
    """
    Crea una grilla de nodos con la cantidad de filas y columnas especificadas y el ancho especificado.

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
    Dibuja la grilla en la ventana. Primero limpia la ventana de cualquier contenido previo y luego dibuja cada nodo en la grilla y las lineas que lo dividen.
    
    Parameters:
    ventana (pygame.display): Ventana en la que se dibujará la grilla
    grid (list): La grilla de nodos, donde cada nodo es un objeto de la clase Nodo
    filas (int): Número de filas en la grid
    ancho (int): Ancho de la ventana en píxeles
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
    """
    Calcula la distancia de Manhattan entre dos nodos.

    Parameters:
    nodo1 (Nodo): El primer nodo.
    nodo2 (Nodo): El segundo nodo.

    Returns:
    int: La distancia de Manhattan entre los dos nodos.
    """
    x1, y1 = nodo1.get_pos()
    x2, y2 = nodo2.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruir_camino(nodo_actual, dibujar, ventana, grid, filas, ancho):
    """
    Reconstruye el camino desde el nodo actual hasta el nodo de inicio.

    Dado el nodo actual, reconstruye el camino hasta el nodo de inicio
    y lo dibuja en la ventana con una pausa para visualizar el camino.

    Parameters:
    nodo_actual (Nodo): El nodo actual en el camino
    dibujar (function): La función para dibujar la grilla y los nodos.
    ventana (pygame.display): La ventana en la que se dibujará el camino
    grid (list): La grilla de nodos
    filas (int): Número de filas en la grid
    ancho (int): Ancho de la ventana en píxeles
    """
    camino = []
    while nodo_actual.padre:
        camino.append(nodo_actual.get_pos())
        nodo_actual = nodo_actual.padre
    camino.reverse()
    print("Camino final encontrado:", camino)
    for pos in camino:
        fila, col = pos
        grid[fila][col].hacer_camino()
        dibujar()
        pygame.display.update()
        time.sleep(0.5)  # Pausa para visualizar el camino

def algoritmo_a_star(dibujar_func, grid, inicio, fin):
    """
    Implementa el algoritmo de A* para encontrar el camino más corto entre un nodo de inicio y un nodo de fin en una grilla.

    Parameters:
    dibujar_func (function): La función para dibujar la grilla y los nodos.
    grid (list): La grilla de nodos.
    inicio (Nodo): El nodo de inicio.
    fin (Nodo): El nodo de fin.

    Returns:
    bool: True si se encontró un camino, False en caso contrario.
    """
    inicio.g = 0
    inicio.h = heuristica(inicio, fin)
    inicio.f = inicio.g + inicio.h

    open_list = []
    heapq.heappush(open_list, (inicio.f, inicio))
    open_set = {inicio}
    closed_set = set()

    while open_list:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        nodo_actual = heapq.heappop(open_list)[1]
        open_set.remove(nodo_actual)
        closed_set.add(nodo_actual)

        if nodo_actual == fin:
            reconstruir_camino(nodo_actual, dibujar_func, VENTANA, grid, len(grid), ANCHO_VENTANA)
            return True

        for vecino in obtener_vecinos(nodo_actual, grid):
            if vecino.es_pared() or vecino in closed_set:
                continue

            temp_g = nodo_actual.g + 1

            if temp_g < vecino.g:
                vecino.padre = nodo_actual
                vecino.g = temp_g
                vecino.h = heuristica(vecino, fin)
                vecino.f = vecino.g + vecino.h

                if vecino not in open_set:
                    heapq.heappush(open_list, (vecino.f, vecino))
                    open_set.add(vecino)
                    vecino.hacer_abierto()

        dibujar_func()

        if nodo_actual != inicio:
            nodo_actual.hacer_cerrado()

        # Imprimir listas abierta y cerrada en la consola
        lista_abierta = sorted(open_set, key=lambda x: x.f)
        lista_cerrada = list(closed_set)

        print("\nLista Abierta:")
        print([nodo.get_pos() for nodo in lista_abierta])
        print("Lista Cerrada:")
        print([nodo.get_pos() for nodo in lista_cerrada])

        time.sleep(0.5)  # Esperar 0.05 segundos antes de continuar (ajusta el tiempo según prefieras)

    print("No se encontró un camino.")
    return False

def obtener_vecinos(nodo, grid):
    """
    Devuelve una lista con los vecinos de un nodo en una grid, incluyendo movimientos diagonales.

    :param nodo: El nodo del que se desean obtener los vecinos.
    :param grid: La grid en la que se encuentra el nodo.
    :return: Una lista con los vecinos del nodo.
    """
    vecinos = []
    filas = len(grid)
    x, y = nodo.get_pos()

    # Movimientos posibles: Abajo, Arriba, Derecha, Izquierda y Diagonales
    if x < filas - 1:  # Abajo
        vecinos.append(grid[x + 1][y])
    if x > 0:  # Arriba
        vecinos.append(grid[x - 1][y])
    if y < filas - 1:  # Derecha
        vecinos.append(grid[x][y + 1])
    if y > 0:  # Izquierda
        vecinos.append(grid[x][y - 1])

    # Movimientos diagonales
    if x < filas - 1 and y < filas - 1:  # Abajo-Derecha
        vecinos.append(grid[x + 1][y + 1])
    if x < filas - 1 and y > 0:  # Abajo-Izquierda
        vecinos.append(grid[x + 1][y - 1])
    if x > 0 and y < filas - 1:  # Arriba-Derecha
        vecinos.append(grid[x - 1][y + 1])
    if x > 0 and y > 0:  # Arriba-Izquierda
        vecinos.append(grid[x - 1][y - 1])

    return vecinos


def main(ventana, ancho):
    """
    Función principal del programa. Inicializa una grilla de nodos y gestiona los eventos de Pygame
    para dibujar la grilla y permitir al usuario interactuar con ella.

    El usuario puede clickear con el botón izquierdo para seleccionar el nodo de inicio y el nodo de fin.
    Puede clickear con el botón derecho para seleccionar los nodos que serán paredes.
    Puede presionar la tecla espacio para iniciar el algoritmo A*.

    La función devuelve None.
    """
    FILAS = 9
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
                    print("Iniciando algoritmo A*...")
                    encontrado = algoritmo_a_star(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)
                    if encontrado:
                        print("Camino encontrado.")
                    else:
                        print("No se encontró un camino.")
                    iniciado = True

    pygame.quit()

if __name__ == "__main__":
    main(VENTANA, ANCHO_VENTANA)

# ----------------------------------------------------------------------------------------------------------------------------------

# 1. Se define el nodo de inicio con un valor inicial g (distancia desde el inicio) de 0.
#    Su heurística h (distancia estimada al nodo final) se calcula usando la distancia de Manhattan.
#    f (costo total estimado) se define como la suma de g + h.

# 2. El nodo de inicio se coloca en una lista abierta (open_list), una estructura de cola de prioridad (usando heapq),
#    donde se almacenan los nodos pendientes de explorar, priorizando aquellos con el menor costo f.
#    También se guarda en un conjunto open_set para verificar si ya ha sido añadido.

# 3. Se inicia un bucle que continúa mientras haya nodos en la lista abierta.
#    En cada iteración se obtiene el nodo con menor valor de f (costo estimado) de la lista abierta.
#    Este nodo se convierte en el "nodo actual" y se marca como explorado moviéndolo de open_set a closed_set,
#    para evitar futuras exploraciones de este nodo.

# 4. Si el nodo actual es el nodo final, significa que se ha encontrado el camino óptimo.
#    En este caso, se llama a una función de reconstrucción para trazar el camino desde el nodo final hasta el nodo inicial.
#    Esto se hace retrocediendo a través de los nodos “padre” guardados de cada nodo en el camino.

# 5. Si el nodo actual no es el nodo final, se exploran sus vecinos (nodos adyacentes).
#    Para cada vecino, se omiten aquellos que son paredes o ya están en closed_set.

# 6. Se calcula un nuevo valor temporal g para cada vecino, sumando 1 al g del nodo actual.
#    Si este valor g temporal es menor que el g actual del vecino, se actualiza el valor g del vecino.
#    También se establece el nodo actual como el "padre" del vecino, permitiendo reconstruir el camino al final.

# 7. La heurística h del vecino (distancia al nodo final) se recalcula, y el valor f del vecino (g + h) se actualiza.

# 8. Si el vecino no está en open_set, se agrega a la lista abierta (open_list) y a open_set.
#    De esta forma, los vecinos con valores f más bajos se priorizan en la próxima iteración.

# 9. Una vez explorados todos los vecinos del nodo actual, el nodo se marca como "cerrado",
#    lo que indica visualmente que ha sido explorado.

# 10. Si se agotan los nodos de open_list sin haber encontrado un camino al nodo final,
#     el algoritmo termina indicando que no se encontró un camino.

# 11. Durante el proceso, el estado de la lista abierta y cerrada se imprime en consola,
#     proporcionando detalles de las posiciones de los nodos abiertos y cerrados.

# ----------------------------------------------------------------------------------------------------------------------------------
