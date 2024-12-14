import os
import requests
import base64
import json
import uuid

def download_images_from_files(json_file_paths, download_folder="img_json"):
    """
    Descarga imágenes desde varios archivos JSON que contienen URLs y datos base64.

    :param json_file_paths: Lista de rutas a archivos JSON con datos de imágenes.
    :param download_folder: Carpeta donde se guardarán las imágenes.
    """
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)  # Crear carpeta si no existe

    for file_path in json_file_paths:
        print(f"Procesando archivo: {file_path}")

        # Leer datos del archivo JSON
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except Exception as e:
            print(f"Error al leer el archivo {file_path}: {e}")
            continue

        for idx, item in enumerate(json_data):
            image_data = item.get("Imagen2")
            if not image_data:
                print(f"Item {idx + 1} en {file_path} no contiene datos de imagen.")
                continue

            unique_id = uuid.uuid4().hex  # Generar un identificador único

            if image_data.startswith("http"):
                # Procesar URL de imagen
                try:
                    response = requests.get(image_data, stream=True)
                    response.raise_for_status()  # Asegura que la respuesta es válida

                    # Extraer extensión de la imagen
                    file_extension = image_data.split(".")[-1].split('?')[0]
                    if file_extension not in ["jpg", "jpeg", "png", "gif", "webp"]:
                        file_extension = "jpg"  # Default

                    file_name = f"image_{unique_id}.{file_extension}"
                    file_path = os.path.join(download_folder, file_name)

                    # Guardar la imagen
                    with open(file_path, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)

                    print(f"Imagen descargada desde URL: {file_path}")
                except requests.exceptions.RequestException as e:
                    print(f"Error al descargar desde URL en item {idx + 1}: {e}")

            elif image_data.startswith("data:image"):
                # Procesar imagen codificada en base64
                try:
                    # Obtener datos base64 sin el encabezado
                    header, encoded = image_data.split(",", 1)
                    file_extension = header.split(";")[0].split("/")[-1]  # Obtener formato de imagen
                    file_name = f"image_{unique_id}_base64.{file_extension}"
                    file_path = os.path.join(download_folder, file_name)

                    # Decodificar y guardar
                    with open(file_path, "wb") as file:
                        file.write(base64.b64decode(encoded))

                    print(f"Imagen guardada desde base64: {file_path}")
                except Exception as e:
                    print(f"Error al procesar base64 en item {idx + 1}: {e}")

            else:
                print(f"Formato no soportado en item {idx + 1}")

# Uso del script
# Lista de archivos JSON
json_files = [
    "C:/Users/Leonardo/Downloads/img31.json",
    "C:/Users/Leonardo/Downloads/img32.json",
    "C:/Users/Leonardo/Downloads/img33.json",
    "C:/Users/Leonardo/Downloads/img34.json",
    "C:/Users/Leonardo/Downloads/img35.json",
    "C:/Users/Leonardo/Downloads/img36.json",
    "C:/Users/Leonardo/Downloads/img37.json",
    "C:/Users/Leonardo/Downloads/img38.json",
    "C:/Users/Leonardo/Downloads/img39.json",
]

download_images_from_files(json_files)

