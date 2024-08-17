from flask import Flask, render_template, request
from sqlalchemy import Table
import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Agrega la carpeta raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database_config import engine, metadata 

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    # Obtener la lista de tickers disponibles en la base de datos
    tickers = obtener_lista_tickers()
    ticker_seleccionado = request.args.get('ticker')
    noticias = []

    if ticker_seleccionado:
        # Filtrar las noticias por el ticker seleccionado
        noticias = obtener_noticias_por_ticker(ticker_seleccionado)

    return render_template('index.html', tickers=tickers, ticker_seleccionado=ticker_seleccionado, noticias=noticias)

def obtener_lista_tickers():
    # Obtener la lista de tablas en la base de datos
    metadata.reflect(bind=engine)
    tickers = [table.name.replace('noticias_', '') for table in metadata.tables.values()]
    return tickers

def obtener_noticias_por_ticker(ticker):
    table_name = f"noticias_{ticker}"
    table = Table(table_name, metadata, autoload_with=engine)
    
    # Usar una sesión para manejar la consulta
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Ejecutar la consulta
        select_stmt = table.select()
        result = session.execute(select_stmt)
        
        # Obtener nombres de columnas
        column_names = result.keys()
        
        # Convertir filas en diccionarios usando nombres de columnas
        noticias = [dict(zip(column_names, row)) for row in result]
        
    except SQLAlchemyError as e:
        print(f"Error al obtener noticias para {ticker}: {e}")
        noticias = []

    finally:
        session.close()
    
    return noticias


if __name__ == '__main__':
    app.run(debug=True)
