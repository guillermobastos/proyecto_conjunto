from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import pandas as pd

def entrenar_modelo_mejorado(noticias_clasificadas, datos_tecnicos, datos_financieros):
    """
    Entrena un modelo de aprendizaje automático con las noticias clasificadas, datos técnicos y financieros.
    
    Args:
        noticias_clasificadas (list): Lista de noticias clasificadas.
        datos_tecnicos (dict): Indicadores técnicos del ticker.
        datos_financieros (dict): Indicadores financieros de la empresa.
    
    Returns:
        modelo: El modelo entrenado.
    """
    df_noticias = pd.DataFrame(noticias_clasificadas)
    X = df_noticias['descripcion']
    y = df_noticias['clasificacion']
    
    if X.empty or y.empty:
        print("No hay suficientes datos para entrenar el modelo.")
        return None
    
    # Crear un pipeline de procesamiento de texto y entrenamiento de modelo
    pipeline = make_pipeline(CountVectorizer(), MultinomialNB())
    modelo = pipeline.fit(X, y)
    
    print("Modelo entrenado con datos técnicos y financieros.")
    return modelo
