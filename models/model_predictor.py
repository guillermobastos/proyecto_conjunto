import pandas as pd

from scripts.entrenar_y_predecir import create_features
def make_predictions(model, stock_data, news_data):
    # Crear las mismas características que se usaron para el entrenamiento
    data = create_features(stock_data, news_data)
    X = data[['SMA_10', 'Volatility', 'Lag1_Close', 'Lag1_Sentiment']]
    
    # Hacer predicciones
    predictions = model.predict(X)
    
    # Retornar predicciones en un DataFrame
    predictions_df = pd.DataFrame({
        'Date': data['Date'],
        'Predicted_Pct_Change': predictions
    })
    
    return predictions_df
