import codecs
import nltk
from nltk.stem.snowball import SnowballStemmer
import re

class sentences:
    '''Separa un texto en oraciones'''
    def __init__(self, diario, ruta_nombres, ruta_verbos, ruta_dicc_etiquetado):
        self.diario = diario
        self.diario_etiquetado = []
        self.oraciones = []
        self.ruta_nombres = ruta_nombres
        self.ruta_verbos = ruta_verbos
        self.ruta_dicc_etiquetado = ruta_dicc_etiquetado
    
    def etiquetado_regex(self):
        patterns=[(r'.*(cé|né|ando|iendo|ió|nó)$','V'), # Verbo en infinitivo
            (r'.*mente$', 'AD'), #Advebios
            (r'.*(o|aje|ambre|an|en|in|on|un|ate|ete|ote|é|és|che|l|ma|miento|n|pa|ta|x|y|re|os)$',
            'S'), #Sustantivos
            (r'.*(a|ia|ie|ad|ed|id|ud|ez|eza|is|ncia|umbre|z|ción|sión|zón|as)$',
            'S'), #Sustantivos
            (r'.*([0-9])$|%|$', 'N') #Números
            ]
        regexp_tagger = nltk.RegexpTagger(patterns)
        tokens = self.diario.split()
        tokens = [token.replace(',','').replace('.','') for token in tokens]
        s_tagged = regexp_tagger.tag(tokens) #Hacemos el etiquetado con las reglas
        self.diario_etiquetado = s_tagged

    def etiquetado_nombres(self):
        f = codecs.open(self.ruta_nombres, 'r')
        nombres = f.readlines()
        f.close()
        nombres = [nombre.strip() for nombre in nombres]

        tagged = []

        for palabra,tag in (self.diario_etiquetado):
            if palabra in nombres:  #Si la palabra esta en la lista de nombres
                tupla = (palabra, 'P') #Creamos una nueva tupla con la palabra etiquetada como nombre
                tagged.append(tupla)
            else:
                tupla=(palabra,tag)
                tagged.append(tupla)
        self.diario_etiquetado = tagged

    def etiquetado_verbos(self):
        f = codecs.open(self.ruta_verbos, 'r')
        verbos = f.readlines()
        f.close()
        verbos = [verbo.strip() for verbo in verbos]

        stemmer = SnowballStemmer("spanish", ignore_stopwords=True) 
        verbos_lemma = [stemmer.stem(palabra) for palabra in verbos] #Lemmatizamos cada verbo y metemos su lemma en uuna lista

        tagged = []

        for palabra,tag in (self.diario_etiquetado):
            palabra = palabra.lower()
            palabra_stem = stemmer.stem(palabra)
            if palabra_stem in verbos_lemma:  #Si la palabra lemmatizada esta en la lista de verbos lemmatizados
                tupla = (palabra, 'V') #Creamos una nueva tupla con la palabra etiquetada como verbo
                tagged.append(tupla)
            else:
                tupla=(palabra,tag)
                tagged.append(tupla)
        self.diario_etiquetado = tagged

    def etiquetado_dicc(self):
        f = codecs.open(self.ruta_dicc_etiquetado, 'r')
        texto = f.readlines()
        f.close() 
        palabras_etiquetadas = {}
        for line in texto:
            linea = line.strip().split()
            palabras_etiquetadas[linea[0]] = linea[1]

        tagged = []
        for palabra,tag in (self.diario_etiquetado):
            if palabra in palabras_etiquetadas:  #Si la palabra esta en la lista de nombres
                etiqueta = palabras_etiquetadas.get(palabra)
                tupla = (palabra, etiqueta) #Creamos una nueva tupla con la palabra etiquetada como nombre
                tagged.append(tupla)
            elif tag == None:
                tupla=(palabra,'S')
                tagged.append(tupla)
            else: 
                tupla=(palabra,tag)
                tagged.append(tupla)
        self.diario_etiquetado = tagged
    
    def etiquetado(self):
        self.etiquetado_regex()
        self.etiquetado_nombres()
        self.etiquetado_verbos()
        self.etiquetado_dicc()

    def completarOraciones(self):
        n = 5
        nueva = []
        oraciones = self.oraciones
        oraciones_finales = []
        for indice, oracion in enumerate(oraciones):
            
            if(indice == len(oraciones) - 1):#Si es el ultimo elemento 
                if len(oracion.split()) <= n: #Si el ultimo es menor a 4
                    nueva[-1] += " " + oracion #Se concatena al FINAL del ultimo elemento de "nueva"
                else:#Si el ultimo es mayor a 3
                    nueva.append(oracion) #Se inserta la oracion como un nuevo elemento a "nueva"
                oraciones[indice] = ""
            
            elif indice == 0:#Si es la primer oracion
                if len(oracion.split()) <= n: 
                    oracion += " " + oraciones[indice + 1] #Se concantena al inicio de la siguiente oracion
                    if len(oracion.split()) <= n:
                        oraciones[indice +1] = oracion
                        nueva.append('') 
                    else:
                        nueva.append(oracion)
                        oraciones[indice + 1] = ''
                else:
                    nueva.append(oracion) #Se inserta la oracion como un nuevo elemento a "nueva"
                oraciones[indice] = ""

            elif len(oracion.split()) <= n: #Si no es el ultimo ni el primero y es menor o igual 3
                #Si la siguiente oracion de "oraciones" tiene mas palabras que la ultima de "nueva"
                if nueva[-1] != '':
                    if len(oraciones[indice+1].split()) < len(nueva[-1].split()):
                        #Se concatena al INICIO de la siguiente oracion y se almacena en "oracion"
                        oracion += " " + oraciones[indice + 1]
                        #Se inserta el resultado de "oracion" a la siguiente oracion 
                        oraciones[indice+1] = oracion 
                    else: #Si la oracion anterior es menor a la siguiente
                        nueva[-1] += " " + oracion #Se concatena la FINAL la oracion de el ultimo elemento de "nueva"
                    oraciones[indice] = '' 
                else:
                    if len(oracion.split()) <= n: 
                        oracion += " " + oraciones[indice + 1] #Se concantena al inicio de la siguiente oracion
                        if len(oracion.split()) <= n:
                            oraciones[indice +1] = oracion
                            nueva.append('') 
                        else:
                            nueva.append(oracion)
                            oraciones[indice + 1] = ''
                    else:
                        nueva.append(oracion) #Se inserta la oracion como un nuevo elemento a "nueva"
                    oraciones[indice] = ""
            else: #Si la oracion no es primera ni ultima y es mayor a 3 lo inserta directo
                nueva.append(oracion)
                oraciones[indice] = ""
        
        for oracion in nueva:
            if oracion != '':
                oraciones_finales.append(oracion)


        self.oraciones = oraciones_finales 

    def crear_oraciones(self):
        self.etiquetado()

        oraciones = []

        grammar = '''SUJ: {<I>?<NP>?<P.*><S>*<AD>*<Y>?<AD>?<S>?<IN>?<Y>?}
            COM: {<Y>?<IN>*<Y>?<AD>*<Y>?<NP>?<Y>?<N>?<Y>?<S>*<Y>?<N>?<Y>?<I>?<S>*}
            ORACION: {<SUJ>+<V>+<COM>+}
            ORACION: {<SUJ>+<V>+<COM>?<Y>?<IN>?<SUJ>+<V>+<COM>*}
            ORACION: {<SUJ>?<COM>?<V>+<COM>*<AD>*<SUJ>?<V>?<P>?<P.*>?<V>?<COM>+}
            '''

        cp = nltk.RegexpParser(grammar)
        tree = cp.parse(self.diario_etiquetado)

        for nodo in tree:
            if type(nodo) != tuple:
                nodo = str(nodo)
                nodo = re.sub('[^a-z0-9:áéíóúüñ%]+', ' ', nodo)
                oraciones.append(nodo)
            else:
                oraciones.append(nodo[0])
        self.oraciones = oraciones
        self.completarOraciones()

