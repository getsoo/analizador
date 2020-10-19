from sklearn.externals import joblib
import nltk
import re
from nltk.stem.snowball import SnowballStemmer
import oraciones
from oraciones import sentences

class PreprocesamientoGET:
    '''Realiza el preprocesamiento del texto del diario'''
    
    def __init__(self, diario, ruta_spanish_pickle, ruta_stopwords_es):
        self.diario = diario
        self.oraciones_diario = []
        self.ruta_spanish_pickle = ruta_spanish_pickle
        self.ruta_stopwords_es = ruta_stopwords_es

    def crearOraciones(self, texto):
        p = sentences(texto, 'nombres.txt', 'verbos.txt', 'dicc.txt')
        p.crear_oraciones()
        oraciones = p.oraciones
        return oraciones
    
    def quitarCaracteresE(self, texto):
        texto = (re.sub('[^a-zA-Z ^ áéíóúüñ]',' ',texto)).split(' ')
        return texto
    
    def quitarStopwords(self, text):
        f = open(self.ruta_stopwords_es, 'r')   #?
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
            
        self.oraciones_diario = limpio
    

class AnalisisEmocionesGet:
    '''Realiza el analisis de emociones del diario una vez preperocesado'''
    def __init__(self, oraciones_diario, rutaModeloPKL):
        self.oraciones_diario = oraciones_diario
        self.alegria = 0
        self.enojo = 0
        self.miedo = 0
        self.repulsion = 0
        self.sorpresa = 0
        self.tristeza = 0
        self.ambiguo = 0
        self.rutaModeloPKL = rutaModeloPKL
        
    def extraerPKL(self):
        with open(self.rutaModeloPKL, 'rb') as fo:  #?
            loaded_model = joblib.load(fo)
        return loaded_model
        
    def realizarAnalisis(self):
        modelo = self.extraerPKL()
        emociones = modelo.predict(self.oraciones_diario)
        return emociones
    
    def eliminarCE(self, emocion):
        opciones = {'Alegría': 'alegria', 'Miedo': 'miedo', 
                    'Repulsión': 'repulsion', 'Enojo': 'enojo', 
                    'Tristeza': 'tristeza', 'Sorpresa': 'sorpresa', 
                    'None': 'ambiguo'}
        return(opciones.get(emocion))
    
    def analisisPonderado(self):
        emociones = self.realizarAnalisis()
        ponderacion = {'alegria':0,'miedo':0, 'repulsion':0,'enojo':0, 
                    'tristeza':0, 'sorpresa':0, 'ambiguo':0}
        len_emociones = len(emociones)
        
        for emocion in emociones:
            ponderacion[self.eliminarCE(emocion.strip())] += 1
        
        
        self.alegria = ponderacion['alegria'] * 100 // len_emociones
        self.enojo = ponderacion['enojo'] * 100 // len_emociones
        self.miedo = ponderacion['miedo'] * 100 // len_emociones
        self.repulsion = ponderacion['repulsion'] * 100 // len_emociones
        self.sorpresa = ponderacion['sorpresa'] * 100 // len_emociones
        self.tristeza = ponderacion['tristeza'] * 100 // len_emociones
        self.ambiguo = ponderacion['ambiguo'] * 100 // len_emociones



def main():
    contenido_diario = "Hoy empecé el día tomando un buen desayuno, con café y postre. Luego de esto fui al trabajo, soy periodista y he tenido que investigar bastante en estos días. Casi no me ha dejado tiempo para compartir con algunos amigos, pero estoy bien porque me gusta lo que hago. En la tarde cuando salía de hacer mis labores me encontré con Nick, él es mi vecino y me parece muy guapo. Me invitó a cenar, acepté y la pasamos genial. Cuando llegué a mi casa me di cuenta que se me había olvidado pagar los servicios, por lo que no tenía nada de luz. Toqué la puerta de Nick, pero al parecer se había quedado profundamente dormido. Así que tuve que improvisar al prender unas velas y estuve observando mucho por la ventana a los caminantes nocturnos, cosa que no hacía desde hace mucho. En seguida noté que había muchos vagabundos y me pregunté: ¿Qué habrá pasado para que terminaran en ese lugar? Después de no encontrar respuestas a mi pregunta me hice poco de té. Apenas y podía ver la llama de la candela. Alguien tocaba a la puerta y pude ver por el picaporte que era Nick. Me sentí muy aliviada en ese momento, así que le abrí, pudimos conversar un rato y me invitó a pasar la noche en su casa. Al día siguiente me devolví a mi hogar, al pasarla junto con mi vecino tenía muchas emociones juntas y en realidad se convirtió en la mejor noche de mi vida. Y sin más que agregar, buenas noches y hasta mañana."
    p = PreprocesamientoGET(contenido_diario,'spanish.pickle','stopwords_es.txt')
    p.preprocesarDiario()

    analisis = AnalisisEmocionesGet(p.oraciones_diario,'Modelo_entrenado.pkl')
    print(p.oraciones_diario)
    
    analisis.analisisPonderado()
    
    print("alegria: ",analisis.alegria)
    print("enojo: ",analisis.enojo)
    print("miedo: ",analisis.miedo)
    print("repulsion: ",analisis.repulsion)
    print("sorpresa: ",analisis.sorpresa)
    print("tristeza: ",analisis.tristeza)
    print("ambiguo: ",analisis.ambiguo)
main()