import pygame
import random
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.models import Sequential
from keras.layers import Dense, Input
import sys
sys.stdout.reconfigure(encoding='utf-8')
########################################################################################################################
#- Configuración del juego##############################################################################################
########################################################################################################################

pygame.init()
w, h = 800, 400
pantalla = pygame.display.set_mode((w, h))
pygame.display.set_caption("Juego: Disparo de Bala, Salto, Nave y Menú")
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
jugador = None
bala = None
fondo = None
nave = None
menu = None
salto = False
salto_altura = 15
gravedad = 1
en_suelo = True
pausa = False
fuente = pygame.font.SysFont('Arial', 24)
menu_activo = True
datos_modelo = [] # Lista para guardar los datos de velocidad, distancia y salto (target)
########################################################################################################################
modelo_entrenado = None
modelo_arbol_entrenado = None
intervalo_salto_red = 1  # Ejecutar salto_red cada 10 frames
contador_salto_red = 0
modo_auto = False  # Indica si el modo de juego es automático
modo_arbol = False
########################################################################################################################
jugador_frames = [
    pygame.image.load('assets/sprites/mono_frame_1.png'),
    pygame.image.load('assets/sprites/mono_frame_2.png'),
    pygame.image.load('assets/sprites/mono_frame_3.png'),
    pygame.image.load('assets/sprites/mono_frame_4.png')
]
bala_img = pygame.image.load('assets/sprites/purple_ball.png')
fondo_img = pygame.image.load('assets/game/fondo2.png')
nave_img = pygame.image.load('assets/game/ufo.png')
menu_img = pygame.image.load('assets/game/menu.png')
fondo_img = pygame.transform.scale(fondo_img, (w, h)) # Escalar la imagen 
# Crear el rectángulo del jugador y de la bala
jugador = pygame.Rect(50, h - 100, 32, 48)
bala = pygame.Rect(w - 50, h - 90, 16, 16)
nave = pygame.Rect(w - 100, h - 100, 64, 64)
menu_rect = pygame.Rect(w // 2 - 135, h // 2 - 90, 270, 180)  # Tamaño del menú
# Variables para la animación del jugador
current_frame = 0
frame_speed = 10  # Cuántos frames antes de cambiar a la siguiente imagen
frame_count = 0
# Variables para la bala
velocidad_bala = -10  # Velocidad de la bala hacia la izquierda
bala_disparada = False
# Variables para el fondo en movimiento
fondo_x1 = 0
fondo_x2 = w

########################################################################################################################
#- Función para disparar bala ##########################################################################################
########################################################################################################################
def disparar_bala():
    global bala_disparada, velocidad_bala
    if not bala_disparada:
        velocidad_bala = random.randint(-15, -5)  # Velocidad aleatoria negativa para la bala
        bala_disparada = True
########################################################################################################################
#- Función para resetear bala ##########################################################################################
########################################################################################################################
def reset_bala():
    global bala, bala_disparada
    bala.x = w - 50  # Reiniciar la posición de la bala
    bala_disparada = False
########################################################################################################################
#- Función para manejar salto ##########################################################################################
########################################################################################################################
def manejar_salto():
    global jugador, salto, salto_altura, gravedad, en_suelo

    if salto:
        jugador.y -= salto_altura  # Mover al jugador hacia arriba
        salto_altura -= gravedad  # Aplicar gravedad (reduce la velocidad del salto)

        # Si el jugador llega al suelo, detener el salto
        if jugador.y >= h - 100:
            jugador.y = h - 100
            salto = False
            salto_altura = 15  # Restablecer la velocidad de salto
            en_suelo = True
########################################################################################################################
#- Función para actualizar juego########################################################################################
########################################################################################################################
def update():
    global bala, velocidad_bala, current_frame, frame_count, fondo_x1, fondo_x2
    # Mover el fondo
    fondo_x1 -= 1
    fondo_x2 -= 1
    # Si el primer fondo sale de la pantalla, lo movemos detrás del segundo
    if fondo_x1 <= -w:
        fondo_x1 = w
    # Si el segundo fondo sale de la pantalla, lo movemos detrás del primero
    if fondo_x2 <= -w:
        fondo_x2 = w
    # Dibujar los fondos
    pantalla.blit(fondo_img, (fondo_x1, 0))
    pantalla.blit(fondo_img, (fondo_x2, 0))
    # Animación del jugador
    frame_count += 1
    if frame_count >= frame_speed:
        current_frame = (current_frame + 1) % len(jugador_frames)
        frame_count = 0
    # Dibujar el jugador con la animación
    pantalla.blit(jugador_frames[current_frame], (jugador.x, jugador.y))

    # Dibujar la nave
    pantalla.blit(nave_img, (nave.x, nave.y))

    # Mover y dibujar la bala
    if bala_disparada:
        bala.x += velocidad_bala

    # Si la bala sale de la pantalla, reiniciar su posición
    if bala.x < 0:
        reset_bala()

    pantalla.blit(bala_img, (bala.x, bala.y))

    # Colisión entre la bala y el jugador
    if jugador.colliderect(bala):
        print("Colisión detectada!")
        # Verificar que NO se esté en modo_arbol ni en modo_auto
        if not modo_arbol and not modo_auto:  
            fit_red()
            fit_arbol()
        reiniciar_juego()  # Terminar el juego y mostrar el menú
########################################################################################################################
#- Función para guardar datos ##########################################################################################
########################################################################################################################
def guardar_datos():
    global jugador, bala, velocidad_bala, salto
    distancia = abs(jugador.x - bala.x)
    salto_hecho = 1 if salto else 0  # 1 si saltó, 0 si no saltó
    # Guardar velocidad de la bala, distancia al jugador y si saltó o no
    datos_modelo.append((velocidad_bala, distancia, salto_hecho))
########################################################################################################################
#- Función para pausar juego ##########################################################################################
########################################################################################################################
def pausa_juego():
    global pausa
    pausa = not pausa
    if pausa:
        print("Juego pausado. Datos registrados hasta ahora:", datos_modelo)
    else:
        print("Juego reanudado.")
########################################################################################################################
#- Función para mostrar menú ###########################################################################################
########################################################################################################################
def mostrar_menu():
    global menu_activo, modo_auto, modo_arbol, datos_modelo, modelo_entrenado, modelo_arbol_entrenado
    pantalla.fill(NEGRO)
    opciones = [
        "Menú principal, presiona una tecla:",
        "",
        "\"M\" Modo Manual",
        "\"A\" Modo Automático",
        "",
        "\"L\" Limpiar Datos",
        "",
        "\"G\" Graficar dataset",
        "\"T\" Modo Árbol",
        "",
        "\"R\" Reiniciar",
        "\"Q\" Salir"
    ]
    # Coordenadas iniciales
    x = w // 20
    y_inicial = h // 18  # Altura inicial para las opciones
    espaciado = h // 15  # Espaciado entre líneas
    # Renderizar cada opción
    for i, texto in enumerate(opciones):
        texto_renderizado = fuente.render(texto, True, BLANCO)
        pantalla.blit(texto_renderizado, (x, y_inicial + i * espaciado))
    pygame.display.flip()
    
    # Ciclo principal del menú
    while menu_activo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                # Salir del juego
                print("Saliendo del juego...")
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:
                    # Activar modo automático
                    print("Modo automático seleccionado.")
                    modo_auto = True
                    modo_arbol = False
                    menu_activo = False

                elif evento.key == pygame.K_m:
                    # Activar modo manual
                    print("Modo manual seleccionado.")
                    modo_auto = False
                    modo_arbol = False
                    menu_activo = False

                elif evento.key == pygame.K_t:
                    # Activar modo árbol de decisiones
                    print("Modo árbol de decisiones seleccionado.")
                    modo_auto = False
                    modo_arbol = True
                    menu_activo = False

                elif evento.key == pygame.K_l:
                    # Limpiar datos de entrenamiento
                    print("Limpiando datos de entrenamiento...")
                    datos_modelo = []  # Reiniciar datos
                    modelo_entrenado = None
                    modelo_arbol_entrenado = None
                    print("Datos limpiados.")
                    mostrar_menu()  # Volver a mostrar el menú

                elif evento.key == pygame.K_g:
                    # Visualizar los datos recopilados
                    print("Generando gráfico de datos recopilados...")
                    if datos_modelo:
                        # Descomponer los datos para graficar
                        x = [d[0] for d in datos_modelo]  # Velocidad
                        y = [d[1] for d in datos_modelo]  # Distancia
                        z = [d[2] for d in datos_modelo]  # Salto

                        # Crear una gráfica 3D
                        fig = plt.figure()
                        ax = fig.add_subplot(111, projection='3d')
                        ax.scatter(x, y, z, c='r', marker='o')
                        ax.set_xlabel('Velocidad')
                        ax.set_ylabel('Distancia')
                        ax.set_zlabel('Salto')

                        # Mostrar gráfica
                        plt.show()
                    else:
                        print("No hay datos recopilados para graficar.")


                elif evento.key == pygame.K_q:
                    # Salir del juego
                    # print("Finalizando el juego. Datos recopilados:", len(datos_modelo))
                    pygame.quit()
                    exit()
########################################################################################################################
#- Función para entrenar modelo ########################################################################################
########################################################################################################################
def fit_red():
    global modelo_entrenado, datos_modelo

    # Validar que hay suficientes datos para entrenar
    if len(datos_modelo) < 2:
        print("No hay suficientes datos para entrenar el modelo.")
        return

    # Convertir datos a numpy arrays
    datos = np.array(datos_modelo)
    x = datos[:, :2]  # Velocidad y distancia
    y = datos[:, 2].astype(int)  # Salto (asegurar que sea entero para clasificación)

    # Dividir los datos en conjuntos de entrenamiento y prueba
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Definir dimensiones y número de clases
    input_dim = x.shape[1]  # Número de características
    num_classes = len(np.unique(y))  # Número de clases únicas

    # Definición del modelo secuencial
    modelo = Sequential([
        Input(shape=(input_dim,)),  # Definir la dimensión de entrada
        Dense(units=64, activation='relu'),
        Dense(units=32, activation='relu'),
        Dense(units=num_classes, activation='softmax')  # Para múltiples clases
    ])

    # Compilar el modelo
    modelo.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',  # Para clasificación con etiquetas enteras
        metrics=['accuracy']
    )

    # Entrenamiento del modelo
    modelo.fit(
        x_train,  # Características de entrada
        y_train,  # Etiquetas de salida
        epochs=100,
        batch_size=32,
        verbose=1
    )

    # Evaluar el modelo
    loss, accuracy = modelo.evaluate(x_test, y_test, verbose=0)
    print(f"Modelo entrenado con precisión: {accuracy:.2f}, Pérdida: {loss:.2f}")

    modelo_entrenado = modelo
