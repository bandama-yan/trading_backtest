from data.utils import*
from models.sma_strategy import apply_sma_strategy
from models.random_forest import train_random_forest
import matplotlib.pyplot as plt

def main ():
    """
    Main function to fetch, sort, and display stock data.
    """
    # Configuration
    ticker = "AAPL"
    start_date = "2020-01-01"
    end_date = "2024-12-31"
    
    # Fetch stock data
    stock_data = get_stock_data(ticker, start_date, end_date)
    if stock_data.empty:
        print("No data retrieved. Please check the ticker or date range.")
        return 

    # Sort stock data by 'Close' price
    sorted_data = sort_stock_data(stock_data)

    
    ### SMA STRATEGY
    result = apply_sma_strategy(sorted_data)

        # Measure and display performance
    show_performance(result)    

        # Display the first few rows of the result
    print("First few rows of the result:")
    display_stock_data(result[['Close', 'SMA_short', 'SMA_long', 'Signal', 'Strategy_Return']])

        # Save results to CSV
    save_to_csv(result[[ 'Signal','Return', 'Strategy_Return']],"results/sma_strategy_results.csv")


    ### RANDOM FOREST STRATEGY

        #Add features to the data
    df=add_features(sorted_data)
        # Train Random Forest model
    rf_model, X_test, y_test, preds = train_random_forest(df)

    # Generate trading signals
    df_trading = add_trading_signals(df, rf_model)

    # Compute strategy and market performance
    df_trading = compute_strategy_returns(df_trading)

    # Plot results
    plt.figure(figsize=(12,6))
    plt.plot(df_trading['Cumulative_Market_Return'], label='Market Return')
    plt.plot(df_trading['Cumulative_Strategy_Return'], label='Strategy Return')
    plt.legend()
    plt.title("Random Forest Long/Short Strategy vs Market")
    plt.show()

if __name__ == "__main__":
    main()
