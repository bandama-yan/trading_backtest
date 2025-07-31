import os
from data.utils import*
from models.sma_strategy import apply_sma_strategy


def main ():
    """
    Main function to fetch, sort, and display stock data.
    """
    # Configuration
    ticker = "AAPL"
    start_date = "2023-01-01"
    end_date = "2024-12-31"
    
    # Fetch stock data
    stock_data = get_stock_data(ticker, start_date, end_date)
    if stock_data.empty:
        print("No data retrieved. Please check the ticker or date range.")
        return 

    # Sort stock data by 'Close' price
    sorted_data = sort_stock_data(stock_data)
    
    # Apply SMA strategy
    result = apply_sma_strategy(sorted_data)

    # Measure and display performance
    show_performance(result)    

    # Display the first few rows of the result
    print("First few rows of the result:")
    display_stock_data(result[['Close', 'SMA_short', 'SMA_long', 'Signal', 'Strategy_Return']])

    # Save results to CSV
    if not os.path.exists("results"):
        os.makedirs("results")
    result.to_csv("results/sma_results.csv")

if __name__ == "__main__":
    main()
