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

# Fonction pour trier les données
def sort_stock_data(stock_data, column='Close', ascending=True):
    """
    Trie les données boursières par une colonne spécifique.
    
    :param stock_data: Un DataFrame contenant les données boursières
    :param column: La colonne par laquelle trier (par défaut 'Close')
    :param ascending: Ordre de tri (par défaut True pour croissant)
    :return: Un DataFrame trié
    """
    return stock_data.sort_values(by=column, ascending=ascending)
    
# Fonction pour afficher les données
def display_stock_data(stock_data):
    """
    Affiche les données boursières.
    
    :param stock_data: Un DataFrame contenant les données boursières
    """
    print(stock_data)