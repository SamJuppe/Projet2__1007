"""Tests de la régression et de l'historique."""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

from exceptions import TaillesDifferentesError
from historique import ajouter_prediction, charger_historique
from modele import charger_modele, construire_metadonnees, enregistrer_jo, interpreter_note, predire, rmse, separer_donnees


def test_rmse_sklearn() -> None:
    """Compare la RMSE NumPy à la fonction de référence."""
    reel = pd.Series([3.0, 4.0, 7.0])
    predit = np.array([3.0, 5.0, 5.0])
    assert rmse(reel, predit) == pytest.approx(root_mean_squared_error(reel, predit))


def test_separation() -> None:
    """Vérifie la proportion du test et l'absence de chevauchement."""
    x = pd.DataFrame({"x": range(10)})
    x_train, x_test, y_train, y_test = separer_donnees(x, x["x"])
    assert (len(x_train), len(x_test)) == (8, 2)
    assert set(x_train.index).isdisjoint(x_test.index)
    assert list(y_train.index) == list(x_train.index)
    assert list(y_test.index) == list(x_test.index)


def test_separation_tailles_differentes() -> None:
    """Vérifie le rejet de tableaux de tailles incompatibles."""
    with pytest.raises(TaillesDifferentesError):
        separer_donnees(pd.DataFrame({"x": [1, 2]}), pd.Series([1]))


def test_modele_sauvegarde(tmp_path: Path) -> None:
    """Vérifie la prédiction après sauvegarde et rechargement du modèle."""
    x = pd.DataFrame({"mesure": [0.0, 1.0, 2.0]})
    modele = LinearRegression().fit(x, [4.0, 5.0, 6.0])
    chemin = str(tmp_path / "modèle.joblib")
    enregistrer_jo(modele, chemin)
    assert predire(charger_modele(chemin), {"mesure": 1.5}) == pytest.approx(5.5)


def test_metadonnees() -> None:
    """Vérifie les bornes, les choix et la métrique écrits dans les métadonnées."""
    meta = construire_metadonnees(pd.DataFrame({"x": [1, 2], "sucre": ["sec", "sucré"]}), 0.5)
    assert meta["rmse"] == pytest.approx(0.5)
    assert meta["colonnes"]["x"] == {"type": "numerique", "min": 1, "max": 2}
    assert meta["colonnes"]["sucre"]["choix"] == ["sec", "sucré"]


def test_interpretation() -> None:
    """Vérifie l'appréciation à la limite de deux catégories."""
    assert interpreter_note(5.5) == "Bon vin"


def test_historique(tmp_path: Path) -> None:
    """Vérifie la création du CSV et l'ordre de lecture des prédictions."""
    chemin = str(tmp_path / "historique.csv")
    assert charger_historique(chemin) == []
    ajouter_prediction(chemin, {"mesure": 1}, 5.5)
    ajouter_prediction(chemin, {"mesure": 2}, 6.5)
    assert [int(ligne["numero"]) for ligne in charger_historique(chemin)] == [2, 1]
