import codecs
import nltk

class sentences:
    '''Separa un texto en oraciones'''
    def __init__(self, diario):
        self.diario = diario
        self.oraciones_diario = []
    
    def etiquetado_regex(self):
        patterns=[(r'.*(ar|er|ir|cé|né|ando|iendo)$','V'), # Verbo en infinitivo
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
        self.oraciones_diario = s_tagged

def main():
    contenido_diario = "Hoy empecé el día tomando un buen desayuno, con café y postre. Luego de esto fui al trabajo, soy periodista y he tenido que investigar bastante en estos días. Casi no me ha dejado tiempo para compartir con algunos amigos, pero estoy bien porque me gusta lo que hago. En la tarde cuando salía de hacer mis labores me encontré con Nick, él es mi vecino y me parece muy guapo. Me invitó a cenar, acepté y la pasamos genial. Cuando llegué a mi casa me di cuenta que se me había olvidado pagar los servicios, por lo que no tenía nada de luz. Toqué la puerta de Nick, pero al parecer se había quedado profundamente dormido. Así que tuve que improvisar al prender unas velas y estuve observando mucho por la ventana a los caminantes nocturnos, cosa que no hacía desde hace mucho. En seguida noté que había muchos vagabundos y me pregunté: ¿Qué habrá pasado para que terminaran en ese lugar? Después de no encontrar respuestas a mi pregunta me hice poco de té. Apenas y podía ver la llama de la candela. Alguien tocaba a la puerta y pude ver por el picaporte que era Nick. Me sentí muy aliviada en ese momento, así que le abrí, pudimos conversar un rato y me invitó a pasar la noche en su casa. Al día siguiente me devolví a mi hogar, al pasarla junto con mi vecino tenía muchas emociones juntas y en realidad se convirtió en la mejor noche de mi vida. Y sin más que agregar, buenas noches y hasta mañana."
    p = sentences(contenido_diario)
    p.etiquetado_regex()

    print(p.oraciones_diario)
    
main()