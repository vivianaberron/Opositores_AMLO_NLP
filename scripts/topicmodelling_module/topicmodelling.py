import pandas as pd
import json
import seaborn as sns
import matplotlib.pyplot as plt

# Palabras clave a rastrear
palabras_clave = [""]

# Lista de archivos JSON de tópicos
archivos_json = [
    './data/Tópicos_LDA/enero2019_lda_topics.json',
    './data/Tópicos_LDA/febrero2019_lda_topics.json',
    './data/Tópicos_LDA/marzo2019_lda_topics.json',
    './data/Tópicos_LDA/abril2019_lda_topics.json',
    './data/Tópicos_LDA/mayo2019_lda_topics.json',
    './data/Tópicos_LDA/junio2019_lda_topics.json',
    './data/Tópicos_LDA/julio2019_lda_topics.json',
    './data/Tópicos_LDA/agosto2019_lda_topics.json',
    './data/Tópicos_LDA/septiembre2019_lda_topics.json',
    './data/Tópicos_LDA/octubre2019_lda_topics.json',
    './data/Tópicos_LDA/noviembre2019_lda_topics.json',
    './data/Tópicos_LDA/diciembre2019_lda_topics.json'
]

# Diccionario para almacenar la relevancia de las palabras clave a lo largo del tiempo
frecuencia_palabras = {palabra: [] for palabra in palabras_clave}
meses = []

for archivo in archivos_json:
    with open(archivo, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Nombre del mes o año
        mes_año = archivo.replace('_lda_topics.json', '')
        meses.append(mes_año)
        
        # Iterar sobre las palabras clave
        for palabra in palabras_clave:
            relevancia_total = 0
            # Sumar la relevancia de la palabra clave en todos los tópicos
            for topic, palabras in data.items():
                if palabra in palabras:
                    relevancia_total += palabras[palabra]
            frecuencia_palabras[palabra].append(relevancia_total)

# Verificar si los datos se cargaron correctamente
print("Datos cargados:")
print(frecuencia_palabras)

# Convertir el diccionario a DataFrame
df_palabras = pd.DataFrame(frecuencia_palabras, index=meses)

# Verificar el DataFrame
print("\nDataFrame de frecuencias:")
print(df_palabras)

# Si el DataFrame no está vacío, crear el mapa de calor
if not df_palabras.empty:
    plt.figure(figsize=(10, 6))
    sns.heatmap(df_palabras, annot=True, cmap="YlGnBu", linewidths=.5)
    plt.title("Relevancia de palabras clave en tópicos a lo largo del tiempo")
    plt.xlabel("Palabras clave")
    plt.ylabel("Mes/Año")
    plt.show()
else:
    print("El DataFrame está vacío. Verifica los archivos JSON o las palabras clave.")


