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

