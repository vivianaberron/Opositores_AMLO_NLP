import spacy
import gensim
from gensim import corpora
import json
import os

def cargar_y_procesar_texto(ruta_archivo):
    # Cargar modelo de SpaCy en español
    nlp = spacy.load("es_core_news_md")
    
    # Leer archivo .txt
    with open(ruta_archivo, "r", encoding="utf-8") as file:
        texto = file.read()

    # Eliminar saltos de línea y caracteres extraños
    texto = texto.replace('\n','').replace('\r', ' ').strip()
    
    # Procesar el texto y tokenización/lematización
    doc = nlp(texto)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    
    return tokens

def generar_modelo_lda(tokens, num_topics=10, passes=15):
    # Crear diccionario y corpus
    dictionary = corpora.Dictionary([tokens])
    corpus = [dictionary.doc2bow(tokens)]
    
    # Crear el modelo LDA
    lda_model = gensim.models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    
    return lda_model

def exportar_lda_a_json(lda_model, num_topics=10, ruta_archivo="lda_topics.json", carpeta_salida="./data/Tópicos_LDA/"):
    # Crear carpeta si no existe
    #if not os.path.exists(carpeta_salida):
      #  os.makedirs(carpeta_salida)
    
    # Obtener solo el nombre del archivo sin extensión
    nombre_base = os.path.basename(ruta_archivo).replace('.txt', '')
    
    # Definir nombre del archivo de salida con extensión .json dentro de la carpeta
    nombre_salida = os.path.join(carpeta_salida, f"{nombre_base}_lda_topics.json")
    
    # Generar los tópicos en un diccionario
    lda_topics = {}
    for idx, topic in lda_model.print_topics(num_topics=num_topics, num_words=10):
        topic_words = lda_model.show_topic(idx, topn=10)
        # Convertir los pesos de float32 a float para que sean serializables en JSON
        lda_topics[f"Tópico {idx}"] = {word: float(weight) for word, weight in topic_words}
    
    # Guardar los tópicos en un archivo JSON
    with open(nombre_salida, 'w', encoding='utf-8') as json_file:
        json.dump(lda_topics, json_file, ensure_ascii=False, indent=4)
    
    print(f"Tópicos LDA guardados en {nombre_salida}.")

# Función principal para generar los tópicos y guardarlos
def procesar_texto_y_guardar_tópicos(ruta_archivo, num_topics=15):
    tokens = cargar_y_procesar_texto(ruta_archivo)
    lda_model = generar_modelo_lda(tokens, num_topics=num_topics)
    exportar_lda_a_json(lda_model, num_topics=num_topics, ruta_archivo=ruta_archivo)

# Ejemplo de uso
procesar_texto_y_guardar_tópicos("./data/Archivos_amlo_txt/febrero2020.txt", num_topics=10)



