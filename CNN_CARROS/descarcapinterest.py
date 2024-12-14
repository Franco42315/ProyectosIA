from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import requests
import random  # Para generar delays aleatorios

# Configuración inicial
output_dir = "imagenes_pinterest"
os.makedirs(output_dir, exist_ok=True)

options = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Evitar descargas duplicadas
downloaded_urls = set()

# Descargar imágenes
def download_image(url, output_path):
    if url in downloaded_urls:
        print(f"Imagen ya descargada: {url}")
        return
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(output_path, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            print(f"Imagen descargada: {output_path}")
            downloaded_urls.add(url)
            time.sleep(random.uniform(1, 3))  # Pausa aleatoria entre descargas
        else:
            print(f"Error al descargar la imagen: {url} (Status: {response.status_code})")
    except Exception as e:
        print(f"Excepción al descargar la imagen {url}: {e}")

# Esperar a que cargue la página
def wait_for_page_load(driver):
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# Procesar imágenes en la página
def process_images():
    images = driver.find_elements(By.XPATH, "//img[contains(@src, 'pinimg.com')]")
    print(f"Imágenes detectadas: {len(images)}")
    for img in images:
        src = img.get_attribute("src")
        if src:
            # Generar un nombre único para cada imagen
            image_name = src.split("/")[-1].split("?")[0]
            output_path = os.path.join(output_dir, image_name)
            download_image(src, output_path)

# Programa principal
try:
    pinterest_url = "https://mx.pinterest.com/search/pins/?q=tsuru%20nissan%20colores&rs=guide&journey_depth=1&source_module_id=OB_tsuru_nissan_colores_58fa9741-8839-490f-9db4-3a6cd81e80e8&add_refine=Colores%7Cguide%7Cword%7C17"
    driver.get(pinterest_url)
    wait_for_page_load(driver)

    total_scrolls = 200  # Número de desplazamientos
    for _ in range(total_scrolls):
        process_images()  # Procesa las imágenes visibles
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)  # Desplázate hacia abajo
        time.sleep(random.uniform(2, 5))  # Pausa aleatoria entre desplazamientos
finally:
    driver.quit()
    print("Proceso completado.")
