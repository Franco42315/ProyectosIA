import os

def renombrar_imagenes(carpeta, numero_inicial):
    """
    Renombra todas las imágenes en una carpeta con el formato `img_XXXX` empezando desde un número inicial.

    Args:
        carpeta (str): Ruta de la carpeta donde se encuentran las imágenes.
        numero_inicial (int): Número inicial para los nombres de las imágenes.

    Returns:
        None
    """
    # Extensiones comunes de imágenes
    extensiones_validas = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff','webm']
    
    try:
        # Obtener lista de archivos en la carpeta
        archivos = os.listdir(carpeta)
        
        # Filtrar solo archivos con extensiones válidas
        imagenes = [archivo for archivo in archivos if os.path.splitext(archivo)[1].lower() in extensiones_validas]
        
        if not imagenes:
            print("No se encontraron imágenes en la carpeta especificada.")
            return

        # Renombrar imágenes
        for indice, imagen in enumerate(imagenes):
            # Construir el nuevo nombre con el formato `img_XXXX`
            nueva_imagen = f"img_{numero_inicial + indice:04d}{os.path.splitext(imagen)[1]}"
            
            # Rutas completas
            ruta_vieja = os.path.join(carpeta, imagen)
            ruta_nueva = os.path.join(carpeta, nueva_imagen)
            
            # Renombrar el archivo
            os.rename(ruta_vieja, ruta_nueva)
            print(f"Renombrado: {imagen} -> {nueva_imagen}")
        
        print(f"Renombradas {len(imagenes)} imágenes exitosamente.")
    
    except Exception as e:
        print(f"Error al renombrar las imágenes: {e}")

# Ejemplo de uso
#carpeta = r"C:/Users/Leonardo/Desktop/CNN_CARROS/prueba/dataset/originales/bocho"  # Cambia esta ruta por la ubicación de tu carpeta
#carpeta = r"C:/VS/IA/generador/dataset"  # Cambia esta ruta por la ubicación de tu carpeta
carpeta = r"C:/Users/Leonardo/Desktop/dataset/tsuru"
numero_inicial = 1  # Cambia este número para iniciar desde un número específico

renombrar_imagenes(carpeta, numero_inicial)
