"""Gestion de l'historique des prédictions (fichier CSV dans le dossier historique/)."""
import csv
import os

from donnees import DOSSIER_PROJET

CHEMIN_HISTORIQUE = os.path.join(DOSSIER_PROJET, "historique", "historique.csv")


def ajouter_prediction(chemin: str, saisies: dict, note: float) -> dict:
    """Ajoute une prédiction à la fin du fichier CSV de l'historique.

    Reçoit : chemin (str), le chemin du fichier CSV ;
             saisies (dict), les valeurs validées entrées par l'utilisateur ;
             note (float), la note de qualité prédite par le modèle.
    Renvoie : la ligne ajoutée (dict), avec les saisies et la note.
    Échoue : OSError si le fichier ne peut pas être écrit (ex. dossier protégé).
    """
    ligne = {**saisies, "note": round(note, 2)}
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    fichier_existe = os.path.exists(chemin)
    with open(chemin, "a", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=list(ligne.keys()))
        if not fichier_existe:
            ecrivain.writeheader()
        ecrivain.writerow(ligne)
    return ligne


def charger_historique(chemin: str) -> list[dict]:
    """Relit l'historique et le trie de la meilleure note à la moins bonne.

    Reçoit : chemin (str), le chemin du fichier CSV.
    Renvoie : une liste de dict (une par prédiction) ; une liste vide si le fichier n'existe pas encore.
    Échoue : OSError si le fichier existe mais ne peut pas être lu.
    """
    if not os.path.exists(chemin):
        return []
    with open(chemin, newline="", encoding="utf-8") as fichier:
        lignes = list(csv.DictReader(fichier))
    # Outil du chapitre 7 : une lambda sert de clé de tri (la note de chaque ligne, convertie en nombre).
    lignes.sort(key=lambda ligne: float(ligne["note"]), reverse=True)
    return lignes
