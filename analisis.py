from sklearn.externals import joblib
import nltk
import re
from nltk.stem.snowball import SnowballStemmer

class Preprocesamiento:
    '''Realiza el preprocesamiento del texto del diario'''
    
    def __init__(self, diario):
        self.diario = diario

    def crearOraciones(self, texto):
        sentences = []
        sent_tokenizer = nltk.data.load('tokenizers/punkt/spanish.pickle')
        sentences = sent_tokenizer.tokenize(texto)
        return sentences
    
    def quitarCaracteresE(self, texto):
        texto = (re.sub('[^a-zA-Z ^ áéíóúüñ]',' ',texto)).split(' ')
        return texto
    
    def quitarStopwords(self, text):
        f = open('stopwords_es.txt', 'r')   #?
        t = f.read()
        stopwords = t.lower()
        f.close()
        contenido = [w for w in text if w.lower() not in stopwords]
        return contenido
    
    def preprocesarDiario(self):
        
        oraciones = self.crearOraciones(self.diario)
        
        aux = []
        frase = []
        limpio = []
        stemm = ''
        
        for oracion in oraciones:
            aux.append(self.quitarStopwords(self.quitarCaracteresE(oracion)))
        
        stemmer = SnowballStemmer('spanish', ignore_stopwords = True)
        
        for oracion in aux:
            for palabra in oracion:
                stemm = stemmer.stem(palabra)
                frase.append(stemm)
            limpio.append(' '.join(frase))
            frase = []
            
        return limpio
    

class Analisis:
    '''Realiza el analisis de emociones del diario una vez preperocesado'''
    
    def __init__(self, diario_prep):
        self.diario_prep = diario_prep
        
        
        

def main():
    contenido_diario = "Hoy empecé el día tomando un buen desayuno, con café y postre. Luego de esto fui al trabajo, soy periodista y he tenido que investigar bastante en estos días. Casi no me ha dejado tiempo para compartir con algunos amigos, pero estoy bien porque me gusta lo que hago. En la tarde cuando salía de hacer mis labores me encontré con Nick, él es mi vecino y me parece muy guapo. Me invitó a cenar, acepté y la pasamos genial. Cuando llegué a mi casa me di cuenta que se me había olvidado pagar los servicios, por lo que no tenía nada de luz. Toqué la puerta de Nick, pero al parecer se había quedado profundamente dormido. Así que tuve que improvisar al prender unas velas y estuve observando mucho por la ventana a los caminantes nocturnos, cosa que no hacía desde hace mucho. En seguida noté que había muchos vagabundos y me pregunté: ¿Qué habrá pasado para que terminaran en ese lugar? Después de no encontrar respuestas a mi pregunta me hice poco de té. Apenas y podía ver la llama de la candela. Alguien tocaba a la puerta y pude ver por el picaporte que era Nick. Me sentí muy aliviada en ese momento, así que le abrí, pudimos conversar un rato y me invitó a pasar la noche en su casa. Al día siguiente me devolví a mi hogar, al pasarla junto con mi vecino tenía muchas emociones juntas y en realidad se convirtió en la mejor noche de mi vida. Y sin más que agregar, buenas noches y hasta mañana."
    a = Preprocesamiento(contenido_diario)
    print(a.preprocesarDiario())
    
    
if __name__ == '__main__':
    main()