########################################################################################################################
#- Función para decidir salto ##########################################################################################
########################################################################################################################
def salto_red():
    global modelo_entrenado, salto, en_suelo
    if modelo_entrenado is None:
        print("Modelo no entrenado. No se puede decidir.")
        return

    # Calcular características de entrada
    try:
        distancia = abs(jugador.x - bala.x)
        entrada = np.array([[velocidad_bala, distancia]])  # Formato de entrada para el modelo
    except AttributeError as e:
        print(f"Error al calcular la entrada: {e}")
        return

    # Hacer predicción con el modelo
    try:
        prediccion = modelo_entrenado.predict(entrada, verbose=0)
        clase_predicha = np.argmax(prediccion)  # Seleccionar la clase con mayor probabilidad

        if clase_predicha == 1 and en_suelo:  # Supongamos que 1 significa "saltar"
            salto = True
            en_suelo = False
            print("Saltar")
        else:
            print("No saltar")
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")
########################################################################################################################
#- Función para entrenar modelo arbol ##################################################################################
########################################################################################################################        
def fit_arbol():
    global modelo_entrenado_arbol, datos_modelo

    # Validar que hay suficientes datos para entrenar
    if len(datos_modelo) < 2:
        print("No hay suficientes datos para entrenar el modelo.")
        return

    # Convertir datos en DataFrame
    dataset = pd.DataFrame(datos_modelo, columns=['Velocidad', 'Distancia', 'Salto'])
    X = dataset[['Velocidad', 'Distancia']]  # Características de entrada
    y = dataset['Salto']  # Etiquetas

    # Dividir datos en entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=44)

    # Crear y entrenar el modelo
    clf = DecisionTreeClassifier(max_depth=5, random_state=44)
    clf.fit(X_train, y_train)

    # Evaluar el modelo
    accuracy = clf.score(X_test, y_test)
    print(f"Modelo de árbol entrenado con precisión: {accuracy:.2f}")

    modelo_entrenado_arbol = clf

