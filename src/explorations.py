from donnees import charger_donnees
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from donnees import DOSSIER_DONNEES,DOSSIER_PROJET


if __name__ == "__main__":
    donne = charger_donnees(os.path.join(DOSSIER_DONNEES,"donnees_selectionnees.csv"))
    print(donne["quality"].value_counts().sort_index()) # on observe que il n'y a aucun vin qui a une note de 1-2-9-10 dans la base de donnee

    print(donne["volatile acidity"])
    plt.scatter(donne["volatile acidity"],donne["quality"], s = 5, label = "Un point = un vin")
    plt.xlabel('ACIDITE g/L')
    plt.ylabel('QUALITE')
    plt.legend()
    plt.title("Qualite par rapport a l'acidite du vin")
    plt.savefig(os.path.join(DOSSIER_PROJET,"Capture_Ecran","nuage_points.png"))
    plt.show()

    counts, bornes, barres = plt.hist(donne["alcohol"], bins=20, label="alcohol")

    # Pour chaque vin, numéro de la colonne dans laquelle il tombe
    intervalles = pd.cut(donne["alcohol"], bins=bornes, include_lowest=True)
    moyennes = donne.groupby(intervalles, observed=False)["quality"].mean()

    # Écrire la moyenne au-dessus de chaque barre
    for barre, moy in zip(barres, moyennes):
        if not np.isnan(moy):           # colonne vide → pas de moyenne
            x = barre.get_x() + barre.get_width() / 2
            y = barre.get_height()
            plt.text(x, y + 3, f"{moy:.1f}", ha="center", fontsize=8)

    plt.xlabel("Taux d'alcool (%)")
    plt.ylabel("Nombre de vins")
    plt.title("Moyenne par rapport a leurs %")
    plt.legend()
    plt.savefig(os.path.join(DOSSIER_PROJET,"Capture_Ecran","histogramme.png"))
    plt.show()