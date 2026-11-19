
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import json as js 
import joblib as jo 
import pandas as pd
import os
from exceptions import TaillesDifferentesError
from donnees import charger_donnees,DOSSIER_DONNEES,DOSSIER_PROJET

def separer_donnees(X : pd.DataFrame, y: pd.Series, taille_test: float=0.2, graine: int=42 ) -> tuple:
    """Sépare X et y en ensembles d'entraînement et de test.
    On va ici avoir X qui va etre le tableau entier de donne sans la colonne qualite qui va etre celle qu'on va chercher a deviner
    Y qui va etre uniquement la colonne qualite qui va etre celle a qui on va se fier pour voir si les resultats sont fiables
    taille_test va etre la proportion d'element que nous voullons predire et le reste va etre pour de la pratique et la graine = 42 c'est pour toujours avoir le 
    meme hasard pour avoir un resultat stable
    Elle va renvoyer un tuble. Et les erreurs vont etre levee quand X et y n’ont pas le même nombre de lignes
    """
    if len(X) != len(y):
        raise TaillesDifferentesError("X et y on un nombre de ligne differents")
    return train_test_split(X, y, test_size=taille_test, random_state=graine)

def rmse(y_reel : pd.Series, y_predit : np.ndarray) -> float:
    """Calcule la RMSE (erreur moyenne) avec NumPy.
    le y_reel va eter le resultat reel de notre base de donner alors que np.ndarray va etre la moyenne qu'on va avoir avec nos test et cela va 
    renvoyer la marge d'erreur"""
    return float(np.sqrt(np.mean((y_reel - y_predit) ** 2)))

def enregistrer_jo(modele : LinearRegression, chemin : str)-> None:
    """Recoie : modele qui est un objet de type sklearn et un chemin vers un dossier qui est un string
    renvoie None car on veut juste qu'elle ecrive dans le fichier 
    Et l'erreur possible ca va etre que le dossier n'existe pas (FileNotFoundError)"""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    jo.dump(modele, chemin)


def construire_metadonnees(X: pd.DataFrame, erreur: float) -> dict:
    """Construit le dictionnaire de métadonnées du modèle.

    Reçoit : X (pd.DataFrame), les colonnes d'entrée (sans la cible) ;
             erreur (float), la RMSE obtenue sur l'ensemble de test.
    renvoie un dict avec la RMSE et, pour chaque colonne, son min et son max.
    Et l'erreur c'est AttributeError si X n'est pas un DataFrame.
    """
    minimums = X.min()
    maximums = X.max()
    colonnes = {}
    for colonne in X.columns:
        colonnes[colonne] = {
            "min": float(minimums[colonne]),
            "max": float(maximums[colonne]),
        }
    return {"rmse": erreur, "colonnes": colonnes}


def enregistrer_metadonnees(metadonnees: dict, chemin: str) -> None:
    """Écrit les metadonnees dans un fichier JSON.
    Reçoit : metadonnees (dict), le dictionnaire à écrire ;
             chemin (str), le chemin du fichier .json à créer.
    renvoie None (la fonction écrit seulement le fichier).
    Et l'erreur c'est TypeError si le dictionnaire contient une valeur que JSON ne sait pas écrire.
    """
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as fichier:
        js.dump(metadonnees, fichier, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    donne = charger_donnees(os.path.join(DOSSIER_DONNEES, "winequalityred.csv"))
    X = donne.drop(columns=["quality"])   
    y = donne["quality"]              
    X_train, X_test, y_train, y_test = separer_donnees(X, y)

    modele = LinearRegression()
    modele.fit(X_train, y_train)    
    y_predit = modele.predict(X_test)          

    #CALCUL RMSEc
    print("RMSE modèle :", rmse(y_test, y_predit))
    print("RMSE référence :", rmse(y_test, y_train.mean())) 

    enregistrer_jo(modele,os.path.join(DOSSIER_PROJET, "modeles","modele.joblib"))

    metadonnees = construire_metadonnees(X, rmse(y_test, y_predit))
    enregistrer_metadonnees(metadonnees, os.path.join(DOSSIER_PROJET, "modeles", "metadonnees.json"))

