def apply_sma_strategy(data, short_window=5, long_window=70):
    df = data.copy()
    df['SMA_short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['Close'].rolling(window=long_window).mean()

    # On crée un signal : 1 si SMA_short > SMA_long, 0 sinon
    df['Signal'] = (df['SMA_short'] > df['SMA_long']).astype(int)

    # La position = Signal du jour précédent pour éviter le look-ahead
    df['Position'] = df['Signal'].shift(1).fillna(0)

    # Retours
    df['Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Position'] * df['Return']

    return df.dropna()
