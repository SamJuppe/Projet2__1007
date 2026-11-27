# Décisions — Projet 2 INF1007

| Choix | Options envisagées | Choix retenu et justification | Validé par l'auxiliaire (date) |

| A · Domaine | Qualité du vin, autres domaines tabulaires | Vin rouge. Le formulaire relie des mesures concrètes à une note de qualité. | Date à renseigner |
| B · Jeu de données | Autres jeux sur le vin, Wine Quality | Wine Quality rouge, 1 599 observations, mesures complètes et cible explicite. Le sucre résiduel est recodé en catégorie. | Date à renseigner |
| C · Cible et métrique | Classification ou régression, MAE ou RMSE | Régression de `quality`. La RMSE reste en points de qualité et pénalise davantage les grands écarts. | Date à renseigner |
| C · Modèle | Moyenne constante, régression linéaire | Régression linéaire pour sa simplicité. La moyenne des notes d'entraînement sert de référence. | Date à renseigner |
| Séparation et valeurs extrêmes | Divers ratios, suppression ou conservation des extrêmes | 80/20 avec graine 42. Les valeurs repérées par l'écart interquartile restent dans le jeu en l'absence d'indice d'erreur. | — |
| D · Interface et maquette | Tkinter, Streamlit | Tkinter pour une fenêtre locale. Deux onglets, formulaire et résultat sur le premier, historique sur le second. | Date à renseigner |
| Historique | CSV ou JSON, dans le formulaire ou dans un onglet | CSV, consultable dans un onglet dédié, avec les prédictions les plus récentes en haut. | — |

## Maquette à présenter

```text
Qualité du vin rouge
[ Prédiction ] [ Historique ]
┌ Caractéristiques ───────────┬ Résultat ───────────────┐
│ Acidité volatile | Ac. citr. │ Note / 10              │
│ SO₂ total        | Densité   │ Appréciation           │
│ Sulfates         | Alcool    │ RMSE sur le jeu de test │
│ Sucre [sec / sucré]           │ Distribution des notes │
│ Messages sous les champs     │ et repère prédiction   │
│ [Prédire] [Exemple] [Effacer] │                        │
└──────────────────────────────┴────────────────────────┘
Historique : tableau des notes et des caractéristiques saisies
```
