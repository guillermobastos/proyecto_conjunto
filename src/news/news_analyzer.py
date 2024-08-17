# src/news/news_analyzer.py
from datetime import datetime, timedelta
import sys
import os
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

# Agrega la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sentiment_analysis import obtener_noticias, obtener_datos_accion, clasificar_noticias, entrenar_modelo, evolucion_posterior_noticia
from app import db, Noticia  # Importa la base de datos y el modelo Noticia

def main():
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'VUKE', 'DIS', 'NFLX',
    ]
    
    fecha_hoy = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    for ticker in tickers:
        print(f"Buscando noticias para: {ticker} en {fecha_hoy}")
        noticias = obtener_noticias(ticker)
        
        if noticias:
            print(f"Noticias obtenidas para {ticker}: {len(noticias)}")
            
            df = obtener_datos_accion(ticker)
            noticias_clasificadas = clasificar_noticias(noticias, df)
            
            print(f"Noticias clasificadas para {ticker}: {len(noticias_clasificadas)}")
            
            modelo = entrenar_modelo(noticias_clasificadas)
            if modelo:
                print(f"Modelo entrenado para {ticker}.")
                
                for noticia in noticias_clasificadas:
                    nueva_noticia = Noticia(
                        ticker=ticker,
                        titulo=noticia['titulo'],
                        descripcion=noticia['descripcion'],
                        fecha=noticia['fecha'],
                        impacto=noticia['impacto'],
                        clasificacion=noticia['clasificacion']
                    )
                    db.session.add(nueva_noticia)
                db.session.commit()

                for noticia in noticias_clasificadas:
                    print(f"Título: {noticia['titulo']}")
                    print(f"Descripción: {noticia['descripcion']}")
                    print(f"Fecha: {noticia['fecha']}")
                    print(f"Impacto en la acción: {noticia['impacto']:.2f}%")
                    print(f"Clasificación: {noticia['clasificacion']}")
                    print()

                    if noticia['clasificacion'] in [0, 7]:
                        evolucion = evolucion_posterior_noticia(ticker, df, noticia)
                        print(f"Evolución después de la noticia: {evolucion['impacto_posterior']:.2f}% en {evolucion['rango_dias']} días.")
                        print(f"Precio inicial: {evolucion['precio_inicio']:.2f}, Precio final: {evolucion['precio_fin']:.2f}")
                        print(f"Detalles: {evolucion['mensaje'] if 'mensaje' in evolucion else 'Evolución completada.'}")
                        print()

        else:
            print(f"No se encontraron noticias para {ticker}.")
    
    print(f"Resultados guardados en la base de datos.")

if __name__ == "__main__":
    main()
