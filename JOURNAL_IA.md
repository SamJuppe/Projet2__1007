# Checklist Projet 2 – INF1007

> ⚠️ `interface.py` a été écrasé (il ne contient plus que `print(mt.sqrt(423))`) : récupérer l'ancien code des graphiques dans l'historique Git.

## 0. Mise en place (Git, structure)
- [x] Dépôt GitHub créé, coéquipier invité
- [x] Dossiers `donnees/`, `src/`, `tests/`
- [ ] Vérifier que le dépôt est public
- [ ] Créer le dossier `modeles/` (modèle sauvegardé + JSON)
- [ ] Créer `.gitignore` avec `__pycache__/` et `.vscode/`
- [ ] Retirer les `.pyc` déjà suivis : `git rm -r --cached src/__pycache__`
- [ ] Remplir `requirements.txt` : pandas, numpy, scikit-learn, matplotlib, joblib, pytest, coverage (+ bibliothèque d'interface)
- [ ] Créer `.github/workflows/tests.yml` qui lance pytest à chaque push
- [ ] Dernier commit qui passe la CI (marque verte sur GitHub)
- [ ] Commits réguliers des deux membres avec des messages clairs

## 1. Volet 1 – Jeu de données
- [x] CSV de plus de 500 lignes, au moins 5 colonnes d'entrée
- [x] Licence (DbCL v1.0) dans le README
- [x] Pas de données personnelles
- [ ] Citer la source (lien Kaggle/UCI) dans le README
- [ ] Validation A (domaine) avec l'auxiliaire, notée avec la date
- [ ] Validation B (jeu de données) avec l'auxiliaire, notée avec la date

## 2. Volet 2 – Modèle

### Étape 1 – Explorer et nettoyer
- [x] Charger avec pandas, vérifier les valeurs vides, dtypes, describe()
- [ ] Chercher les valeurs aberrantes et expliquer ce qu'on en fait
- [ ] Expliquer en quelques lignes ce qu'on a vérifié et corrigé
- [ ] Au moins un graphique d'exploration enregistré avec `plt.savefig`

### Étape 2 – Définir le problème
- [x] Cible = quality, type = régression, métrique = RMSE
- [ ] Justifier pourquoi la RMSE (une phrase)
- [ ] Validation C (cible, métrique, modèle) avec l'auxiliaire

### Étape 3 – Séparer
- [x] train_test_split 80/20 avec random_state=42

### Étape 4 – Référence
- [x] Prédire toujours la moyenne → RMSE ≈ 0,81

### Étape 5 – Entraîner et évaluer
- [x] LinearRegression entraînée sur train → RMSE ≈ 0,63
- [ ] Comparer modèle et référence par écrit (≈ 22 % d'erreur en moins)
- [ ] Graphique « prédit contre réel »
- [ ] Commenter honnêtement les limites
- [ ] (Facultatif) Comparer un 2e modèle

### Étape 6 – Sauvegarder
- [ ] Sauvegarder le modèle avec `joblib.dump` dans `modeles/`
- [ ] Fichier JSON de métadonnées : noms des colonnes, intervalles min/max, métrique obtenue
- [ ] L'interface charge le modèle (pas de ré-entraînement)

## 3. Volet 3 – Interface graphique
- [ ] Choisir la technologie (Tkinter, Streamlit, Gradio…)
- [ ] Maquette sur papier de la fenêtre
- [ ] Validation D (technologie + maquette) avec l'auxiliaire
- [ ] Un champ par variable, construit à partir du JSON
- [ ] Validation des saisies : vide / non numérique / hors intervalle → message clair, jamais de traceback
- [ ] Bouton « Prédire » avec un résultat compréhensible par un non-informaticien
- [ ] Graphique Matplotlib dans la fenêtre (titre, axes, légende)
- [ ] Historique : chaque prédiction ajoutée à un CSV/JSON, consultable dans l'interface
- [ ] Fonctionne en local, commandes d'installation et de lancement dans le README

## 4. Exigences de code

### Chapitre 5 – Fichiers
- [ ] Chemins construits avec `os.path.join`
- [ ] Vérifier avec `os.path.exists` avant d'ouvrir un fichier
- [ ] `with open(...)` pour chaque ouverture
- [ ] Écrire le JSON des métadonnées et l'historique

### Chapitre 6 – Fonctions
- [ ] Docstring complète partout (reçoit / renvoie / quand elle échoue)
- [ ] Annotations de type partout
- [ ] Les fonctions renvoient avec `return`, l'affichage est ailleurs
- [ ] Renommer `est_ce_que_il_ny_a__pas_de_strings_vide_True_or_False` (ex. `aucune_valeur_vide`)
- [ ] Corriger la docstring de `donnees.py` (« prix de sortie du marché », « neuf colonnes »)

### Chapitre 7 – Modules
- [x] Fichiers donnees, modele, exceptions, interface, main créés
- [ ] Plus de code au niveau des fichiers (lignes 13-14 et 25 de `donnees.py`)
- [ ] `modele.py` importe `charger_donnees` au lieu de la variable `donnee`
- [ ] Remplir `main.py` (point d'entrée)
- [ ] Un outil du chapitre 7 (décorateur / générateur / lambda), expliqué dans le README

### Chapitre 8 – Exceptions
- [ ] Remplir `exceptions.py` (au moins une exception qui hérite de `Exception`)
- [ ] La lever avec `raise`
- [ ] `try / except` sur des exceptions précises, jamais `except:` seul

### Chapitre 8 – Tests
- [ ] Au moins 8 tests pytest (`test_donnees.py`, `test_modele.py`)
- [ ] Cas usuels, cas limites et cas d'erreur (`pytest.raises`)
- [ ] `pytest.approx` pour les nombres à virgule
- [ ] Test : notre `rmse` NumPy = celle de scikit-learn
- [ ] Mesurer la couverture avec `coverage`, résultat dans le README

### Chapitres 9 à 11 – POO
- [ ] Au moins 3 classes (constructeur, méthodes, attributs `_protégés` / `__privés`)
- [ ] Héritage : classe parente (idéalement abstraite) + 2 classes enfants qui redéfinissent la même méthode
- [ ] Composition : une classe qui contient d'autres objets
- [ ] Au moins une méthode spéciale (`__str__`, `__repr__`, `__eq__`…)

### Chapitre 12 – NumPy
- [x] Calcul vectorisé : fonction `rmse`

### Chapitre 13 – Matplotlib et documentation
- [ ] Graphique d'exploration (savefig) + graphique dans l'interface
- [ ] Citer 3 pages de documentation officielle dans le README (pandas, scikit-learn, interface)

## 5. Livrables

### README.md
- [ ] Description du projet
- [ ] Source du jeu de données (licence déjà là)
- [ ] Commandes d'installation et de lancement
- [ ] Structure du code (quel fichier fait quoi)
- [ ] Résultat du modèle (RMSE modèle et référence)
- [ ] Couverture de tests
- [ ] 3 références de documentation
- [ ] Outil du chapitre 7 utilisé

### DECISIONS.md
- [x] Commencé (étapes 1 à 3)
- [ ] Mettre en tableau : Choix · Options envisagées · Choix retenu et justification · Validé par l'auxiliaire (date)
- [ ] Une ligne par choix : domaine, jeu de données, cible et métrique, modèle, technologie d'interface…

### JOURNAL_IA.md
- [ ] Tableau : Outil · Demande · Réponse reçue · Vérification faite · Décision
- [ ] Au moins 5 entrées
- [ ] Au moins une vérification qui a changé une décision (ex. : pathlib → os)

### Remise
- [ ] Lien du dépôt GitHub sur Moodle
- [ ] Test final : cloner dans un dossier neuf, installer, lancer l'appli et les tests

## 6. Présentation (10 min)
- [ ] Répartir la parole à parts égales
- [ ] Démo en direct : cas normal, saisie invalide, graphique
- [ ] Schéma simple des classes et des modules
- [ ] Plan B (captures d'écran ou vidéo)
- [ ] Maximum 4 diapositives (facultatif)
- [ ] Répéter en chronométrant (5 min)
- [ ] Chacun peut expliquer chaque ligne du code