import pandas as pd

''' '''
colonnes = [
    "Stock Index",
    "Open Price",
    "Inflation Rate (%)",
    "Interest Rate (%)",
    "GDP Growth (%)",
    "Close Price",
    "Crude Oil Price (USD per Barrel)",
    "Gold Price (USD per Ounce)"
]

donnees = pd.read_csv("donnees/finance_lol.csv", usecols=colonnes)
donnees.to_csv("donnees/donnees_selectionnees.csv", index=False)
def est_ce_que_il_ny_a__pas_de_strings_vide_True_or_False(fichier)-> bool: 
    liste = []
    for elt in fichier: 
        print(elt) #prend toutes les colonnes
        for nom in fichier[elt] :
            if str(nom) == "":
                liste.append(nom)
    return len(liste) == 0 
print(est_ce_que_il_ny_a__pas_de_strings_vide_True_or_False(donnees))