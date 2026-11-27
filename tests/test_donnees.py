"""Tests du chargement et de la validation des données."""
from pathlib import Path

import pandas as pd
import pytest

from donnees import VariableCategorielle, VariableNumerique, aucune_valeur_vide, categoriser_sucre, charger_donnees
from exceptions import FichierIntrouvableError, Pasunnombre, StringVide, depasse_limite, pas_dedans


def test_aucune_valeur_vide() -> None:
    """Vérifie qu'un tableau renseigné est accepté."""
    assert aucune_valeur_vide(pd.DataFrame({"x": [0, 1]}))


@pytest.mark.parametrize("valeur", [None, "", " "])
def test_valeur_vide(valeur: str | None) -> None:
    """Vérifie que les formes courantes de valeurs manquantes sont détectées."""
    assert not aucune_valeur_vide(pd.DataFrame({"x": [valeur]}))


def test_fichier_absent(tmp_path: Path) -> None:
    """Vérifie l'exception levée pour un CSV absent."""
    with pytest.raises(FichierIntrouvableError):
        charger_donnees(str(tmp_path / "absent.csv"))


def test_seuil_sucre() -> None:
    """Vérifie le classement au seuil et immédiatement au-dessus."""
    resultat = categoriser_sucre(pd.DataFrame({"residual sugar": [0, 4, 4.01]}))
    assert resultat["sucre"].tolist() == ["sec", "sec", "sucré"]


@pytest.mark.parametrize("saisie, attendu", [("0", 0.0), ("0.25", 0.25), ("1", 1.0)])
def test_variable_numerique(saisie: str, attendu: float) -> None:
    """Vérifie une valeur usuelle et les deux bornes inclusives."""
    assert VariableNumerique("mesure", 1, 0).valider(saisie) == pytest.approx(attendu)


@pytest.mark.parametrize("saisie, erreur", [(" ", StringVide), ("abc", Pasunnombre), ("1.01", depasse_limite), ("nan", depasse_limite)])
def test_saisie_numerique_invalide(saisie: str, erreur: type[Exception]) -> None:
    """Vérifie le type d'erreur associé à chaque saisie invalide."""
    with pytest.raises(erreur):
        VariableNumerique("mesure", 1, 0).valider(saisie)


def test_variable_categorielle() -> None:
    """Vérifie la normalisation et le rejet d'un choix inconnu."""
    variable = VariableCategorielle("sucre", ["sec", "sucré"])
    assert variable.valider(" SEC ") == "sec"
    with pytest.raises(pas_dedans):
        variable.valider("inconnu")
