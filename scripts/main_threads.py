from datetime import datetime, timedelta
import sys
import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Agrega la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sentiment_analysis import obtener_noticias, obtener_datos_accion, clasificar_noticias, entrenar_modelo, evolucion_posterior_noticia

def leer_tickers(desde_archivo):
    """Lee los tickers desde un archivo CSV y devuelve una lista de tickers."""
    try:
        df_tickers = pd.read_csv(desde_archivo)
        return df_tickers['Ticker'].tolist()
    except Exception as e:
        print(f"Error al leer el archivo de tickers: {e}")
        return []

def procesar_ticker(ticker):
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
                impacto_redondeado = round(noticia['impacto'], 4)
                resultado = {
                    "Ticker": ticker,
                    "Título": noticia['titulo'],
                    "Descripción": noticia['descripcion'],
                    "Fecha": noticia['fecha'],
                    "Impacto": impacto_redondeado,
                    "Clasificación": noticia['clasificacion']
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
                if noticia['clasificacion'] in [0, 7]:
                    evolucion = evolucion_posterior_noticia(ticker, df, noticia)
                    print(f"Evolución después de la noticia: {evolucion['impacto_posterior']:.2f}% en {evolucion['rango_dias']} días.")
                    print(f"Precio inicial: {evolucion['precio_inicio']:.2f}, Precio final: {evolucion['precio_fin']:.2f}")
                    print(f"Detalles: {evolucion['mensaje'] if 'mensaje' in evolucion else 'Evolución completada.'}")
                    print()
    else:
        print(f"No se encontraron noticias para {ticker}.")
    
    return resultados_ticker

def main():
    # Definir la ruta del archivo de tickers
    ruta_archivo_tickers = os.path.join('data', 'tickers', 'tickers.csv')
    
    # Leer los tickers desde el archivo
    tickers = leer_tickers(ruta_archivo_tickers)
    
    if not tickers:
        print("No se encontraron tickers en el archivo.")
        return
    
    # Obtener la fecha de ayer en formato 'YYYY-MM-DD'
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    
    # Crear un DataFrame vacío para almacenar todos los resultados
    resultados_totales = pd.DataFrame(columns=["Ticker", "Título", "Descripción", "Fecha", "Impacto", "Clasificación"])

    # Usar ThreadPoolExecutor para procesar tickers en paralelo
    with ThreadPoolExecutor(max_workers=len(tickers)) as executor:
        # Enviar tareas al executor
        future_to_ticker = {executor.submit(procesar_ticker, ticker): ticker for ticker in tickers}
        
        # Obtener los resultados a medida que se completan las tareas
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                resultados_ticker = future.result()
                # Añadir resultados al DataFrame principal
                resultados_totales = pd.concat([resultados_totales, pd.DataFrame(resultados_ticker)], ignore_index=True)
            except Exception as exc:
                print(f"{ticker} generó una excepción: {exc}")
    
    # Guardar los resultados en un archivo Excel
    año_actual = datetime.today().strftime('%Y')
    archivo_excel = f"resultados_noticias_{fecha_hoy}.xlsx"
    
    # Construir la ruta donde se guardará el archivo
    ruta_guardado = os.path.join('data', 'time', año_actual)
    os.makedirs(ruta_guardado, exist_ok=True)
    ruta_completa_archivo = os.path.join(ruta_guardado, archivo_excel)
    
    # Guardar el DataFrame en el archivo Excel en la ruta correspondiente
    resultados_totales.to_excel(ruta_completa_archivo, index=False)
    print(f"Resultados guardados en {ruta_completa_archivo}")

if __name__ == "__main__":
    main()
