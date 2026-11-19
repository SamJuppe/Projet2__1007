"""On a séléctionné les six colonnes qu'on pense être le plus pertinent pour prédire la qualite du vin avec les donnes entree par l'utilisateur"""
import os
import pandas as pd
from abc import ABC,abstractmethod
from exceptions import *
import json as json
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
    'residual sugar',
    "quality"
]
def charger_donnees(chemin: str) -> pd.DataFrame:
    """Ouvre le fichier avec les fonctions de pandas avec le chemin fournis. Il prend un string en entrer pour en faire sortir un objet
    du type Panda avec plus precisement un DataFrame. L'erreur possible va etre que python ne trouve pas le fichier en quesiton (FileNotFoundError) """
    if not os.path.exists(chemin):
        raise FichierIntrouvableError(f"Le fichier {chemin} est introuvable.") #ERREUR AFFICHE {chemin}
    return pd.read_csv(chemin, usecols=colonnes) 

def aucun_string_vide(fichier: pd.DataFrame) -> bool:
    """Grace au fonction de pandas on verifie sans faire de boucle et pour gagner de la vitesse. On utilise des vecteurs afin de savoir si il y a
    des string vide/= None dans notre fichier. Il va prendre le type qui vient de charger donne donc DataFrame pour en faire sortir un Bool. L'erreur 
    va etre si le fichier fournis n'est pas du type DatFrame"""
    return not fichier.isna().any().any()
def categoriser_sucre(donnees: pd.DataFrame) -> pd.DataFrame:
    """cette fonction va creer une colonne qu'on nomme sucre avec la fonction panda pd.cut avec les seuils de 0 a 4 c'est sec et pour tout ce qui est au dessus cela va 
    etre sucre"""
    bornes = [0, 4, 45]
    donnees = donnees.copy()
    donnees["sucre"] = pd.cut(donnees["residual sugar"], bins=bornes, labels=["sec", "sucré"], include_lowest=True)
    donnees = donnees.drop(columns=["residual sugar"])
    return donnees
def charger_metadonnees(chemin: str) -> dict:#a relire et comprendre 
    """cela va charger le fichier metadonne (.json)
    il va donc recevoir un string qui est le chemin vers le fichier
    et il va retourner un dictionnaire qui est dans le fichier json 
    la possible erreur est que le fichier n'existe 
    """
    if not os.path.exists(chemin):
        raise FichierIntrouvableError(f"Les métadonnées {chemin} sont introuvables. Lancez d'abord modele.py.")
    with open(chemin, encoding="utf-8") as fichier:
        return json.load(fichier)

class Variable(ABC):
    def __init__(self,nom : str) -> None :
        self._nom = nom
    # ############ get_choix a été retiré d'ici et déplacé dans VariableCategorielle (seule classe qui a self._choix)

    @abstractmethod
    def valider(self, saisie :str ) -> str|float:
        """Ce que va faire cette fonction grace au decorateur @abstractmethod tout les enfants tirer de cette
        Class vont obligatoirement devoir avoir une fonction valider. Sinon Python va systematiquement refuser
        l'application de la Classe enfants
        recoie : un str rentrer par l'utilisatueur
        renvoie : un float si c'est valider
        erreur : si ce n'est pas un float"""

    def get_nom(self) -> str:
        """etant donne que la variable self._nom est 'proteger' par la fonction on cree une fonction afin de pouvoir avoir son nom 
        en dehors de la class"""
        return self._nom
        
class VariableNumerique(Variable):
    def __init__(self,nom : str ,maxi : float ,mini : float) -> None:
        super().__init__(nom) 
        self._maxi = maxi
        self._mini = mini 
    def valider(self,saisie : str ) -> str|float : 
        """Ca va etre une fonction obligatoire du a la class Parent. Qui va valider ou non l'entrer saisie par l'utilisateur
        la sortie va etre un string ou un float. Un float si la saisie et bonne et un string si l'erruer n'est pas bonne
        Et les erreurs possible vont etre si la valeur et en dessous du minimum ou au dessus du maximum ou si la saisie est vide ou si ce n'est pas un nombre
        """
        if saisie.strip() == "" :
            raise StringVide("Veillez saisir quelque chose")
        try:
            nombre = float(saisie)
        except ValueError:
            raise Pasunnombre(f"{saisie} n'est pas une entree qui peut etre convertie en nombre")
        if not( self._mini  <= float(saisie)<= self._maxi):
            raise depasse_limite(f"Votre saisie : {saisie} doit etre compris entre {self._mini} et {self._maxi}")
        return float(saisie)
    def __str__(self) -> str: #polymorphisme
        """Renvoie une description lisible de la variable, utilisée par print()."""
        return f"{self._nom} : nombre entre {self._mini} et {self._maxi}"

class VariableCategorielle(Variable):
    def __init__(self, nom : str, choix: list[str]) -> None:
        super().__init__(nom)
        self._choix = choix
    def valider(self, saisie : str) ->str :
        """L'entrer va etre le type de sucre saisie par l'utilisateur
        la sortie va forcement etre un string, peut importe qu'il y est une erreur
        ou non
        Les Erreur possible vont etre si le string est vide, si la saisie n'est pas dans la liste 
        """   
        if saisie.strip() == "":
            raise StringVide("Votre saisie est vide veuillez saisir quelque chose") 
        if saisie.lower().strip() not in self._choix : 
            raise pas_dedans(f"Votre saisie : {saisie} n'est pas dans la liste : {self._choix}")
        return saisie.lower().strip()  
    def get_choix(self) -> list[str]:  
        """Renvoie la liste des choix possibles de la variable catégorielle.

        Reçoit : rien.
        Renvoie : la liste des choix (list[str]), ex. ["sec", "sucré"].
        Échoue : jamais, self._choix est toujours défini dans le constructeur.
        """
        return self._choix 
    def __str__(self) -> str:
        """Renvoie une description lisible de la variable, utilisée par print()."""
        return f"{self._nom} : un de {', '.join(self._choix)}"           
def creer_variables(metadonnees: dict) -> list[Variable]: #a relire et comprendre 
    """Crée la liste des variables d'entrée à partir des méta données du modèle.

    Reçoit : metadonnees (dict), le dictionnaire lu dans metadonnees.json.
    Renvoie : une liste de VariableNumerique et de VariableCategorielle,
              une par colonne d'entrée, dans le même ordre que le JSON.
    Échoue : KeyError si le dictionnaire n'a pas la clé "colonnes",
             ou si une colonne n'a pas les clés attendues ("type", "min", "max" ou "choix").
    """
    variables = []
    for nom, infos in metadonnees["colonnes"].items():
        if infos["type"] == "numerique":
            variables.append(VariableNumerique(nom, infos["max"], infos["min"]))
        else:
            variables.append(VariableCategorielle(nom, infos["choix"]))
    return variables

if __name__ == "__main__":
    donne = charger_donnees(os.path.join(DOSSIER_DONNEES, "winequalityred.csv"))  
    print(type(donne))
    print(aucun_string_vide(donne))
    print(donne.dtypes)
    print(donne.describe())
    donne.to_csv(os.path.join(DOSSIER_DONNEES, "donnees_selectionnees.csv"), index=False)


    

        