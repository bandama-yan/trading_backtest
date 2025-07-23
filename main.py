
from stock_utils import*

def main():
    # Configuration
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2024-12-31"

    # Fetch stock data
    stock_data = get_stock_data(ticker, start_date, end_date)

    if data.empty:
        print("No data retrieved. Please check the ticker or date range.")
        return
    
    # Sort stock data by 'Close' price
    sorted_data = sort_stock_data(stock_data)
    display_stock_data(sorted_data)