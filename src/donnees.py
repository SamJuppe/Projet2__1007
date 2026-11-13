import pandas as pd

''' '''
colonnes = [
    "alcohol",
    "sulphates",
    "volatile acidity",
    "citric acid",
    "total sulfur dioxide",
    "density",
    "quality"
]

donnee = pd.read_csv("donnees/winequalityred.csv", usecols=colonnes)
donnee.to_csv("donnees/donnees_selectionnees.csv", index=False)
def est_ce_que_il_ny_a__pas_de_strings_vide_True_or_False(fichier)-> bool: 
    liste = []
    for elt in fichier: 
        #print(elt) #prend toutes les colonnes
        for nom in fichier[elt] :
            if str(nom) == "":
                liste.append(nom)
    return len(liste) == 0 
print(est_ce_que_il_ny_a__pas_de_strings_vide_True_or_False(donnee))

