#Premiere exceptions : « fichier de données introuvable »
class FichierIntrouvableError(Exception):
    """Leve quand le fichier de données demande n'existe pas."""
class TaillesDifferentesError(ValueError):
    """Leve quand les nombres qu'on etudie ne vont pas etre coherent"""