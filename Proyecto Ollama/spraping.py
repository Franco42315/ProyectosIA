import os
import json
import re

def clean_tweet_content(tweet):
    """
    Limpia el contenido de un tweet eliminando URLs.
    """
    # Eliminar URLs
    tweet = re.sub(r'http\S+|www\S+', '', tweet)
    return tweet

# Ajusta el procesamiento en tu función
def extract_and_save_tweet_content(json_files, output_file="output_texts/tweets.txt"):
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_file, "w", encoding="utf-8") as txt_file:
        for idx, json_file in enumerate(json_files):
            try:
                with open(json_file, "r", encoding="utf-8") as file:
                    data = json.load(file)

                if isinstance(data, list):
                    for item_idx, item in enumerate(data):
                        tweet_content = item.get("Tweet_Content", "")
                        if tweet_content:
                            tweet_content = clean_tweet_content(tweet_content)  # Limpieza
                            txt_file.write(tweet_content + "\n")
                else:
                    tweet_content = data.get("Tweet_Content", "")
                    if tweet_content:
                        tweet_content = clean_tweet_content(tweet_content)  # Limpieza
                        txt_file.write(tweet_content + "\n")

            except Exception as e:
                print(f"Error procesando el archivo {json_file}: {e}")


# Ejemplo de uso
# Lista de rutas a archivos JSON
json_files = [
                "./twitter/reforma1.json",
                "./twitter/reforma2.json",
                "./twitter/reforma3.json",
                "./twitter/reforma4.json",
                "./twitter/reforma5.json",
                "./twitter/reforma6.json",
                "./twitter/reforma7.json",
                "./twitter/reforma8.json",
                "./twitter/reforma9.json",
                "./twitter/reforma10.json",
                "./twitter/reforma11.json",
                "./twitter/reforma12.json",
                "./twitter/reforma13.json",
                "./twitter/reforma14.json",
                "./twitter/reforma15.json",
                "./twitter/reforma16.json",
                "./twitter/reforma17.json",
                "./twitter/reforma18.json",
            ]

# Llamar a la función para procesar los archivos
extract_and_save_tweet_content(json_files)
