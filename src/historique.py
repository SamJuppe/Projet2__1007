"""Gestion de l'historique des prédictions (fichier CSV dans le dossier historique/)."""
import csv
import os

from donnees import DOSSIER_PROJET

CHEMIN_HISTORIQUE = os.path.join(DOSSIER_PROJET, "historique", "historique.csv")


def compter_predictions(chemin: str) -> int:
    """Compte les prédictions déjà enregistrées dans l'historique.

    Reçoit : chemin (str), le chemin du fichier CSV.
    Renvoie : le nombre de lignes de données (int) ; 0 si le fichier n'existe pas encore.
    Échoue : OSError si le fichier existe mais ne peut pas être lu.
    """
    if not os.path.exists(chemin):
        return 0
    with open(chemin, newline="", encoding="utf-8") as fichier:
        return len(list(csv.DictReader(fichier)))


def ajouter_prediction(chemin: str, saisies: dict, note: float) -> dict:
    """Ajoute une prédiction numérotée à la fin du fichier CSV de l'historique.

    Reçoit : chemin (str), le chemin du fichier CSV ;
             saisies (dict), les valeurs validées entrées par l'utilisateur ;
             note (float), la note de qualité prédite par le modèle.
    Renvoie : la ligne ajoutée (dict), avec son numéro, les saisies et la note.
    Échoue : OSError si le fichier ne peut pas être lu ou écrit (ex. dossier protégé).
    """
    numero = compter_predictions(chemin) + 1  # la 1re prédiction a le numéro 1, la suivante 2, etc.
    ligne = {"numero": numero}
    for nom, valeur in saisies.items():  # on recopie chaque valeur entrée par l'utilisateur
        ligne[nom] = valeur
    ligne["note"] = round(note, 2)
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    # Fichier absent OU vide (ex. vidé à la main) : il faut écrire la ligne d'en-tête.
    fichier_vide = not os.path.exists(chemin) or os.path.getsize(chemin) == 0
    with open(chemin, "a", newline="", encoding="utf-8") as fichier:
        ecrivain = csv.DictWriter(fichier, fieldnames=list(ligne.keys()))
        if fichier_vide:
            ecrivain.writeheader()
        ecrivain.writerow(ligne)
    return ligne


def charger_historique(chemin: str) -> list[dict]:
    """Relit l'historique et le trie de la prédiction la plus récente (plus grand numéro) à la plus ancienne.

    Reçoit : chemin (str), le chemin du fichier CSV.
    Renvoie : une liste de dict (une par prédiction) ; une liste vide si le fichier n'existe pas encore.
    Échoue : OSError si le fichier existe mais ne peut pas être lu.
    """
    if not os.path.exists(chemin):
        return []
    with open(chemin, newline="", encoding="utf-8") as fichier:
        lignes = list(csv.DictReader(fichier))
    # Outil du chapitre 7 : une lambda sert de clé de tri (le numéro de chaque ligne, converti en entier).
    return sorted(lignes, key=lambda ligne: int(ligne["numero"]), reverse=True)
