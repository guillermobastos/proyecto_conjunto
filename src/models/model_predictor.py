def predecir_impacto_noticia_mejorado(modelo, texto_noticia, datos_tecnicos, datos_financieros):
    """
    Predice el impacto de una nueva noticia utilizando el modelo entrenado y datos adicionales.
    
    Args:
        modelo: El modelo entrenado.
        texto_noticia (str): Texto de la nueva noticia.
        datos_tecnicos (dict): Indicadores técnicos del ticker.
        datos_financieros (dict): Indicadores financieros de la empresa.
    
    Returns:
        str: La predicción del impacto de la noticia.
    """
    prediccion = modelo.predict([texto_noticia])
    
    # Ajustar la predicción considerando los datos técnicos y financieros
    if datos_tecnicos['RSI'] > 70:
        prediccion -= 1
    elif datos_tecnicos['RSI'] < 30:
        prediccion += 1

    if datos_financieros['PER'] > 30:
        prediccion -= 1
    elif datos_financieros['PER'] < 10:
        prediccion += 1

    return prediccion[0]
