import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from donnees import donnee


def separer_donnees(X, y, taille_test=0.2, graine=42):
    """Sépare X et y en ensembles d'entraînement et de test."""
    return train_test_split(X, y, test_size=taille_test, random_state=graine)


if __name__ == "__main__":
    X = donnee.drop(columns=["quality"])   
    y = donnee["quality"]              
    X_train, X_test, y_train, y_test = separer_donnees(X, y)

    modele = LinearRegression()
    modele.fit(X_train, y_train)    
    y_predit = modele.predict(X_test) 

    print(y_predit[:5])                   
    print(y_test[:5].values)               

    #CALCUL RMSE
    print( type(donnee))