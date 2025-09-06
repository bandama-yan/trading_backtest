import yfinance as yf
import pandas as pd
import os

def get_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker and date range.

    :param ticker: Stock symbol (e.g., 'AAPL')
    :param start_date: Start date in 'YYYY-MM-DD' format
    :param end_date: End date in 'YYYY-MM-DD' format
    :return: A pandas DataFrame with historical stock data
    """
    data = yf.download(ticker, start=start_date, end=end_date)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)
    return data

def sort_stock_data(data, column='Close', ascending=True):
    """
    Sort stock data based on a specific column.

    :param data: DataFrame containing stock data
    :param column: Column to sort by (default is 'Close')
    :param ascending: Sort order (default is True for ascending)
    :return: A sorted DataFrame
    """
    
    return data.sort_values(by=column, ascending=ascending)

def display_stock_data(data, rows=10):
    """
    Display the first few rows of the stock data.

    :param data: DataFrame containing stock data
    :param rows: Number of rows to display (default is 10)
    """
    print(data.head(rows))

def show_performance(df):
    cum_strategy = (1 + df['Strategy_Return']).prod() - 1
    cum_market = (1 + df['Return']).prod() - 1
    print(f"Buy and Hold Return: {cum_market*100:.2f}%")
    print(f"SMA strategy Return: {cum_strategy*100:.2f}%")

def save_to_csv(df, filename):
    """
    Save DataFrame to a CSV file.
    :param df: DataFrame to save
    :param filename: Name of the CSV file
    """
    if not os.path.exists("results"):
        os.makedirs("results")
    df.to_csv(filename) 

def prepare_data(df):
    """
    Prepare features and target for classification.
    Target = 1 if tomorrow's close price > today's close price, else 0.
    """
    df = df.copy()
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    df = df[:-1]  # remove last row (NaN)
    
    features = ['Close', 'SMA_short', 'SMA_long']
    X = df[features]
    y = df['Target']
    return X, y

def add_features(df):
    """
    Add technical indicators to the stock data.
    """
    df = df.copy()
    df['SMA_short'] = df['Close'].rolling(window=10).mean()
    df['SMA_long'] = df['Close'].rolling(window=50).mean()
    return df


def add_trading_signals(df, model):
    """
    Add trading signals based on model predictions.
    Signal = 1 → Buy (go long)
    Signal = -1 → Sell (go short)
    """
    # Prepare features and target
    X, y = prepare_data(df)
    
    # Align dataframe with the number of rows in X
    df_trading = df.iloc[-len(X):].copy()
    
    # Predict market direction with the trained model
    df_trading['Prediction'] = model.predict(X)
    
    # Map predictions to trading signals:
    # 1 means the model expects an upward move (go long),
    # 0 means the model expects a downward move → we treat it as -1 (go short).
    df_trading['Signal'] = df_trading['Prediction'].replace({0: -1, 1: 1})
    
    return df_trading


def compute_strategy_returns(df_trading):
    """
    Compute strategy returns using the trading signals.
    - If Signal = 1 → profit from positive returns (long).
    - If Signal = -1 → profit from negative returns (short).
    """
    # Daily percentage change of closing price
    df_trading['Return'] = df_trading['Close'].pct_change()
    
    # Strategy return:
    # Signal of the previous day * today's market return
    # → if long yesterday and price goes up, you profit.
    # → if short yesterday and price goes down, you profit.
    df_trading['Strategy_Return'] = df_trading['Signal'].shift(1) * df_trading['Return']
    
    # Cumulative returns over time
    df_trading['Cumulative_Strategy_Return'] = (1 + df_trading['Strategy_Return']).cumprod()
    df_trading['Cumulative_Market_Return'] = (1 + df_trading['Return']).cumprod()
    
    return df_trading