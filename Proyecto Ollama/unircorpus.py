def unir_corpus(corpus_files, output_file):
    try:
        with open(output_file, 'a', encoding='utf-8') as outfile:
            for corpus_file in corpus_files:
                print(f"Procesando archivo: {corpus_file}")
                try:
                    with open(corpus_file, 'r', encoding='utf-8') as infile:
                        # Leer el contenido del archivo, eliminar saltos de línea y añadir al archivo de salida
                        contenido = infile.read().replace('\n', ' ').strip()
                        outfile.write(contenido + ' ')  # Agregar un espacio al final del texto procesado
                except FileNotFoundError:
                    print(f"El archivo '{corpus_file}' no se encontró.")
                except Exception as e:
                    print(f"Error procesando el archivo '{corpus_file}': {e}")

        print(f"El contenido de todos los archivos se guardó en: {output_file}")
    except Exception as e:
        print(f"Se produjo un error general: {e}")

# Uso del script
corpus_files = [
    "./corpus/corpus01.txt",
    "./corpus/corpus02.txt",
    "./corpus/corpus_unido.txt",
    "./corpus/corpus_unido2.txt"
  ]  # Lista de archivos de entrada
output_file = 'corpus_full.txt'  # Archivo de salida

unir_corpus(corpus_files, output_file)
