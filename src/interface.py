"""Interface graphique (Tkinter) : saisie des caractéristiques, prédiction, graphique et historique.

L'interface ne contient pas la logique : elle appelle les fonctions de donnees.py, modele.py et historique.py.
"""
import os
import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from donnees import (DOSSIER_DONNEES, DOSSIER_PROJET, Variable, VariableCategorielle,
                     charger_donnees, charger_metadonnees, creer_variables)
from exceptions import Pasunnombre, StringVide, depasse_limite, pas_dedans
from historique import CHEMIN_HISTORIQUE, ajouter_prediction, charger_historique
from modele import charger_modele, interpreter_note, predire

# ---------- Apparence ----------
BORDEAUX = "#6D1A36"
BORDEAUX_CLAIR = "#8E2A4D"
ROSE_PALE = "#F4E4EA"
FOND = "#F6F1EE"
CARTE = "#FFFFFF"
TEXTE = "#2B2024"
GRIS = "#7A6E72"
BORDURE = "#E3D9DC"
ROUGE_ERREUR = "#C0392B"
AVERTISSEMENT_FOND = "#FFF4DE"
AVERTISSEMENT_TEXTE = "#7A5300"
POLICE = "Segoe UI"
LIBELLES = {
    "volatile acidity": ("Acidité volatile", "g/L"),
    "citric acid": ("Acide citrique", "g/L"),
    "total sulfur dioxide": ("Dioxyde de soufre total", "mg/L"),
    "density": ("Densité", "g/cm³"),
    "sulphates": ("Sulfates", "g/L"),
    "alcohol": ("Alcool", "% vol."),
    "sucre": ("Teneur en sucre", ""),
}

ERREURS_SAISIE = (StringVide, Pasunnombre, depasse_limite, pas_dedans)


def virgule(nombre: float, decimales: int) -> str:
    """Formate un nombre à la française (virgule décimale), ex. virgule(6.25, 1) -> '6,2'."""
    return f"{nombre:.{decimales}f}".replace(".", ",")


class ChampSaisie:
    """Un champ du formulaire : étiquette, zone de saisie et message d'erreur pour une Variable."""

    def __init__(self, parent: tk.Widget, variable: Variable, infos: dict, ligne: int, colonne: int) -> None:
        self._variable = variable
        nom, unite = LIBELLES.get(variable.get_nom(), (variable.get_nom(), ""))

        cadre = tk.Frame(parent, bg=CARTE)
        cadre.grid(row=ligne, column=colonne, sticky="new", padx=8, pady=(0, 4))

        tk.Label(cadre, text=nom, font=(POLICE, 10, "bold"), fg=TEXTE, bg=CARTE, anchor="w").pack(fill="x")
        tk.Label(cadre, text=self._indice(infos, unite), font=(POLICE, 8), fg=GRIS, bg=CARTE, anchor="w").pack(fill="x")

        self._est_liste = isinstance(variable, VariableCategorielle)
        if self._est_liste:
            self._champ = ttk.Combobox(cadre, values=variable.get_choix(), state="readonly",
                                       font=(POLICE, 10), style="Vin.TCombobox")
            self._champ.pack(fill="x", ipady=3, pady=(3, 0))
        else:
            self._champ = tk.Entry(cadre, font=(POLICE, 10), relief="flat", bg="#FBF8F9", fg=TEXTE,
                                   highlightthickness=1, highlightbackground=BORDURE,
                                   highlightcolor=BORDEAUX_CLAIR, insertbackground=TEXTE)
            self._champ.pack(fill="x", ipady=5, pady=(3, 0))

        self._erreur = tk.Label(cadre, text="", font=(POLICE, 8), fg=ROUGE_ERREUR, bg=CARTE, anchor="w",
                                justify="left", wraplength=260)
        self._erreur.pack(fill="x")

    @staticmethod #pas sself

    def _indice(infos: dict, unite: str) -> str:
        """Construit le petit texte d'aide affiché à droite du nom (intervalle permis ou choix)."""
        if infos["type"] == "numerique":
            return f"entre {infos['min']:.4g} et {infos['max']:.4g} {unite}".strip()
        return "choisir dans la liste"

    def get_nom(self) -> str:
        """Renvoie le nom de la colonne associée à ce champ."""
        return self._variable.get_nom()

    def lire(self) -> str | float:
        """Valide la saisie et renvoie la valeur. Lève une exception de saisie si elle est invalide."""
        saisie = self._champ.get().replace(",", ".")  # accepte 12,5 comme 12.5
        return self._variable.valider(saisie)

    def montrer_erreur(self, message: str) -> None:
        """Affiche le message d'erreur sous le champ et colore sa bordure en rouge."""
        self._erreur.config(text=f"⚠ {message}")
        if not self._est_liste:
            self._champ.config(highlightbackground=ROUGE_ERREUR, highlightcolor=ROUGE_ERREUR)

    def effacer_erreur(self) -> None:
        """Retire le message d'erreur et remet la bordure normale."""
        self._erreur.config(text="")
        if not self._est_liste:
            self._champ.config(highlightbackground=BORDURE, highlightcolor=BORDEAUX_CLAIR)

    def remplir(self, valeur: str) -> None:
        """Remplace le contenu du champ par la valeur donnée."""
        if self._est_liste:
            self._champ.set(valeur)
        else:
            self._champ.delete(0, tk.END)
            self._champ.insert(0, valeur)


