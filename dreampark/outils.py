"""Fonctions utilitaires partagées, pour permettre d'avoir l'heure de France

@author: MUSHIMIYIMANA MOISE
"""
from datetime import date, datetime
from zoneinfo import ZoneInfo

FUSEAU_FRANCE = ZoneInfo("Europe/Paris")


def aujourd_hui() -> date:
    """Date du jour en France (calculée à chaque appel)."""
    return datetime.now(FUSEAU_FRANCE).date()

def maintenant() -> datetime:
    """Date et heure actuelles en France."""
    return datetime.now(FUSEAU_FRANCE).replace(tzinfo=None)