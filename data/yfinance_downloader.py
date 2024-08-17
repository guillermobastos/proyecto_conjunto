import yfinance as yf

def obtener_datos_tecnicos(ticker):
    """
    Obtiene indicadores técnicos para el ticker dado.
    
    Args:
        ticker (str): El ticker de la acción.
    
    Returns:
        dict: Diccionario con indicadores técnicos (ejemplo: RSI, MACD).
    """
    df = yf.download(ticker, period='6mo', interval='1d')

    # Calcular indicadores técnicos (ejemplos: RSI, MACD, medias móviles)
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    # RSI (Relative Strength Index)
    delta = df['Close'].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD (Moving Average Convergence Divergence)
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']

    # Seleccionar y devolver los últimos valores calculados
    datos_tecnicos = {
        'SMA_50': df['SMA_50'].iloc[-1],
        'SMA_200': df['SMA_200'].iloc[-1],
        'RSI': df['RSI'].iloc[-1],
        'MACD': df['MACD'].iloc[-1]
    }

    return datos_tecnicos

def obtener_datos_financieros(ticker):
    """
    Obtiene datos financieros para el ticker dado.
    
    Args:
        ticker (str): El ticker de la acción.
    
    Returns:
        dict: Diccionario con indicadores financieros (ejemplo: PER, deuda/capital).
    """
    stock = yf.Ticker(ticker)
    datos_financieros = stock.info
    
    # Obtener indicadores financieros clave
    per = datos_financieros.get('trailingPE', None)
    deuda_capital = datos_financieros.get('debtToEquity', None)
    margen_beneficio = datos_financieros.get('profitMargins', None)
    crecimiento_ingresos = datos_financieros.get('revenueGrowth', None)

    return {
        'PER': per,
        'Deuda/Capital': deuda_capital,
        'Margen_Beneficio': margen_beneficio,
        'Crecimiento_Ingresos': crecimiento_ingresos
    }
