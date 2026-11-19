import os
import tkinter as tk
from tkinter import ttk

from donnees import DOSSIER_PROJET, charger_metadonnees, creer_variables, VariableCategorielle
from modele import charger_modele


class Application:
    """Fenêtre principale : contient le modèle, les variables et les champs de saisie."""

    def __init__(self, fenetre: tk.Tk) -> None:
        self._fenetre = fenetre
        self._fenetre.title("Prédiction de la qualité d'un vin rouge")

        dossier_modeles = os.path.join(DOSSIER_PROJET, "modeles")
        self._modele = charger_modele(os.path.join(dossier_modeles, "modele.joblib"))
        metadonnees = charger_metadonnees(os.path.join(dossier_modeles, "metadonnees.json"))
        self._variables = creer_variables(metadonnees)
        self._champs = {}

        self._creer_champs()

    def _creer_champs(self) -> None:
        """Crée une étiquette et un champ de saisie pour chaque variable."""
        for ligne, variable in enumerate(self._variables):
            tk.Label(self._fenetre, text=str(variable)).grid(row=ligne, column=0, sticky="w", padx=8, pady=4)
            if isinstance(variable, VariableCategorielle):
                champ = ttk.Combobox(self._fenetre, values=variable.get_choix(), state="readonly")
            else:
                champ = tk.Entry(self._fenetre)
            champ.grid(row=ligne, column=1, padx=8, pady=4)
            self._champs[variable.get_nom()] = champ