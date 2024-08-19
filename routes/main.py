from flask import Blueprint, render_template, request
from sqlalchemy import Table, desc, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from database_config import engine, metadata

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    # Obtener la lista de tickers disponibles en la base de datos
    tickers = obtener_lista_tickers()
    ticker_seleccionado = request.args.get('ticker')
    tipo_orden = request.args.get('orden')  # 'asc' o 'desc'
    noticias = []

    if ticker_seleccionado:
        if tipo_orden:
            # Usar la función para obtener noticias ordenadas por impacto
            noticias = obtener_noticias_ordenadas_por_impacto(ticker_seleccionado, tipo_orden)
        else:
            # Usar la función original para obtener noticias sin orden específico
            noticias = obtener_noticias_por_ticker(ticker_seleccionado)

    return render_template('index.html', tickers=tickers, ticker_seleccionado=ticker_seleccionado, noticias=noticias)



def obtener_lista_tickers():
    metadata.reflect(bind=engine)
    tickers = [table.name.replace('noticias_', '') for table in metadata.tables.values()]
    return tickers

def obtener_noticias_por_ticker(ticker):
    table_name = f"noticias_{ticker}"
    table = Table(table_name, metadata, autoload_with=engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        select_stmt = table.select()
        result = session.execute(select_stmt)
        column_names = result.keys()
        noticias = [dict(zip(column_names, row)) for row in result]
        
    except SQLAlchemyError as e:
        print(f"Error al obtener noticias para {ticker}: {e}")
        noticias = []
    finally:
        session.close()
    
    return noticias


def obtener_noticias_ordenadas_por_impacto(ticker, tipo_orden):
    """Obtiene las noticias para un ticker específico, ordenadas por impacto según el tipo de orden."""
    table_name = f"noticias_{ticker}"
    table = Table(table_name, metadata, autoload_with=engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Seleccionar el tipo de orden
        if tipo_orden == 'asc':
            order = asc(table.c.impacto)
        else:
            order = desc(table.c.impacto)
        
        # Ordenar las noticias por impacto
        select_stmt = table.select().order_by(order)
        result = session.execute(select_stmt)
        column_names = result.keys()
        noticias = [dict(zip(column_names, row)) for row in result]
        
    except SQLAlchemyError as e:
        print(f"Error al obtener noticias ordenadas para {ticker}: {e}")
        noticias = []
    finally:
        session.close()
    
    return noticias