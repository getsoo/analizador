import codecs
import pandas as pd
import re 
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.pipeline import Pipeline
from nltk.stem.snowball import SnowballStemmer
from sklearn.externals import joblib

#FUNCIONES

def extraerDiarios( nombre_archivo ):
    f = codecs.open(nombre_archivo, 'r')
    texto = f.readlines()
    f.close() 
    
    oraciones = []
    emociones = []
    
    for linea in texto:
        if linea != '\n':
            linea = linea.split('emociones_')
            oraciones.append(linea[0])
            emociones.append(linea[1])
    return oraciones, emociones

def without_stop(text):
    f = open('stopwords_es.txt','r')
    t = f.read()
    stopwords = t.lower()
    f.close()
    content = [w for w in text if w.lower() not in stopwords]
    return content

def limpiar(vector_oraciones):
    limpio = []
    frase = []
    limpio2 = []
    stemm = ''
    
    for oracion in vector_oraciones:
        limpio.append(without_stop(limpiar_texto(oracion)))
        
    stemmer = SnowballStemmer("spanish", ignore_stopwords=True) 
    
    for oracion in limpio:
        for palabra in oracion:
            stemm = stemmer.stem(palabra)
            frase.append(stemm)
        limpio2.append(frase)
        frase = []
    
    return limpio2

def limpiar_texto(texto):
    texto = (re.sub('[^a-zA-Z ^ áéíóúüñ]',' ',texto)).split(' ')
    return texto

def numero_emocion(i):
    switcher={'emociones_Alegría':0,'emociones_Miedo':1, 'emociones_Repulsión':2, 
    'emociones_Enojo':3, 'emociones_Tristeza':4, 'emociones_Sorpresa':5, "emociones_None": 6}
    return(switcher.get(i))

def crear_df(oraciones, emociones):
    df = pd.DataFrame({'Oraciones' : oraciones,
                       'Emociones' : emociones})
        
    return df
    
def vectorizar(df):
    
    x_train, x_test, y_train, y_test = train_test_split(df.Oraciones, df.Emociones, test_size=0.2)
    
    #Calculamos la frecuencia de cada palabra con countVectorizer
    vect = CountVectorizer()
    
    #Normalizamos la frecuencia 
    tfidf = TfidfTransformer()
    
    model = svm.SVC(kernel='linear', C=1)
    
    pipeline = Pipeline([
    ('vect', vect),
    ('tfidf', tfidf),
    ('clf', model)
    ])
        
    pipeline.fit(x_train,y_train)
    
    print(pipeline.score(x_train,y_train))
      
    joblib.dump(pipeline, 'Modelo_entrenado.pkl')
    
def crear_archivo(nombre_archivo,lista):
    f = open(nombre_archivo,'w')
    for elemento in lista:
        if(type(elemento) == list):
            for num in elemento:
                f.write(str(num))
                f.write(' ')
            f.write('\n\n')
        else:
            f.write(elemento)
            f.write('\n\n')
    f.close()

#MAIN
oraciones, emociones = extraerDiarios('CORPUS3.txt')
oraciones_limpias = limpiar(oraciones)

oraciones_str = []

for oraciones in oraciones_limpias:
    oraciones_str.append(' '.join(oraciones))

df = crear_df(oraciones_str, emociones)
vectorizar(df)
