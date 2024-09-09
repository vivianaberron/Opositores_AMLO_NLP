import pandas as pd
import os

# Ruta de la carpeta principal donde están los archivos CSV
root_dir = '/Users/vivi/Desktop/Conferencias_amlo_csv/2024/Julio 2024'  # Cambia esta ruta a la ruta principal donde están los CSV

# Inicializar una lista para almacenar el texto concatenado
all_texts = []

# Recorrer recursivamente todos los archivos en el directorio
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(root, file)
            try:
                df = pd.read_csv(file_path)
                print(f"Leyendo archivo: {file_path}")
                if 'Texto' in df.columns:
                    all_texts.extend(df['Texto'].dropna().tolist())  # Drop missing values if any
                else:
                    print(f"El archivo {file_path} no contiene la columna 'Texto'.")
            except Exception as e:
                print(f"Error al leer el archivo {file_path}: {e}")

# Unir todos los textos en un solo string
if all_texts:
    concatenated_text = '\n'.join(all_texts)

    # Guardar el texto concatenado en un archivo TXT
    output_file_path = '/Users/vivi/Desktop/Proyecto_semántica/Archivos_amlo_txt/julio2024.txt'  # Cambia esta ruta a la ruta donde quieres guardar el archivo TXT
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(concatenated_text)

    print(f"El texto concatenado se ha guardado en {output_file_path}")
else:
    print("No se encontró ningún texto en los archivos CSV especificados.")
