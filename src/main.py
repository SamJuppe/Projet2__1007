"""Point d'entrée : lance l'application de prédiction de la qualité du vin."""
import tkinter as tk
from tkinter import messagebox

from exceptions import FichierIntrouvableError
from interface import Application


def rendre_net_sur_windows() -> None:
    """Évite le texte flou sur les écrans haute résolution de Windows (sans effet ailleurs)."""
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass


def lancer() -> None:
    """Crée la fenêtre et démarre l'application ; affiche un message clair si un fichier manque."""
    rendre_net_sur_windows()
    fenetre = tk.Tk()
    try:
        Application(fenetre)
    except FichierIntrouvableError as erreur:
        fenetre.withdraw()
        messagebox.showerror("Fichier manquant", str(erreur))
        fenetre.destroy()
        return
    fenetre.protocol("WM_DELETE_WINDOW", lambda: (fenetre.quit(), fenetre.destroy()))
    fenetre.mainloop()


if __name__ == "__main__":
    lancer()
