import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# Cargar los n-gramas clasificados desde el archivo Excel
df = pd.read_excel('./data/Frecuencias por año/frecuencias_globales_ngramas_2024.xlsx')

# Comprobar la estructura de los n-gramas
print(df.head())  # Asegúrate de que el archivo se cargue correctamente

# Crear una lista con las palabras de los n-gramas
n_gramas = df['N-grama'].apply(lambda x: x.split())

# Generar todas las combinaciones de co-ocurrencias
co_ocurrencias = Counter(itertools.chain(*[itertools.combinations(n_grama, 2) for n_grama in n_gramas]))

# Crear un DataFrame de co-ocurrencias
co_ocurrencias_df = pd.DataFrame(co_ocurrencias.items(), columns=['Pair', 'Frequency'])

# Filtrar para las palabras más frecuentes (puedes ajustar el valor de min_frecuencia)
min_frecuencia = 5  
co_ocurrencias_df = co_ocurrencias_df[co_ocurrencias_df['Frequency'] >= min_frecuencia]

# Verificar cuántas co-ocurrencias quedan después del filtrado
print("Número de co-ocurrencias después del filtrado: ", len(co_ocurrencias_df))

# Continuar con la creación de la tabla pivotada y el gráfico
if not co_ocurrencias_df.empty:
    # Separar las combinaciones en dos columnas (Word1 y Word2)
    co_ocurrencias_df[['Word1', 'Word2']] = pd.DataFrame(co_ocurrencias_df['Pair'].tolist(), index=co_ocurrencias_df.index)
    
    # Crear una tabla pivotada de co-ocurrencias
    co_ocurrencias_pivot = co_ocurrencias_df.pivot_table(index='Word1', columns='Word2', values='Frequency', fill_value=0)
    
    # Visualización con un heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(co_ocurrencias_pivot, cmap="Blues", annot=False, fmt="d")
    plt.title('Matriz de co-ocurrencias')
    plt.show()
else:
    print("No se generaron suficientes co-ocurrencias después del filtrado.")