def main():
    contenido_diario = "Hoy empecé el día tomando un buen desayuno, con café y postre. Luego de esto fui al trabajo, soy periodista y he tenido que investigar bastante en estos días. Casi no me ha dejado tiempo para compartir con algunos amigos, pero estoy bien porque me gusta lo que hago. En la tarde cuando salía de hacer mis labores me encontré con Nick, él es mi vecino y me parece muy guapo. Me invitó a cenar, acepté y la pasamos genial. Cuando llegué a mi casa me di cuenta que se me había olvidado pagar los servicios, por lo que no tenía nada de luz. Toqué la puerta de Nick, pero al parecer se había quedado profundamente dormido. Así que tuve que improvisar al prender unas velas y estuve observando mucho por la ventana a los caminantes nocturnos, cosa que no hacía desde hace mucho. En seguida noté que había muchos vagabundos y me pregunté: ¿Qué habrá pasado para que terminaran en ese lugar? Después de no encontrar respuestas a mi pregunta me hice poco de té. Apenas y podía ver la llama de la candela. Alguien tocaba a la puerta y pude ver por el picaporte que era Nick. Me sentí muy aliviada en ese momento, así que le abrí, pudimos conversar un rato y me invitó a pasar la noche en su casa. Al día siguiente me devolví a mi hogar, al pasarla junto con mi vecino tenía muchas emociones juntas y en realidad se convirtió en la mejor noche de mi vida. Y sin más que agregar, buenas noches y hasta mañana."
    p = sentences(contenido_diario, 'nombres.txt', 'verbos.txt', 'dicc.txt')
    p.crear_oraciones()

    oraciones = p.oraciones

    for oracion in oraciones:
        print('-------')
        print(oracion)
    
main()

