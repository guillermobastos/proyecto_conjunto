import os
import sys
import pandas as pd
from sqlalchemy import Column, Float, Integer, String, Table
from sqlalchemy.exc import SQLAlchemyError

# Agrega la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_config import engine, metadata 
from src.sentiment_analysis import (
    clasificar_noticias,
    entrenar_modelo,
    evolucion_posterior_noticia,
    obtener_datos_accion,
    obtener_noticias,
)

def leer_tickers(desde_archivo):
    """Lee los tickers desde un archivo CSV y devuelve una lista de tickers."""
    try:
        df_tickers = pd.read_csv(desde_archivo)
        return df_tickers["Ticker"].tolist()
    except Exception as e:
        print(f"Error al leer el archivo de tickers: {e}")
        return []

def crear_tabla(ticker):
    """Crea una tabla para un ticker específico en la base de datos, si no existe ya."""
    table_name = f"noticias_{ticker}"
    table = Table(
        table_name,
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("ticker", String(10), nullable=False),
        Column("titulo", String(255), nullable=False),
        Column("descripcion", String, nullable=False),
        Column("fecha", String(19), nullable=False),
        Column("impacto", Float, nullable=False),
        Column("clasificacion", Integer, nullable=False),
        extend_existing=True,
    )
    # Crear la tabla si no existe
    metadata.create_all(engine, tables=[table])
    print(f"Tabla '{table_name}' creada o verificada.")
    return table

def procesar_ticker(ticker):
    """Procesa las noticias para un ticker específico."""
    print(f"Buscando noticias para: {ticker}")
    noticias = obtener_noticias(ticker)
    resultados_ticker = []

    if noticias:
        print(f"Noticias obtenidas para {ticker}: {len(noticias)}")

        df = obtener_datos_accion(ticker)
        noticias_clasificadas = clasificar_noticias(noticias, df)

        print(f"Noticias clasificadas para {ticker}: {len(noticias_clasificadas)}")

        modelo = entrenar_modelo(noticias_clasificadas)
        if modelo:
            print(f"Modelo entrenado para {ticker}.")

            for noticia in noticias_clasificadas:
                impacto_redondeado = round(noticia["impacto"], 4)
                resultado = {
                    "ticker": ticker,
                    "titulo": noticia["titulo"],
                    "descripcion": noticia["descripcion"],
                    "fecha": noticia["fecha"],
                    "impacto": impacto_redondeado,
                    "clasificacion": noticia["clasificacion"],
                }
                resultados_ticker.append(resultado)

                # Mostrar los resultados en la consola
                print(f"Título: {noticia['titulo']}")
                print(f"Descripción: {noticia['descripcion']}")
                print(f"Fecha: {noticia['fecha']}")
                print(f"Impacto en la acción: {noticia['impacto']:.2f}%")
                print(f"Clasificación: {noticia['clasificacion']}")
                print()

                # Si la clasificación es 0 (muy negativa) o 7 (muy positiva), analizar la evolución posterior
                if noticia["clasificacion"] in [0, 7]:
                    evolucion = evolucion_posterior_noticia(ticker, df, noticia)
                    print(
                        f"Evolución después de la noticia: {evolucion['impacto_posterior']:.2f}% en {evolucion['rango_dias']} días."
                    )
                    print(
                        f"Precio inicial: {evolucion['precio_inicio']:.2f}, Precio final: {evolucion['precio_fin']:.2f}"
                    )
                    print(
                        f"Detalles: {evolucion['mensaje'] if 'mensaje' in evolucion else 'Evolución completada.'}"
                    )
                    print()
    else:
        print(f"No se encontraron noticias para {ticker}.")

    return resultados_ticker

def guardar_datos_en_tabla(df_resultados_ticker, table):
    """Guarda los datos en la tabla especificada."""
    try:
        with engine.connect() as conn:
            for _, row in df_resultados_ticker.iterrows():
                conn.execute(
                    table.insert().values(
                        ticker=row["ticker"],
                        titulo=row["titulo"],
                        descripcion=row["descripcion"],
                        fecha=row["fecha"],
                        impacto=row["impacto"],
                        clasificacion=row["clasificacion"],
                    )
                )
                conn.commit() # Muy importante para guardar los datos y se actualice
        print(f"Resultados guardados en la base de datos.")
    except SQLAlchemyError as e:
        print(f"Error al guardar los resultados: {e}")

def main():
    """Función principal para ejecutar el procesamiento de tickers y guardar los resultados en la base de datos."""
    # Definir la ruta del archivo de tickers
    ruta_archivo_tickers = os.path.join("data", "tickers", "tickers.csv")

    # Leer los tickers desde el archivo
    tickers = leer_tickers(ruta_archivo_tickers)

    if not tickers:
        print("No se encontraron tickers en el archivo.")
        return

    for ticker in tickers:
        # Crear tabla para el ticker
        table = crear_tabla(ticker)

        # Procesar noticias para el ticker
        resultados_ticker = procesar_ticker(ticker)

        if resultados_ticker:
            df_resultados_ticker = pd.DataFrame(resultados_ticker)
            # Filtrar columnas vacías o con solo NA
            df_resultados_ticker = df_resultados_ticker.dropna(how="all", axis=1)

            # Guardar resultados en la tabla del ticker
            guardar_datos_en_tabla(df_resultados_ticker, table)

def prueba():
    """Lee los tickers desde un archivo CSV y devuelve una lista de tickers."""
    try:
        df_tickers = pd.read_csv(os.path.join("data", "tickers", "tickers.csv"))
        return df_tickers["Ticker"].tolist()
    except Exception as e:
        print(f"Error al leer el archivo de tickers: {e}")
        return []                 

if __name__ == "__main__": 
    main()