########################################################################################################################
#- Función para decidir salto arbol ####################################################################################
########################################################################################################################
def salto_arbol():
    global modelo_entrenado_arbol, salto, en_suelo

    # Validar que el modelo está entrenado
    if modelo_entrenado_arbol is None:
        print("Modelo no entrenado. No se puede decidir.")
        return

    # Validar que las variables necesarias existen
    try:
        distancia = abs(jugador.x - bala.x)
        entrada = pd.DataFrame([[velocidad_bala, distancia]], columns=['Velocidad', 'Distancia'])
    except AttributeError as e:
        print(f"Error al calcular la entrada: {e}")
        return

    # Realizar la predicción
    try:
        prediccion = modelo_entrenado_arbol.predict(entrada)[0]
        if prediccion == 1 and en_suelo and distancia < 100:
            salto = True
            en_suelo = False
            print("Saltar")
        else:
            print("No saltar")
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")

########################################################################################################################
#- Función para reiniciar juego ########################################################################################
########################################################################################################################
def reiniciar_juego():
    global menu_activo, jugador, bala, nave, bala_disparada, salto, en_suelo
    menu_activo = True  # Activar de nuevo el menú
    jugador.x, jugador.y = 50, h - 100  # Reiniciar posición del jugador
    bala.x = w - 50  # Reiniciar posición de la bala
    nave.x, nave.y = w - 100, h - 100  # Reiniciar posición de la nave
    bala_disparada = False
    salto = False
    en_suelo = True
    # Mostrar los datos recopilados hasta el momento
    # print("Datos recopilados para el modelo: ", datos_modelo)
    mostrar_menu()  # Mostrar el menú de nuevo para seleccionar modo
