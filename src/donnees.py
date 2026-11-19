"""On a séléctionné les six colonnes qu'on pense être le plus pertinent pour prédire la qualite du vin avec les donnes entree par l'utilisateur"""
import os
import pandas as pd
from exceptions import FichierIntrouvableError

# Dossier racine du projet : on part de ce fichier (src/donnees.py) et on remonte de 2 crans.
DOSSIER_PROJET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_DONNEES = os.path.join(DOSSIER_PROJET, "donnees")
colonnes = [
    "alcohol",
    "sulphates",
    "volatile acidity",
    "citric acid",
    "total sulfur dioxide",
    "density",
    "quality"
]
def charger_donnees(chemin: str) -> pd.DataFrame:
    """Ouvre le fichier avec les fonctions de pandas avec le chemin fournis. Il prend un string en entrer pour en faire sortir un objet
    du type Panda avec plus precisement un DataFrame. L'erreur possible va etre que python ne trouve pas le fichier en quesiton (FileNotFoundError) """
    if not os.path.exists(chemin):
        raise FichierIntrouvableError(f"Le fichier {chemin} est introuvable.")
    return pd.read_csv(chemin, usecols=colonnes) 

def aucun_string_vide(fichier: pd.DataFrame) -> bool:
    """Grace au fonction de pandas on verifie sans faire de boucle et pour gagner de la vitesse. On utilise des vecteurs afin de savoir si il y a
    des string vide/= None dans notre fichier. Il va prendre le type qui vient de charger donne donc DataFrame pour en faire sortir un Bool. L'erreur 
    va etre si le fichier fournis n'est pas du type DatFrame"""
    return not fichier.isna().any().any()
            

if __name__ == "__main__":
    donne = charger_donnees(os.path.join(DOSSIER_DONNEES, "winequalityred.csv"))
    print(type(donne))
    print(aucun_string_vide(donne))
    print(donne.dtypes)
    print(donne.describe())
    donne.to_csv(os.path.join(DOSSIER_DONNEES, "donnees_selectionnees.csv"), index=False)

