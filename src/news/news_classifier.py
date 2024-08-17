from src.sentiment_analysis import calcular_impacto_noticia


def clasificar_noticias_mejorado(noticias, df, datos_tecnicos, datos_financieros):
    """
    Clasifica las noticias basándose en la variación del precio de la acción, datos técnicos y financieros.
    
    Args:
        noticias (list): Lista de noticias relacionadas con el ticker.
        df (DataFrame): Datos históricos del precio de la acción.
        datos_tecnicos (dict): Indicadores técnicos del ticker.
        datos_financieros (dict): Indicadores financieros de la empresa.
    
    Returns:
        list: Lista de noticias con su clasificación de impacto mejorada.
    """
    noticias_clasificadas = []
    for noticia in noticias:
        impacto = calcular_impacto_noticia(noticia['fecha'], df)
        
        # Ajustar la clasificación considerando indicadores técnicos y financieros
        if datos_tecnicos['RSI'] > 70:
            impacto -= 1
        elif datos_tecnicos['RSI'] < 30:
            impacto += 1

        if datos_financieros['PER'] > 30:
            impacto -= 1
        elif datos_financieros['PER'] < 10:
            impacto += 1
        
        # Clasificación en 7 niveles
        if impacto <= -10:
            clasificacion = 0  # Muy Negativa
        elif -10 < impacto <= -5:
            clasificacion = 1  # Negativa
        elif -5 < impacto <= -1:
            clasificacion = 2  # Ligeramente Negativa
        elif -1 < impacto <= 1:
            clasificacion = 3  # Neutra
        elif 1 < impacto <= 5:
            clasificacion = 4  # Ligeramente Positiva
        elif 5 < impacto <= 10:
            clasificacion = 5  # Positiva
        elif impacto > 10:
            clasificacion = 6  # Muy Positiva
        
        noticias_clasificadas.append({
            'titulo': noticia['titulo'],
            'descripcion': noticia['descripcion'],
            'fecha': noticia['fecha'],
            'impacto': impacto,
            'clasificacion': clasificacion
        })
    
    return noticias_clasificadas
