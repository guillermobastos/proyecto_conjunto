import sqlite3
import pandas as pd
import os

def cargar_datos_ticker(ticker, db_path='database/noticias.db'):
    # Definir el nombre de la tabla basado en el ticker
    table_name = f'noticias_{ticker}'
    
    # Imprimir la ruta para verificar
    print(f"Ruta a la base de datos: {db_path}")
    
    # Conectar a la base de datos SQLite
    conn = sqlite3.connect(db_path)
    
    # Consulta SQL para extraer las noticias de la tabla específica
    query = f"""
    SELECT id, ticker, titulo, descripcion, fecha, impacto, clasificacion
    FROM {table_name}
    """
    
    try:
        # Ejecutar la consulta y cargar los datos en un DataFrame
        df_noticias = pd.read_sql_query(query, conn)
    except pd.io.sql.DatabaseError as e:
        print(f"Error al ejecutar la consulta: {e}")
        df_noticias = pd.DataFrame()  # Devolver un DataFrame vacío en caso de error
    
    # Cerrar la conexión a la base de datos
    conn.close()
    
    return df_noticias

# Ejemplo de uso
# df_noticias = cargar_datos_ticker('MSFT')
# print(df_noticias.head())
