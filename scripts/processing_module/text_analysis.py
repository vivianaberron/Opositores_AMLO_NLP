import spacy
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import nltk
from nltk.corpus import wordnet as wn
import gensim
from gensim import corpora

# Configurar la ruta del directorio de datos de NLTK
nltk.data.path.append('/Users/tu_usuario/nltk_data')

# Descargar los recursos necesarios de NLTK si aún no se han descargado
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)
nltk.download('stopwords', quiet=True)

print("Leyendo archivo de texto...")
# Leer el archivo .txt
with open("./Archivos_amlo_txt/diciembre2019.txt", "r", encoding="utf-8") as file:
    texto = file.read()

# Cargar el modelo de SpaCy en español
print("Cargando modelo de SpaCy...")
nlp = spacy.load("es_core_news_md")

# Procesar el texto con SpaCy
print("Procesando el texto...")
doc = nlp(texto)

# Tokenización y lematización, eliminando stop words y signos de puntuación
tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]

# Calcular frecuencias
frecuencia = Counter(tokens)

# Palabras relacionadas con "oposición" usando WordNet
keywords = ['oposición', 'opositores', 'opositor']
related_words = set(keywords)

for keyword in keywords:
    for synset in wn.synsets(keyword, lang='spa'):
        for lemma in synset.lemmas(lang='spa'):
            related_words.add(lemma.name().replace('_', ' '))

print("Palabras relacionadas con 'oposición' usando WordNet:")
print(related_words)

# Obtener vectores de palabras y encontrar palabras similares usando embeddings
for keyword in keywords:
    token = nlp(keyword)
    # Verifica que el vector no sea nulo
    if token.vector is not None:
        # Convertir el vector a un array numpy y obtener los similares
        similar_words = token.vocab.vectors.most_similar(token.vector.reshape(1, -1), n=10)
        for similar_word in similar_words[0][0]:
            related_words.add(nlp.vocab.strings[similar_word])

print("Palabras relacionadas con embeddings:")
print(related_words)

# Filtrar términos relevantes
frecuencia_oposicion = {item: frecuencia[item] for item in related_words if item in frecuencia}

print("Frecuencias de palabras clave:")
print(frecuencia_oposicion)

# Unir los tokens procesados en un texto
processed_text = " ".join(tokens)

# Lista de stop words en español
spanish_stop_words = [
    'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para',
    'con', 'no', 'una', 'su', 'al', 'es', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya',
    'o', 'este', 'sí', 'porque', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también',
    'me', 'hasta', 'hay', 'donde', 'quien', 'desde', 'todo', 'nos', 'durante', 'todos',
    'uno', 'les', 'ni', 'contra', 'otros', 'ese', 'eso', 'ante', 'ellos', 'e', 'esto', 'mí',
    'antes', 'algunos', 'qué', 'unos', 'yo', 'otro', 'otras', 'otra', 'él', 'tanto', 'esa',
    'estos', 'mucho', 'quienes', 'nada', 'muchos', 'cual', 'poco', 'ella', 'estar', 'estas',
    'algunas', 'algo', 'nosotros', 'mi', 'mis', 'tú', 'te', 'ti', 'tu', 'tus', 'ellas', 'nosotras',
    'vosotros', 'vosotras', 'os', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 'tuyos', 'tuyas',
    'suyo', 'suya', 'suyos', 'suyas', 'nuestro', 'nuestra', 'nuestros', 'nuestras', 'vuestro',
    'vuestra', 'vuestros', 'vuestras', 'esos', 'esas', 'estoy', 'estás', 'está', 'estamos',
    'estáis', 'están', 'esté', 'estés', 'estemos', 'estéis', 'estén', 'estaré', 'estarás',
    'estará', 'estaremos', 'estaréis', 'estarán', 'estaría', 'estarías', 'estaríamos',
    'estaríais', 'estarían', 'estaba', 'estabas', 'estábamos', 'estabais', 'estaban', 'estuve',
    'estuviste', 'estuvo', 'estuvimos', 'estuvisteis', 'estuvieron', 'estuviera', 'estuvieras',
    'estuviéramos', 'estuvierais', 'estuvieran', 'estuviese', 'estuvieses', 'estuviésemos',
    'estuvieseis', 'estuviesen', 'estando', 'estado', 'estada', 'estados', 'estadas', 'estad'
]

# Normalizar stop words
spanish_stop_words = [word.lower() for word in spanish_stop_words]

# Configurar el vectorizador para generar n-gramas (bigramas y trigramas)
vectorizer = CountVectorizer(ngram_range=(2, 3), stop_words=spanish_stop_words)
X = vectorizer.fit_transform([processed_text])
ngrams = vectorizer.get_feature_names_out()

# Filtrar n-gramas que contengan las palabras clave
relevant_ngrams = [ngram for ngram in ngrams if any(keyword in ngram for keyword in related_words)]

print("N-gramas relevantes:")
for ngram in relevant_ngrams:
    print(ngram)

# Crear diccionario y corpus para LDA
tokens = [token.split() for token in tokens]  # Tokens ya procesados de antes
dictionary = corpora.Dictionary(tokens)
corpus = [dictionary.doc2bow(token) for token in tokens]

# Construir el modelo LDA
lda_model = gensim.models.LdaModel(corpus, num_topics=10, id2word=dictionary, passes=15)

# Mostrar los tópicos generados
print("Modelos de tópicos (LDA):")
for idx, topic in lda_model.print_topics(-1):
    print("Tópico: {} \nPalabras: {}".format(idx, topic))

# Guardar los n-gramas relevantes en un archivo Excel
df = pd.DataFrame(relevant_ngrams, columns=["N-gramas relevantes"])
df.to_excel("./Tópicos y n-gramas/diciembre2019.xlsx", index=False)