class Application:
    """Fenêtre principale : contient le modèle, les variables, les champs et l'historique (composition)."""

    def __init__(self, fenetre: tk.Tk) -> None:
        self._fenetre = fenetre
        dossier_modeles = os.path.join(DOSSIER_PROJET, "modeles")
        self._modele = charger_modele(os.path.join(dossier_modeles, "modele.joblib"))
        self._metadonnees = charger_metadonnees(os.path.join(dossier_modeles, "metadonnees.json"))
        self._variables = creer_variables(self._metadonnees)
        self._rmse = float(self._metadonnees["rmse"])
        self._donnees = charger_donnees(os.path.join(DOSSIER_DONNEES, "winequalityred.csv"))
        self._champs: list[ChampSaisie] = []

        self._configurer_fenetre()
        self._configurer_styles()
        self._creer_onglets()
        self._dessiner_graphique(None)
        self._rafraichir_historique()

    def _configurer_fenetre(self) -> None:
        """Titre, taille et couleur de fond de la fenêtre."""
        self._fenetre.title("Qualité du vin rouge – INF1007")
        # Windows agrandit les polices (ex. 150 %) : on agrandit la fenêtre dans la même proportion.
        facteur = self._fenetre.winfo_fpixels("1i") / 96
        largeur = min(int(1240 * facteur), self._fenetre.winfo_screenwidth() - 40)
        hauteur = min(int(760 * facteur), self._fenetre.winfo_screenheight() - 90)
        x = (self._fenetre.winfo_screenwidth() - largeur) // 2
        self._fenetre.geometry(f"{largeur}x{hauteur}+{x}+10")
        self._fenetre.minsize(int(1000 * facteur * 0.8), int(600 * facteur * 0.8))
        self._fenetre.configure(bg=FOND)
        self._fenetre.bind("<Return>", lambda evenement: self._predire())

    def _configurer_styles(self) -> None:
        """Styles ttk : onglets, liste déroulante et tableau de l'historique."""
        style = ttk.Style(self._fenetre)
        style.theme_use("clam")
        style.configure("TNotebook", background=FOND, borderwidth=0)
        style.configure("TNotebook.Tab", font=(POLICE, 10, "bold"), padding=(18, 8),
                        background=BORDURE, foreground=GRIS, borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", CARTE)], foreground=[("selected", BORDEAUX)])
        style.configure("Vin.TCombobox", fieldbackground="#FBF8F9", background=CARTE,
                        bordercolor=BORDURE, arrowcolor=BORDEAUX, padding=4)
        style.map("Vin.TCombobox", fieldbackground=[("readonly", "#FBF8F9")],
                  selectbackground=[("readonly", "#FBF8F9")], selectforeground=[("readonly", TEXTE)])
        style.configure("Treeview", font=(POLICE, 9), rowheight=28, background=CARTE,
                        fieldbackground=CARTE, bordercolor=BORDURE, foreground=TEXTE)
        style.configure("Treeview.Heading", font=(POLICE, 9, "bold"), background=ROSE_PALE,
                        foreground=BORDEAUX, relief="flat", padding=6)
        style.map("Treeview", background=[("selected", BORDEAUX_CLAIR)], foreground=[("selected", "white")])

    def _creer_onglets(self) -> None:
        """Deux onglets : la prédiction et l'historique."""
        onglets = ttk.Notebook(self._fenetre)
        onglets.pack(fill="both", expand=True, padx=20, pady=16)

        onglet_prediction = tk.Frame(onglets, bg=FOND)
        onglet_historique = tk.Frame(onglets, bg=FOND)
        onglets.add(onglet_prediction, text="  Prédiction  ")
        onglets.add(onglet_historique, text="  Historique  ")

        self._creer_formulaire(onglet_prediction)
        self._creer_resultat(onglet_prediction)
        self._creer_historique(onglet_historique)

    @staticmethod
    def _carte(parent: tk.Widget, titre: str) -> tk.Frame:
        """Crée un cadre blanc avec un titre (style « carte ») et renvoie sa zone de contenu."""
        bordure = tk.Frame(parent, bg=BORDURE, padx=1, pady=1)
        contenu = tk.Frame(bordure, bg=CARTE, padx=20, pady=16)
        contenu.pack(fill="both", expand=True)
        tk.Label(contenu, text=titre, font=(POLICE, 12, "bold"), fg=BORDEAUX, bg=CARTE).pack(anchor="w", pady=(0, 10))
        return contenu

    def _creer_formulaire(self, parent: tk.Frame) -> None:
        """Carte de gauche : un champ par variable, construit à partir des métadonnées."""
        carte = self._carte(parent, "Caractéristiques du vin")
        carte.master.pack(side="left", fill="y", padx=(12, 8), pady=12)

        grille = tk.Frame(carte, bg=CARTE)
        grille.pack(fill="x")
        grille.columnconfigure((0, 1), weight=1, uniform="champs", minsize=260)
        for numero, variable in enumerate(self._variables):
            infos = self._metadonnees["colonnes"][variable.get_nom()]
            self._champs.append(ChampSaisie(grille, variable, infos, numero // 2, numero % 2))

        boutons = tk.Frame(carte, bg=CARTE, padx=8)
        boutons.pack(fill="x", pady=(10, 0))
        self._bouton(boutons, "Predire", self._predire, principal=True).pack(fill="x", ipady=4)
        secondaires = tk.Frame(boutons, bg=CARTE)
        secondaires.pack(fill="x", pady=(8, 0))
        self._bouton(secondaires, "Remplir un exemple", self._remplir_exemple).pack(side="left", expand=True, fill="x", padx=(0, 4))
        self._bouton(secondaires, "Effacer", self._effacer).pack(side="left", expand=True, fill="x", padx=(4, 0))

    @staticmethod
    def _bouton(parent: tk.Widget, texte: str, commande, principal: bool = False) -> tk.Button:
        """Crée un bouton plat aux couleurs de l'application."""
        if principal:
            couleurs = {"bg": BORDEAUX, "fg": "white", "activebackground": BORDEAUX_CLAIR, "activeforeground": "white"}
            police = (POLICE, 11, "bold")
        else:
            couleurs = {"bg": ROSE_PALE, "fg": BORDEAUX, "activebackground": BORDURE, "activeforeground": BORDEAUX}
            police = (POLICE, 9, "bold")
        return tk.Button(parent, text=texte, command=commande, font=police, relief="flat",
                         bd=0, cursor="hand2", pady=6, **couleurs)

    def _creer_resultat(self, parent: tk.Frame) -> None:
        """Carte de droite : la note prédite, son appréciation et le graphique."""
        carte = self._carte(parent, "Résultat")
        carte.master.pack(side="left", fill="both", expand=True, padx=(8, 12), pady=12)

        ligne_note = tk.Frame(carte, bg=CARTE)
        ligne_note.pack(anchor="w")
        self._label_note = tk.Label(ligne_note, text="–", font=(POLICE, 38, "bold"), fg=BORDEAUX, bg=CARTE)
        self._label_note.pack(side="left")
        tk.Label(ligne_note, text=" / 10", font=(POLICE, 16), fg=GRIS, bg=CARTE).pack(side="left", anchor="s", pady=(0, 10))

        self._label_appreciation = tk.Label(carte, text="Remplissez le formulaire puis cliquez sur « Prédire ».",
                                            font=(POLICE, 12, "bold"), fg=TEXTE, bg=CARTE, anchor="w")
        self._label_appreciation.pack(fill="x")
        self._label_detail = tk.Label(carte, text="", font=(POLICE, 9), fg=GRIS, bg=CARTE, anchor="w", justify="left")
        self._label_detail.pack(fill="x", pady=(2, 8))

        self._figure = Figure(figsize=(5, 3), dpi=100, facecolor=CARTE)
        self._axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvasTkAgg(self._figure, master=carte)
        self._canvas.get_tk_widget().pack(fill="both", expand=True)

    def _creer_historique(self, parent: tk.Frame) -> None:
        """Onglet historique : tableau de toutes les prédictions enregistrées."""
        carte = self._carte(parent, "Historique des prédictions")
        carte.master.pack(fill="both", expand=True, padx=12, pady=12)

        self._label_compte = tk.Label(carte, text="", font=(POLICE, 9), fg=GRIS, bg=CARTE, anchor="w")
        self._label_compte.pack(fill="x", pady=(0, 8))

        self._colonnes_historique = ["numero", "note", "appreciation"] + [v.get_nom() for v in self._variables]
        cadre_tableau = tk.Frame(carte, bg=CARTE)
        cadre_tableau.pack(fill="both", expand=True)
        self._tableau = ttk.Treeview(cadre_tableau, columns=self._colonnes_historique, show="headings")
        titres = {"numero": "N°", "note": "Note", "appreciation": "Appréciation",
                  "volatile acidity": "Acidité vol.", "citric acid": "Ac. citrique",
                  "total sulfur dioxide": "SO₂ total", "density": "Densité",
                  "sulphates": "Sulfates", "alcohol": "Alcool", "sucre": "Sucre"}
        for colonne in self._colonnes_historique:
            titre = titres.get(colonne, colonne)
            largeur = {"numero": 50, "note": 60, "appreciation": 130}.get(colonne, 95)
            self._tableau.heading(colonne, text=titre)
            self._tableau.column(colonne, width=largeur, minwidth=60, anchor="center")
        self._tableau.tag_configure("pair", background="#FBF6F8")
        defilement = ttk.Scrollbar(cadre_tableau, orient="vertical", command=self._tableau.yview)
        self._tableau.configure(yscrollcommand=defilement.set)
        self._tableau.pack(side="left", fill="both", expand=True)
        defilement.pack(side="right", fill="y")

    # ---------- Actions ----------
    def _predire(self) -> None:
        """Valide toutes les saisies ; si elles sont correctes, prédit, affiche et enregistre."""
        saisies = {}
        for champ in self._champs:
            champ.effacer_erreur()
            try:
                saisies[champ.get_nom()] = champ.lire()
            except ERREURS_SAISIE as erreur:
                champ.montrer_erreur(str(erreur))

        if len(saisies) != len(self._champs):
            self._label_note.config(text="–")
            self._label_appreciation.config(text="Certaines saisies sont invalides.", fg=ROUGE_ERREUR)
            self._label_detail.config(text="Corrigez les champs marqués en rouge, puis cliquez de nouveau sur « Prédire ».")
            return

        note = min(10.0, max(0.0, predire(self._modele, saisies)))
        self._label_note.config(text=virgule(note, 1))
        self._label_appreciation.config(text=interpreter_note(note), fg=TEXTE)
        bas, haut = max(0.0, note - self._rmse), min(10.0, note + self._rmse)
        self._label_detail.config(
            text=(f"La vraie note se situe probablement entre {virgule(bas, 1)} et {virgule(haut, 1)}\n"
                  f"(erreur moyenne du modèle : ± {virgule(self._rmse, 2)})."))
        self._dessiner_graphique(note)

        try:
            ajouter_prediction(CHEMIN_HISTORIQUE, saisies, note)
        except OSError as erreur:
            messagebox.showwarning("Historique", f"La prédiction n'a pas pu être enregistrée :\n{erreur}")
        self._rafraichir_historique()

    def _remplir_exemple(self) -> None:
        """Remplit le formulaire avec un vin « typique » (valeurs médianes du jeu de données)."""
        medianes = self._donnees.median(numeric_only=True)
        for champ in self._champs:
            champ.effacer_erreur()
            if champ.get_nom() in medianes:
                champ.remplir(f"{medianes[champ.get_nom()]:.4g}")
            else:
                champ.remplir("sec")

    def _effacer(self) -> None:
        """Vide tous les champs et remet le résultat à zéro."""
        for champ in self._champs:
            champ.remplir("")
            champ.effacer_erreur()
        self._label_note.config(text="–")
        self._label_appreciation.config(text="Remplissez le formulaire puis cliquez sur « Prédire ».", fg=TEXTE)
        self._label_detail.config(text="")
        self._dessiner_graphique(None)

    def _dessiner_graphique(self, note: float | None) -> None:
        """Dessine la répartition des notes du jeu de données et, si fournie, la note prédite."""
        compte = self._donnees["quality"].value_counts().sort_index()
        axes = self._axes
        axes.clear()
        axes.bar(compte.index, compte.values, width=0.7, color="#D9B8C4", edgecolor="#B98A9C",
                 label="Vins du jeu de données")
        if note is not None:
            axes.axvspan(note - self._rmse, note + self._rmse, color=BORDEAUX, alpha=0.10,
                         label=f"Marge d'erreur (± {virgule(self._rmse, 2)})")
            axes.axvline(note, color=BORDEAUX, linewidth=2.5, label=f"Votre vin : {virgule(note, 1)}")
        axes.set_title(f"Votre vin parmi les {len(self._donnees)} vins du jeu de données",
                       fontsize=11, color=TEXTE, fontweight="bold")
        axes.set_xlabel("Note de qualité (sur 10)", color=GRIS)
        axes.set_ylabel("Nombre de vins", color=GRIS)
        axes.set_xlim(0, 10)
        axes.set_xticks(range(0, 11))
        axes.spines[["top", "right"]].set_visible(False)
        axes.spines[["left", "bottom"]].set_color(BORDURE)
        axes.tick_params(colors=GRIS)
        axes.grid(axis="y", color="#F0E8EB")
        axes.set_axisbelow(True)
        axes.legend(frameon=False, fontsize=9, loc="upper left")
        self._canvas.draw()

    def _rafraichir_historique(self) -> None:
        """Recharge l'historique depuis le fichier CSV et l'affiche (plus récent en premier)."""
        try:
            lignes = charger_historique(CHEMIN_HISTORIQUE)
        except OSError as erreur:
            messagebox.showwarning("Historique", f"L'historique n'a pas pu être lu :\n{erreur}")
            return
        self._tableau.delete(*self._tableau.get_children())
        for numero, ligne in enumerate(lignes):
            valeurs = []
            for colonne in self._colonnes_historique:
                if colonne == "appreciation":
                    valeurs.append(interpreter_note(float(ligne["note"])))
                else:
                    valeurs.append(ligne.get(colonne, ""))
            self._tableau.insert("", tk.END, values=valeurs, tags=("pair",) if numero % 2 else ())
        pluriel = "s" if len(lignes) > 1 else ""
        self._label_compte.config(text=f"{len(lignes)} prédiction{pluriel} enregistrée{pluriel} · la plus récente en haut")
