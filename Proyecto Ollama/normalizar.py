# Script para eliminar saltos de línea de un archivo de texto
def eliminar_saltos_linea(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            # Leer todo el contenido del archivo y reemplazar los saltos de línea
            contenido = infile.read().replace('\n', ' ')
        
        # Guardar el contenido procesado en un nuevo archivo
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(contenido)
        
        print(f"El archivo sin saltos de línea se guardó en: {output_file}")
    except FileNotFoundError:
        print(f"El archivo '{input_file}' no se encontró.")
    except Exception as e:
        print(f"Se produjo un error: {e}")

# Uso del script
input_file = 'C:/Users/Leonardo/Downloads/reforma/pendientes/02.txt'  # Archivo de entrada
output_file = 'C:/Users/Leonardo/Downloads/reforma/pendientes/corpus02.txt'  # Archivo de salida

eliminar_saltos_linea(input_file, output_file)
