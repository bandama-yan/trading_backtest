# importation des modules
import yfinance as yf

# Récupération des données boursières
def get_stock_data(ticker, start_date, end_date):
    """
    Récupère les données boursières pour un ticker donné entre deux dates.
    
    :param ticker: Le symbole boursier de l'instrument financier
    :param start_date: La date de début au format 'YYYY-MM-DD'
    :param end_date: La date de fin au format 'YYYY-MM-DD'
    :return: Un DataFrame contenant les données boursières
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

