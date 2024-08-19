from joblib import load
import os

# Función para predecir la clasificación de una nueva noticia
def predecir_clasificacion(nueva_descripcion, ticker, model_dir='models'):
    modelo_path = os.path.join(model_dir, f'{ticker}_model.joblib')
    vectorizer_path = os.path.join(model_dir, f'{ticker}_vectorizer.joblib')
    
    modelo = load(modelo_path)
    vectorizer = load(vectorizer_path)
    
    nueva_descripcion_vec = vectorizer.transform([nueva_descripcion])
    prediccion = modelo.predict(nueva_descripcion_vec)
    
    return prediccion

# Ejemplo de uso
prediccion = predecir_clasificacion("Microsoft announces new AI-powered tools for developers.", 'MSFT')
print(f'Clasificación predicha: {prediccion[0]}')
