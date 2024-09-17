import spacy
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import time

# Cargar modelo de embeddings de SpaCy
nlp = spacy.load("es_core_news_md")


# Prototipos de palabras clave para cada marco
prototipo_colaboracion = ["evitar", "gustar", "querer", "pensar", "ánimo", "participativo", "postura", "comunidad", "diálogo", "aceptar", "democracia", "político", "tranquilo", "consciencia"]
prototipo_descalificacion = ["adversario", "contrario", "corrupción", "corrupto", "prensa", "legítimo", "rival", "conservador", "conservadurismo", "legítimo", "opositor", "irresponsable", "crítico", "críticos", "oposición", "aprovechar","ataque", "enemigo", "opositores"]
prototipo_conflicto = ["resistencia", "perjudicar", "perseguir", "cerco", "violencia", "guerra", "exceso", "investigación", "problema", "molestar", "aprovechar", "delito", "afectar", "obstáculo", "fractura", "impunidad"]


# Función para calcular la similitud de un n-grama con los prototipos de los marcos
def clasificar_ngram(ngrama):
    # Vectorizar el n-grama y los prototipos
    vector_ngram = nlp(ngrama).vector.reshape(1, -1)
    print(f"Procesando n-grama: {ngrama}")
    
    # Calcular la similitud con los prototipos
    sim_colaboracion = cosine_similarity(vector_ngram, [nlp(p).vector for p in prototipo_colaboracion]).mean()
    sim_descalificacion = cosine_similarity(vector_ngram, [nlp(p).vector for p in prototipo_descalificacion]).mean()
    sim_conflicto = cosine_similarity(vector_ngram, [nlp(p).vector for p in prototipo_conflicto]).mean()

    
    # Asignar al marco con la mayor similitud
    if max(sim_colaboracion, sim_descalificacion, sim_conflicto) == sim_colaboracion:
        return 'Colaboración'
    elif max(sim_colaboracion, sim_descalificacion, sim_conflicto) == sim_descalificacion:
        return 'Descalificación'
    else:
        return 'Conflicto'
print(f"Similitudes calculadas")
# Cargar los n-gramas desde tu archivo Excel (.xlsx)
df = pd.read_excel('./data/Frecuencias por año/frecuencias_globales_ngramas_2024.xlsx')

# Aplicar la función a cada n-grama en el DataFrame
df['Clasificación'] = df['N-grama'].apply(clasificar_ngram)

# Guardar el resultado en un nuevo archivo Excel
df.to_excel('n_gramas_clasificados_2024.xlsx', index=False)

print(df.head())


## Prototipos de palabras clave para cada marco
#prototipo_colaboracion = ["evitar", "gustar", "querer", "pensar", "ánimo", "participativo", "postura", "comunidad", "diálogo", "aceptar", "democracia", "político", "tranquilo", "consciencia"]
#prototipo_descalificacion = ["adversario", "contrario", "corrupción", "corrupto", "prensa", "legítimo", "rival", "conservador", "conservadurismo", "legítimo", "opositor", "irresponsable", "crítico", "críticos", "oposición", "aprovechar","ataque", "enemigo", "opositores"]
#prototipo_conflicto = ["resistencia", "perjudicar", "perseguir", "cerco", "violencia", "guerra", "exceso", "investigación", "problema", "molestar", "aprovechar", "delito", "afectar", "obstáculo", "fractura", "impunidad"]
