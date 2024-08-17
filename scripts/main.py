from datetime import datetime, timedelta
import sys
import os
import pandas as pd
# Agrega la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.sentiment_analysis import obtener_noticias, obtener_datos_accion, clasificar_noticias, entrenar_modelo, evolucion_posterior_noticia


def main():
    tickers = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'VUKE', 'DIS', 'NFLX',
    ]
    
    # Obtener la fecha de ayer en formato 'YYYY-MM-DD'
    fecha_hoy = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Crear un DataFrame vacío para almacenar todos los resultados
    resultados_totales = pd.DataFrame(columns=["Ticker", "Título", "Descripción", "Fecha", "Impacto", "Clasificación"])

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
                
                # Añadir las noticias clasificadas al DataFrame
                for noticia in noticias_clasificadas:
                    impacto_redondeado = round(noticia['impacto'], 4)
                    resultados_totales = resultados_totales._append({
                        "Ticker": ticker,
                        "Título": noticia['titulo'],
                        "Descripción": noticia['descripcion'],
                        "Fecha": noticia['fecha'],
                        # "Impacto": noticia['impacto'],
                        "Impacto": impacto_redondeado,
                        "Clasificación": noticia['clasificacion']
                    }, ignore_index=True)
                    
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
