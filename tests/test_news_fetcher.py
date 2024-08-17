import pytest
from src.news.news_classifier import clasificar_noticias_mejorado
from src.data.yfinance_downloader import obtener_datos_tecnicos, obtener_datos_financieros
from src.sentiment_analysis import obtener_datos_accion

def test_clasificar_noticias_mejorado():
    ticker = 'AAPL'
    noticias = [{'titulo': 'Sample News', 'descripcion': 'Sample description', 'fecha': 1692134400}]  # Fecha de ejemplo
    df = obtener_datos_accion(ticker)
    datos_tecnicos = obtener_datos_tecnicos(ticker)
    datos_financieros = obtener_datos_financieros(ticker)
    
    noticias_clasificadas = clasificar_noticias_mejorado(noticias, df, datos_tecnicos, datos_financieros)
    assert len(noticias_clasificadas) == len(noticias)
    assert 'clasificacion' in noticias_clasificadas[0]
