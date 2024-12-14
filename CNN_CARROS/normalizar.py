import os
from skimage.io import imread, imsave
from skimage.transform import resize
import numpy as np


def normalize_images(input_folder, output_folder, target_size=(128, 128)):
    """
    Normaliza las imágenes de una carpeta especificada redimensionándolas a un tamaño fijo
    y guardándolas en una nueva carpeta sin perder calidad visual.

    :param input_folder: Ruta de la carpeta con las imágenes originales.
    :param output_folder: Ruta de la carpeta para guardar las imágenes normalizadas.
    :param target_size: Tamaño al que se redimensionarán las imágenes (alto, ancho).
    """
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Recorrer las imágenes en la carpeta de entrada
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            try:
                # Leer la imagen
                image = imread(input_path)
                
                # Validar que la imagen tenga al menos 2 dimensiones (no esté corrupta)
                if image.ndim < 2:
                    print(f"Imagen no válida (menos de 2D): {filename}")
                    continue
                
                # Redimensionar la imagen al tamaño deseado
                image_resized = resize(
                    image, 
                    target_size, 
                    anti_aliasing=True, 
                    preserve_range=True
                )
                
                # Convertir la imagen a uint8 para guardar correctamente
                image_resized = np.clip(image_resized, 0, 255).astype(np.uint8)
                
                # Guardar la imagen redimensionada
                imsave(output_path, image_resized)
                print(f"Procesada: {filename} -> Guardada en {output_folder}")
            except Exception as e:
                print(f"Error al procesar {filename}: {e}")
    
    print(f"Todas las imágenes han sido normalizadas y guardadas en: {output_folder}")


# Ejemplo de uso
input_folder = "C:/Users/Leonardo/Desktop/CNN Dataset/dataset/vocho"
output_folder = "C:/Users/Leonardo/Desktop/CNN_CARROS/dataset/vocho"
normalize_images(input_folder, output_folder)
