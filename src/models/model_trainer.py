import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from joblib import dump
import os
import sqlite3

def cargar_datos_ticker(ticker, db_path='database/noticias.db'):
    table_name = f'noticias_{ticker}'
    conn = sqlite3.connect(db_path)
    query = f"SELECT id, ticker, titulo, descripcion, fecha, impacto, clasificacion FROM {table_name}"
    try:
        df_noticias = pd.read_sql_query(query, conn)
    except pd.io.sql.DatabaseError as e:
        print(f"Error al ejecutar la consulta: {e}")
        df_noticias = pd.DataFrame()
    conn.close()
    return df_noticias

def entrenar_modelo(df, ticker, save_dir='models'):
    if df.empty:
        print("El DataFrame está vacío.")
        return None, None
    
    if df['descripcion'].isnull().sum() > 0:
        print("Hay valores nulos en la columna 'descripcion'.")
    
    # Mostrar las primeras filas para verificar datos
    print(df.head())
    
    # Preprocesar los datos
    vectorizer = TfidfVectorizer(stop_words=None, max_features=5000)  # Ajustar el vectorizador
    try:
        X = vectorizer.fit_transform(df['descripcion'])
    except ValueError as e:
        print(f"Error al ajustar el vectorizador: {e}")
        return None, None
    
    y = df['clasificacion']
    
    # Dividir los datos
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entrenar el modelo
    modelo = MultinomialNB()
    modelo.fit(X_train, y_train)
    
    # Evaluar el modelo
    y_pred = modelo.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    # Guardar el modelo y el vectorizador
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    modelo_path = os.path.join(save_dir, f'{ticker}_model.joblib')
    vectorizer_path = os.path.join(save_dir, f'{ticker}_vectorizer.joblib')
    dump(modelo, modelo_path)
    dump(vectorizer, vectorizer_path)
    
    return modelo, vectorizer

# Ejemplo de uso
df_noticias = cargar_datos_ticker('AAPL')
modelo, vectorizer = entrenar_modelo(df_noticias, 'AAPL')
