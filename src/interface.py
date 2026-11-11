import matplotlib.pyplot as plt
from donnees import charger_donnees

donne = charger_donnees("donnees/finance_lol.csv")

indice = "Dow Jones"
un_indice = donne[donne["Stock Index"] == indice]
un_indice = un_indice.sort_values("Date")
plt.figure(figsize=(16, 7))   # 14 de large, 7 de haut

plt.scatter(un_indice["Date"], un_indice["Open Price"], label="Prix d'ouverture", s=10)
plt.scatter(un_indice["Date"], un_indice["Close Price"], label="Prix de clôture", s=10)
plt.title("Évolution des prix du S&P 500", fontsize=16)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Prix", fontsize=12)
plt.legend(fontsize=12)
plt.savefig("graphique_exploration.png", dpi=150)
plt.show()
