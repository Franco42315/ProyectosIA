import json

def agregar_corpus(json_files, output_file):
    try:
        # Iterar sobre la lista de archivos JSON
        for json_file in json_files:
            print(f"Procesando archivo: {json_file}")
            # Leer el archivo JSON actual
            with open(json_file, 'r', encoding='utf-8') as infile:
                datos = json.load(infile)
            
            # Procesar el contenido de "NewsText" y eliminar saltos de línea
            textos = []
            for item in datos:
                if "NewsText" in item and item["NewsText"]:
                    textos.append(item["NewsText"].replace('\n', ' ').strip())
            
            # Guardar el texto procesado en el archivo de salida
            with open(output_file, 'a', encoding='utf-8') as outfile:
                for texto in textos:
                    outfile.write(texto + ' ')  # Agregar el texto y un espacio al final

        print(f"Se agregó el contenido de todos los archivos al archivo: {output_file}")
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo. Detalle: {e}")
    except json.JSONDecodeError:
        print(f"Error al leer uno de los archivos JSON. Verifica su formato.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Uso del script
json_files = [
        './googlenews/google1.json',
        './googlenews/google2.json',
        './googlenews/google3.json',
        './googlenews/google4.json',
        './googlenews/google5.json',
        './googlenews/google6.json',
        './googlenews/google7.json',
        './googlenews/google8.json',
        './googlenews/google9.json',
        './googlenews/google10.json'
    ]  # Lista de archivos JSON
output_file = 'corpusgoogle.txt'  # Archivo de texto de salida

agregar_corpus(json_files, output_file)