########################################################################################################################
#- Función principal ###################################################################################################
########################################################################################################################
def main():
    global salto, en_suelo, bala_disparada, contador_salto_red

    reloj = pygame.time.Clock()
    mostrar_menu()  # Mostrar el menú al inicio
    correr = True

    while correr:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                correr = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and en_suelo and not pausa:  # Detectar la tecla espacio para saltar
                    salto = True
                    en_suelo = False
                if evento.key == pygame.K_p:  # Presiona 'p' para pausar el juego
                    pausa_juego()
                if evento.key == pygame.K_r:  # Presiona 'p' para pausar el juego
                    reiniciar_juego()
                if evento.key == pygame.K_q:  # Presiona 'q' para terminar el juego
                    print("Juego terminado. Datos recopilados:", datos_modelo)
                    pygame.quit()
                    exit()

        if not pausa:
            # Modo manual: el jugador controla el salto
            if not modo_auto or modo_arbol:
                if salto:
                    manejar_salto()
                # Guardar los datos si estamos en modo manual
                guardar_datos()

            if modo_auto:         
                
                if contador_salto_red >= intervalo_salto_red:
                    salto_red()
                    contador_salto_red = 0  # Reiniciar el contador
                else:
                    contador_salto_red += 1

                if salto:
                    manejar_salto()
            
            if modo_arbol:         
                
                if contador_salto_red >= intervalo_salto_red:
                    salto_arbol()
                    contador_salto_red = 0  # Reiniciar el contador
                else:
                    contador_salto_red += 1

                if salto:
                    manejar_salto()


            # Actualizar el juego
            if not bala_disparada:
                disparar_bala()
            update()

        # Actualizar la pantalla
        pygame.display.flip()
        reloj.tick(60)  # Limitar el juego a 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()
########################################################################################################################
#"""""""""""""""""""""""""""""""########################################################################################
########################################################################################################################