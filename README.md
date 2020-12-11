# Analizador de emociones en textos por segmentación en oraciones

Clasificación de textos por emociones abordado como un problema de clasificación multiclase usando SVM.
Donde el texto es segmentado en oraciones para la clasificación individual de cada una.
La segmentación de oraciones de textos se realiza mediante POS y con la librería nltk. 

## Machine Learning

1. Preprocesamiento 
2. Vectorización
3. Generación del modelo

## Segmentación por oraciones

Se hizo la segmentación por oraciones usando POS. Para el etiquetado se consideraron:

- Verbos
- Adverbios
- Sustantivos
- Números
