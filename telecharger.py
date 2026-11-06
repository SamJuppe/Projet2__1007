import pandas as pd

colonnes = [
    "Stock Index",
    "Open Price",
    "Inflation Rate (%)",
    "Interest Rate (%)",
    "GDP Growth (%)",
    "Close Price"
]

donnees = pd.read_csv("finance_lol.csv", usecols=colonnes)
donnees.to_csv("donnees_selectionnees.csv", index=False)
print("Fichier donnees_selectionnees.csv créé !")