import finnhub
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()
# Obtener la clave API desde las variables de entorno
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

def obtener_noticias(ticker):
    """
    Obtiene noticias relacionadas con un ticker específico para el día actual usando Finnhub.
    
    Args:
        ticker (str): El ticker de la acción.
    
    Returns:
        list: Lista de noticias obtenidas.
    """
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')

    noticias = finnhub_client.company_news(ticker, _from=fecha_hoy, to=fecha_hoy)
    
    noticias_filtradas = []
    for noticia in noticias:
        noticia_fecha = datetime.fromtimestamp(noticia['datetime']).strftime('%Y-%m-%d %H:%M:%S')
        noticias_filtradas.append({
            'titulo': noticia['headline'],
            'descripcion': noticia['summary'],
            'fecha': noticia_fecha
        })

    return noticias_filtradas

def obtener_datos_accion(ticker):
    """
    Obtiene datos históricos de precios de una acción para el día actual.
    
    Args:
        ticker (str): El ticker de la acción.
    
    Returns:
        DataFrame: Datos de precios de la acción.
    """
    df = yf.download(ticker, period='1d', interval='1m')
    return df

def calcular_impacto_noticia(noticia_fecha, df):
    """
    Calcula el impacto de una noticia en el precio de la acción.
    
    Args:
        noticia_fecha (int): La fecha de la noticia en formato timestamp.
        df (DataFrame): Datos históricos del precio de la acción.
    
    Returns:
        float: La variación del precio en torno a la fecha de la noticia.
    """
    fecha_noticia = pd.to_datetime(noticia_fecha)
    df['Fecha'] = pd.to_datetime(df.index).date
    fecha_noticia = fecha_noticia.date()
    
    rango_dias = 1
    fecha_inicio = fecha_noticia - timedelta(days=rango_dias)
    fecha_fin = fecha_noticia + timedelta(days=rango_dias)
    
    datos_rango = df[(df['Fecha'] >= fecha_inicio) & (df['Fecha'] <= fecha_fin)]
    
    if datos_rango.empty:
        return 0.0
    
    precio_inicio = datos_rango.iloc[0]['Close']
    precio_fin = datos_rango.iloc[-1]['Close']
    
    if precio_inicio == 0:
        return 0.0
    
    impacto = ((precio_fin - precio_inicio) / precio_inicio) * 100
    return impacto

def clasificar_noticias(noticias, df):
    """
    Clasifica las noticias basándose en la variación del precio de la acción en 7 niveles.
    
    Args:
        noticias (list): Lista de noticias relacionadas con el ticker.
        df (DataFrame): Datos históricos del precio de la acción.
    
    Returns:
        list: Lista de noticias con su clasificación de impacto.
    """
    noticias_clasificadas = []
    for noticia in noticias:
        impacto = calcular_impacto_noticia(noticia['fecha'], df)
        
        # Clasificación en 7 niveles
        if impacto <= -10:
            clasificacion = 0  # Muy Negativa
        elif -10 < impacto <= -5:
            clasificacion = 1  # Negativa
        elif -5 < impacto <= -1:
            clasificacion = 2  # Ligeramente Negativa
        elif -1 < impacto <= 1:
            clasificacion = 3  # Neutra
        elif 1 < impacto <= 5:
            clasificacion = 4  # Ligeramente Positiva
        elif 5 < impacto <= 10:
            clasificacion = 5  # Positiva
        elif impacto > 10:
            clasificacion = 6  # Muy Positiva
        
        noticias_clasificadas.append({
            'titulo': noticia['titulo'],
            'descripcion': noticia['descripcion'],
            'fecha': noticia['fecha'],
            'impacto': impacto,
            'clasificacion': clasificacion
        })
    
    return noticias_clasificadas


def entrenar_modelo(noticias_clasificadas):
    """
    Entrena un modelo de aprendizaje automático con las noticias clasificadas.
    
    Args:
        noticias_clasificadas (list): Lista de noticias clasificadas.
    
    Returns:
        modelo: El modelo entrenado.
    """
    df_noticias = pd.DataFrame(noticias_clasificadas)
    X = df_noticias['descripcion']
    y = df_noticias['clasificacion']
    
    if X.empty or y.empty:
        print("No hay suficientes datos para entrenar el modelo.")
        return None
    
    pipeline = make_pipeline(CountVectorizer(), MultinomialNB())
    modelo = pipeline.fit(X, y)
    
    print("Modelo entrenado.")
    return modelo

def predecir_impacto_noticia(modelo, texto_noticia):
    """
    Predice el impacto de una nueva noticia utilizando el modelo entrenado.
    
    Args:
        modelo: El modelo entrenado.
        texto_noticia (str): Texto de la nueva noticia.
    
    Returns:
        str: La predicción del impacto de la noticia.
    """
    prediccion = modelo.predict([texto_noticia])
    return prediccion[0]


def evolucion_posterior_noticia(ticker, df, noticia, rango_dias=10):
    """
    Analiza la evolución del precio de la acción en los 10 días posteriores a una noticia significativa.
    
    Args:
        ticker (str): El ticker de la acción.
        df (DataFrame): Datos históricos del precio de la acción.
        noticia (dict): La noticia que ha sido clasificada como muy positiva o muy negativa.
        rango_dias (int): Número de días a analizar después de la noticia (por defecto es 10).
    
    Returns:
        dict: Información de la evolución del precio tras la noticia.
    """
    fecha_noticia = pd.to_datetime(noticia['fecha'], unit='s').date()
    
    df['Fecha'] = pd.to_datetime(df.index).date
    df_posterior = df[df['Fecha'] > fecha_noticia]
    
    if df_posterior.empty:
        return {
            'mensaje': 'No hay suficientes datos después de la fecha de la noticia.',
            'impacto_posterior': 0.0,
            'precio_inicio': None,
            'precio_fin': None
        }

    df_posterior = df_posterior.head(rango_dias)
    
    precio_inicio = df_posterior.iloc[0]['Close']
    precio_fin = df_posterior.iloc[-1]['Close']
    
    if precio_inicio == 0:
        return {
            'mensaje': 'El precio de inicio es 0, no se puede calcular el impacto.',
            'impacto_posterior': 0.0,
            'precio_inicio': precio_inicio,
            'precio_fin': precio_fin
        }
    
    impacto_posterior = ((precio_fin - precio_inicio) / precio_inicio) * 100
    
    return {
        'ticker': ticker,
        'fecha_noticia': fecha_noticia,
        'precio_inicio': precio_inicio,
        'precio_fin': precio_fin,
        'impacto_posterior': impacto_posterior,
        'rango_dias': rango_dias
    }