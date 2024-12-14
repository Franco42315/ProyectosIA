import json
import os
import requests

# Crear la carpeta "136x136" si no existe
dirname = 'jadePintRaw'
os.makedirs(dirname, exist_ok=True)

# Cargar el archivo JSON con los datos
with open('datasetPintJadePlant.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Extraer las URLs de las imágenes con etiqueta "136x136"
for pin in data:
    if 'images' in pin and '136x136' in pin['images']:
        image_url = pin['images']['136x136']['url']
        
        # Obtener el nombre del archivo de la URL
        image_name = image_url.split('/')[-1]
        
        # Descargar la imagen
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(os.path.join(dirname, image_name), 'wb') as file:
                file.write(response.content)
            print(f"Imagen descargada: {image_name}")
        else:
            print(f"Error al descargar la imagen: {image_url}")

print("Descarga completada.")
