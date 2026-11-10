"""La classe Place.

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .voiture import Voiture
    from .placement import Placement


class Place:
    """Emplacement du parking, identifié par un numéro et un niveau."""

    LONGUEUR_MIN = 4.0
    LONGUEUR_MAX = 6.0
    HAUTEUR_MIN = 2.0
    HAUTEUR_MAX = 4.0

    def __init__(self, numero: int, niveau: str, longueur: float, hauteur: float):
        """Crée une place libre.

        :param numero: numéro (>= 1)
        :param niveau: lettre majuscule du niveau (ex. 'A')
        :param longueur: longueur de la place (LONGUEUR_MIN <= l <= LONGUEUR_MAX)
        :param hauteur: hauteur de la place (HAUTEUR_MIN <= h <= HAUTEUR_MAX)
        :raises ValueError: si une valeur est invalide.
        """
        if numero < 1:
            raise ValueError("Le numéro de place doit être >= 1.")
        if len(niveau) != 1 or not niveau.isalpha() or not niveau.isupper():
            raise ValueError("Le niveau doit être une lettre majuscule (ex. 'A').")
        if not (self.LONGUEUR_MIN <= longueur <= self.LONGUEUR_MAX):
            raise ValueError(f"Longueur hors limites [{self.LONGUEUR_MIN}, {self.LONGUEUR_MAX}].")
        if not (self.HAUTEUR_MIN <= hauteur <= self.HAUTEUR_MAX):
            raise ValueError(f"Hauteur hors limites [{self.HAUTEUR_MIN}, {self.HAUTEUR_MAX}].")

        self.numero = numero
        self.niveau = niveau
        self.longueur = longueur
        self.hauteur = hauteur
        
        self.est_libre = True

    @property
    def id_place(self) -> str:
        """Identifiant unique = niveau + numéro (ex. 'A1', 'C15')."""
        raise NotImplementedError

    def convient_a(self, voiture: "Voiture") -> bool:
        """Vrai si la place est libre et si longueur/hauteur de la voiture <= celles de la place."""
        raise NotImplementedError

    def ajouter_placement(self, p: "Placement") -> None:
        """Enregistre un placement sur cette place et la marque occupée."""
        raise NotImplementedError

    def liberer(self) -> None:
        """Marque la place libre (appelée par le téléporteur à la sortie)."""
        raise NotImplementedError
