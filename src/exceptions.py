#Premiere exceptions : « fichier de données introuvable »
class FichierIntrouvableError(Exception):
    """Leve quand le fichier de données demande n'existe pas."""
class TaillesDifferentesError(ValueError):
    """Leve quand les nombres qu'on etudie ne vont pas etre coherent"""
class StringVide(ValueError):
    """Leve une erreur si il y a un string vide"""
class Pasunnombre(ValueError):
    """Leve une erreur si il y a un string qui ne peut etre converti en float"""
class depasse_limite(ValueError):
    """Leve une erreur si il y a un nombre est au dessus des limites donnes"""
class pas_dedans(ValueError):
    """Leve une erreur si il y a un string qui n'est pas dans la liste donner"""