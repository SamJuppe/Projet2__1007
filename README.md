# Qualité du vin rouge · INF1007

Cette application Tkinter estime une note de qualité sur 10 à partir de sept caractéristiques d'un vin rouge. Elle affiche la note sur la distribution des observations et conserve les prédictions dans un CSV local.

## Données et préparation

Le fichier contient 1 599 vins rouges du jeu [Wine Quality de Cortez et coll. (UCI)](https://archive.ics.uci.edu/dataset/186/wine+quality). La [fiche UCI](https://archive.ics.uci.edu/dataset/186/wine+quality) indique une licence CC BY 4.0. La [version Kaggle](https://www.kaggle.com/datasets/uciml/red-wine-quality-cortez-et-al-2009) affiche « Database: Open Database, Contents: Database Contents » (DbCL v1.0 pour le contenu). Le fichier contient des mesures physicochimiques et des notes, sans données personnelles.

On a vérifié les types, les valeurs manquantes et les statistiques descriptives. Les huit colonnes lues sont numériques et complètes. On conserve six mesures numériques et on transforme le sucre résiduel en une catégorie : sec jusqu'à 4 g/L, sucré au-delà (seuil simplifié pour le projet).

Avec la règle de 1,5 fois l'écart interquartile, les valeurs extrêmes repérées étaient 19 pour l'acidité volatile, 1 pour l'acide citrique, 155 pour le sucre résiduel, 55 pour le SO₂ total, 45 pour la densité, 59 pour les sulfates et 13 pour l'alcool. Les observations ont été conservées : le seuil statistique seul ne suffit pas à conclure qu'une mesure est erronée.

Voir les graphiques dans [Capture_Ecran](Capture_Ecran), dont le [nuage prédit contre réel](Capture_Ecran/predit_contre_reel.png).

## Évaluation

La cible est la colonne `quality`. La RMSE s'exprime en points de qualité et pénalise davantage les grandes erreurs. La séparation est de 80 % pour l'entraînement et 20 % pour le test avec `random_state=42`.

| Sur le même jeu de test | RMSE |
| --- | ---: |
| Moyenne des notes d'entraînement | 0,8107 |
| Régression linéaire | 0,6335 |

La régression réduit la RMSE d'environ 21,9 %. Les notes 5 et 6 représentent 1 319 des 1 599 observations, et les notes observées s'étendent de 3 à 8. Les notes rares et les vins provenant d'autres populations peuvent être moins bien estimés. La RMSE décrit les erreurs sur le jeu de test et ne donne pas un intervalle de prédiction individuel.

## Installation et lancement

Utiliser Python 3.14 avec Tkinter. Sous Windows :

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src/main.py
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m coverage run --source=src -m pytest
.\.venv\Scripts\python.exe -m coverage report -m
```

Sous macOS ou Linux, utiliser `.venv/bin/python` dans les mêmes commandes. Vérifier Tkinter avec `python -m tkinter`.

L'application utilise le modèle et les métadonnées fournis dans `modeles/`. Pour les régénérer, lancer `python src/modele.py`. Pour reproduire les graphiques d'exploration, lancer `python src/explorations.py`.

Les 21 cas pytest passent. La couverture globale mesurée est de **28 %** sur les lignes de src/. Les tests automatisés ciblent surtout les données, le modèle et l’historique.

## Structure

| Fichier | Rôle |
| --- | --- |
| `src/main.py` | Lance l'interface. |
| `src/donnees.py` | Lit le CSV et le JSON, prépare la catégorie sucre et valide les variables. |
| `src/modele.py` | Entraîne, évalue, sauvegarde et recharge la régression. |
| `src/interface.py` | Construit le formulaire, affiche la note, le graphique et l'historique. |
| `src/historique.py` | Lit et écrit les prédictions. Une lambda sert de clé de tri par numéro décroissant. |
| `src/exceptions.py` | Définit les exceptions du projet. |
| `src/explorations.py` | Génère les graphiques d'exploration. |
| `tests/` | Vérifie le modèle, les entrées et l'historique. |

## Documentation officielle

- [pandas — read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [scikit-learn — LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)
- [Python — Tkinter](https://docs.python.org/3/library/tkinter.html)
