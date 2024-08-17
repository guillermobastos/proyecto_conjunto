import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import xgboost as xgb
from src.models.model_saver import save_model
from src.data.data_loader import load_data_from_file
from src.news.news_analyzer import analyze_sentiment
from src.models.model_predictor import make_predictions

def create_features(stock_data, news_data):
    # Procesa datos financieros: crea medias móviles, volatilidad, etc.
    stock_data['SMA_10'] = stock_data['Close'].rolling(window=10).mean()
    stock_data['Volatility'] = stock_data['Close'].rolling(window=10).std()

    # Agrega sentimiento de las noticias
    news_data['Sentiment'] = news_data['Text'].apply(analyze_sentiment)

    # Combina datos financieros y de noticias
    combined_data = pd.merge(stock_data, news_data, on='Date', how='left')

    # Crear lags de las características
    combined_data['Lag1_Close'] = combined_data['Close'].shift(1)
    combined_data['Lag1_Sentiment'] = combined_data['Sentiment'].shift(1)

    # Predecir el cambio porcentual de la acción
    combined_data['Pct_Change'] = combined_data['Close'].pct_change() * 100

    combined_data.dropna(inplace=True)

    return combined_data

def train_model(stock_data, news_data):
    # Crear características y etiqueta (target)
    data = create_features(stock_data, news_data)
    X = data[['SMA_10', 'Volatility', 'Lag1_Close', 'Lag1_Sentiment']]
    y = data['Pct_Change']

    # Dividir en conjunto de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Configurar los parámetros de XGBoost
    params = {
        'objective': 'reg:squarederror',
        'eval_metric': 'mae',
        'learning_rate': 0.1,
        'max_depth': 6,
        'n_estimators': 100,
        'random_state': 42
    }

    # Entrenar el modelo XGBoost
    model = xgb.XGBRegressor(**params)
    model.fit(X_train, y_train)

    # Evaluar el modelo
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Error absoluto medio en el conjunto de prueba: {mae}")

    return model

def train_and_predict():
    # Cargar datos
    stock_data = load_data_from_file('data/processed/stock_data_processed.csv')
    news_data = load_data_from_file('data/processed/news_data_processed.csv')

    # Entrenar el modelo
    model = train_model(stock_data, news_data)

    # Guardar el modelo en la carpeta models/modelos_entrenados
    model_filepath = 'models/modelos_entrenados/model_xgboost.pkl'
    save_model(model, model_filepath)

    # Realizar predicciones con nuevos datos
    predictions = make_predictions(model, stock_data, news_data)

    # Guardar predicciones
    predictions.to_csv('data/predictions/predictions.csv', index=False)

    print("Entrenamiento y predicciones completadas.")

if __name__ == "__main__":
    train_and_predict()
