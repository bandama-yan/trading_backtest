from data.utils import*
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def train_random_forest(df):
    """
    Train a Random Forest on the data.
    """
    X, y = prepare_data(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    preds = rf.predict(X_test)
    
    print("Random Forest Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))
    
    return rf, X_test, y_test, preds
