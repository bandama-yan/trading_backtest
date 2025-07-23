import yfinance as yf
import pandas as pd

def get_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker and date range.

    :param ticker: Stock symbol (e.g., 'AAPL')
    :param start_date: Start date in 'YYYY-MM-DD' format
    :param end_date: End date in 'YYYY-MM-DD' format
    :return: A pandas DataFrame with historical stock data
    """
    data = yf.download(ticker, start=start_date, end=end_date)
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
