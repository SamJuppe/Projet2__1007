import pandas as pd
"""On a séléctionné les neufs colonnes qu'on pense être le plus pertinent pour prédire le prix de sortie du marché."""
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
def charger_donnees(chemin) :
    return pd.read_csv(chemin, usecols=colonnes, parse_dates=["Date"]) 

def est_ce_que_il_ny_a__pas_de_strings_vide_True_or_False(fichier) -> bool:
    liste = []
    for elt in fichier:
        for nom in fichier[elt]:
            if pd.isna(nom) or str(nom).strip() == "":
                liste.append(nom)
    return len(liste) == 0 
print(est_ce_que_il_ny_a__pas_de_strings_vide_True_or_False(donnee))


if __name__ == "__main__":
    donne = charger_donnees("donnees/winequalityred.csv")
    print(est_ce_que_il_ny_a__pas_de_strings_vide_True_or_False(donne))
    print(donne.dtypes)
    print(donne.describe())
    donne.to_csv("donnees/donnees_selectionnees.csv", index=False)

