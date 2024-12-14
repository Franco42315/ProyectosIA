from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
#import #time
import os
import requests
import random

# Configuración inicial
output_dir = "imagenes_bing_ferrari"
os.makedirs(output_dir, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

downloaded_urls = set()  # Evitar descargas duplicadas

# Lista de URLs a procesar
urls = [
    "https://www.bing.com/images/search?q=Ferrari%20488%20rosa&qs=n&form=QBIR&sp=-1&lq=0&pq=ferrari%20488%20r&sc=10-13&cvid=8FF59A6CDDAF4552B7CE3DD545AE6765&ghsh=0&ghacc=0&first=1",
    "https://www.bing.com/images/search?q=Ferrari%20488%20verde&qs=n&form=QBIR&sp=-1&lq=0&pq=ferrari%20488%20ver&sc=10-15&cvid=71BD49331A114594B60EAFCDAE738B40&ghsh=0&ghacc=0&first=1"


]

# Descargar imágenes
def download_image(url, output_path):
    if url in downloaded_urls:
        print(f"Imagen ya descargada: {url}")
        return
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type')
            if content_type:
                if "image/jpeg" in content_type:
                    extension = ".jpg"
                elif "image/png" in content_type:
                    extension = ".png"
                elif "image/gif" in content_type:
                    extension = ".gif"
                else:
                    extension = ""  # Sin extensión conocida

                output_path += extension

            with open(output_path, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            print(f"Imagen descargada: {output_path}")
            downloaded_urls.add(url)
            #time.sleep(random.uniform(1, 3))  # Pausa aleatoria entre descargas
        else:
            print(f"Error al descargar la imagen: {url} (Status: {response.status_code})")
    except Exception as e:
        print(f"Excepción al descargar la imagen {url}: {e}")

# Esperar a que cargue la página completamente
def wait_for_page_load(driver):
    WebDriverWait(driver, 20).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# Procesar imágenes en la página de Bing
def process_images_bing():
    images = driver.find_elements(By.XPATH, "//img[contains(@class, 'mimg')]")
    print(f"Imágenes detectadas: {len(images)}")
    for img in images:
        src = img.get_attribute("src")
        if src and src.startswith("http"):
            image_name = src.split("/")[-1].split("?")[0]
            output_path = os.path.join(output_dir, image_name)
            download_image(src, output_path)

# Buscar y hacer clic en el botón 'Ver más imágenes'
def click_see_more_button():
    try:
        see_more_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Ver más imágenes')]"))
        )
        if see_more_button:
            print("Botón 'Ver más imágenes' encontrado. Haciendo clic...")
            see_more_button.click()
            #time.sleep(random.uniform(2, 4))  # Pausa tras el clic
            return True
    except Exception:
        return False

# Ejecutar el proceso para una URL específica
def process_url(url):
    driver.get(url)
    wait_for_page_load(driver)

    total_scrolls = 100
    failed_clicks = 0  # Contador de intentos fallidos
    for _ in range(total_scrolls):
        process_images_bing()
        if not click_see_more_button():
            failed_clicks += 1
            print(f"Intento fallido {failed_clicks} de encontrar el botón.")
            if failed_clicks >= 15:
                print("Máximo de intentos fallidos alcanzado. Pasando a la siguiente URL.")
                break
        else:
            failed_clicks = 0  # Reinicia el contador si encuentra el botón
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        #time.sleep(random.uniform(2, 5))

# Programa principal
try:
    for url in urls:
        print(f"Procesando URL: {url}")
        process_url(url)
finally:
    driver.quit()
    print("Proceso completado.")
