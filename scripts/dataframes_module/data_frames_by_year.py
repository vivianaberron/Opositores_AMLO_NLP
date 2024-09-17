import pandas as pd
import os

# Ruta donde están tus archivos .xlsx
ruta_archivos = '/Users/vivi/Desktop/project/data/N-gramas/2024'

# Lista para almacenar los DataFrames de cada archivo
dataframes = []

# Iteramos sobre cada archivo en la carpeta
for archivo in os.listdir(ruta_archivos):
    if archivo.endswith('.xlsx'):
        # Leer cada archivo .xlsx
        df = pd.read_excel(os.path.join(ruta_archivos, archivo))
        
        # Renombrar la columna "N-gramas relevantes" a "N-grama"
        df.rename(columns={"N-gramas relevantes": "N-grama"}, inplace=True)
        
        # Añadir el DataFrame a la lista
        dataframes.append(df)

# Unir todos los DataFrames en uno solo, sin considerar el mes
df_unificado = pd.concat(dataframes, ignore_index=True)

# Calcular la frecuencia de cada n-grama en todo el conjunto de datos
frecuencias = df_unificado['N-grama'].value_counts().reset_index(name='Frecuencia')
frecuencias.rename(columns={'index': 'N-grama'}, inplace=True)

# Calcular el porcentaje de aparición de cada n-grama
total_ngramas = frecuencias['Frecuencia'].sum()
frecuencias['Porcentaje'] = (frecuencias['Frecuencia'] / total_ngramas) * 100

# Mostrar los primeros resultados para revisión
print(frecuencias.head())

# Guardar los resultados en un archivo Excel
#frecuencias.to_excel('frecuencias_globales_ngramas_2019.xlsx', index=False)
