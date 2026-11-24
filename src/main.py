"""Point d'entrée : lance l'application de prédiction de la qualité du vin."""
import tkinter as tk
from tkinter import messagebox

from exceptions import FichierIntrouvableError
from interface import Application



def lancer() -> None:
    """Crée la fenêtre et démarre l'application ; affiche un message clair si un fichier manque."""
    fenetre = tk.Tk()
    try:
        Application(fenetre)
    except FichierIntrouvableError as erreur:
        fenetre.destroy()
        messagebox.showerror("Fichier manquant", str(erreur))
        
        return
    fenetre.protocol("WM_DELETE_WINDOW", lambda: (fenetre.quit(), fenetre.destroy()))
    fenetre.mainloop()


if __name__ == "__main__":
    lancer()
