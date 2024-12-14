import os
import json

def extract_and_save_comments(json_files, output_file="output_texts/youtube_comments.txt"):
    """
    Extrae el campo `Comment` de una lista de archivos JSON y lo guarda en un solo archivo TXT, separando los comentarios por saltos de línea.

    Args:
        json_files (list): Lista de rutas de los archivos JSON.
        output_file (str): Ruta del archivo de salida para los textos extraídos.

    Returns:
        None
    """
    # Crear el directorio de salida si no existe
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w", encoding="utf-8") as txt_file:
        for idx, json_file in enumerate(json_files):
            try:
                # Leer el archivo JSON
                with open(json_file, "r", encoding="utf-8") as file:
                    data = json.load(file)

                # Manejar si data es una lista
                if isinstance(data, list):
                    for item_idx, item in enumerate(data):
                        comment = item.get("Comment", "")

                        if comment:
                            # Escribir el comentario en el archivo de salida
                            txt_file.write(comment + "\n")

                            print(f"Comentario del item {item_idx + 1} de {json_file} agregado al archivo {output_file}")
                        else:
                            print(f"No se encontró el campo 'Comment' en el item {item_idx + 1} de {json_file}")
                else:
                    comment = data.get("Comment", "")

                    if comment:
                        # Escribir el comentario en el archivo de salida
                        txt_file.write(comment + "\n")

                        print(f"Comentario de {json_file} agregado al archivo {output_file}")
                    else:
                        print(f"No se encontró el campo 'Comment' en {json_file}")

            except Exception as e:
                print(f"Error procesando el archivo {json_file}: {e}")

# Ejemplo de uso
# Lista de rutas a archivos JSON
json_files = [
  "./youtube/yt1.json",
  "./youtube/yt2.json",
  "./youtube/yt3.json",
  "./youtube/yt4.json",
  ]

# Llamar a la función para procesar los archivos
extract_and_save_comments(json_files)