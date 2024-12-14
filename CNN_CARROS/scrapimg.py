import os
import requests
import re

def sanitize_filename(filename):
    """
    Limpia caracteres no válidos para nombres de archivo.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_images(image_urls, download_folder="images_mini_2015"):
    """
    Descarga imágenes desde una lista de URLs.

    :param image_urls: Lista de URLs de las imágenes.
    :param download_folder: Carpeta donde se guardarán las imágenes.
    """
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)  # Crear la carpeta si no existe

    for idx, url in enumerate(image_urls):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Verifica que la descarga fue exitosa
            
            # Extraer extensión válida de imagen o usar ".jpg" por defecto
            file_extension = url.split(".")[-1][:4].split('?')[0]  # Manejar parámetros en la URL
            if not file_extension.lower() in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                file_extension = 'jpg'
            
            # Nombre del archivo basado en el índice y URL limpiada
            sanitized_url = sanitize_filename(url)
            file_name = f"image_{idx + 1}_{sanitized_url[:30]}.{file_extension}"  # Limitar longitud del nombre
            file_path = os.path.join(download_folder, file_name)

            # Guardar la imagen
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            
            print(f"Imagen descargada: {file_path}")

        except requests.exceptions.RequestException as e:
            print(f"Error al descargar {url}: {e}")

# Ejemplo de uso
image_urls = [
    #"https://www.bing.com/images/search?q=mini+cooper+2015&qs=n&form=QBILPG&sp=-1&lq=0&pq=mini+cooper&sc=10-11&cvid=431294B8C83A472A97CF2CAFE45DBCE0&ghsh=0&ghacc=0&first=1&cw=1657&ch=926",  # Ejemplo 1
    "https://www.bing.com/images/sarch?q=Mini+Cooper+JCW+2015&form=RESTAB&first=1&cw=1657&ch=926",
    "https://www.bing.com/images/search?q=Mini+Cooper+5+Puertas&form=RESTAB&first=1&cw=1657&ch=926",
    "https://www.bing.com/images/search?q=Mini+Cooper+Coupe+Rojo&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Mini+Cooper+Countryman+2015&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Valor+Mini+Cooper+2015&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Mini+Cooper+Modelos&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Tipos+Mini+Cooper&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Tipos+Mini+Cooper&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Mini+Cooper+Sport&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Fotos+Mini+Cooper&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Mini+Cooper+Verde&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Im%c3%a1genes+Mini+Cooper&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Mini+Cooper+2D+2015&form=RESTAB&first=1",
    "https://www.bing.com/images/search?q=Mini+Cooper+2015+Azul&form=RESTAB&first=1&cw=1657&ch=926",
    "https://www.bing.com/images/search?q=Ashplash+Mini+Cooper&form=RESTAB&first=1&cw=1657&ch=926",
    "https://www.bing.com/images/search?q=Mini+Cooper+De+2+Puertas&form=RESTAB&first=1&cw=1657&ch=926"

]

download_images(image_urls)
