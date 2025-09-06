def apply_sma_strategy(data, short_window=5, long_window=70):
    df = data.copy()
    df['SMA_short'] = df['Close'].rolling(window=short_window).mean()
    df['SMA_long'] = df['Close'].rolling(window=long_window).mean()

    # Create signal : 1 if SMA_short > SMA_long, 0 else
    df['Signal'] = (df['SMA_short'] > df['SMA_long']).astype(int)

    # position = Signal of the previous day for avoiding look-ahead
    df['Position'] = df['Signal'].shift(1).fillna(0)

    # Returns
    df['Return'] = df['Close'].pct_change()
    df['Strategy_Return'] = df['Position'] * df['Return']

    return df.dropna()
