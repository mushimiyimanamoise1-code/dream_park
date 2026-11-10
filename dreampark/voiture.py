"""La classe Voiture.

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .placement import Placement


class Voiture:
    """Véhicule d'un client, identifié par son immatriculation."""

    def __init__(self, immatriculation: str, hauteur: float, longueur: float):
        """Crée une voiture, hors du parking au départ.

        :param immatriculation: plaque d'immatriculation (non vide)
        :param hauteur: hauteur en mètres (> 0)
        :param longueur: longueur en mètres (> 0)
        :raises ValueError: immatriculation vide, hauteur ou longueur <= 0.
        """
        if not immatriculation.strip():
            raise ValueError("L'immatriculation ne peut pas être vide.")
        if hauteur <= 0 or longueur <= 0:
            raise ValueError("La hauteur et la longueur doivent être > 0.")

        self.immatriculation = immatriculation
        self.hauteur = hauteur
        self.longueur = longueur
        self.placements: list = []

    @property
    def estDansParking(self) -> bool:
        """Vrai si un des placements de la voiture est en cours."""
        raise NotImplementedError

    def ajouter_placement(self, p: "Placement") -> None:
        """Ajoute le placement p à l'historique de la voiture.

        La voiture est alors dans le parking tant que p est en cours.
        """
        raise NotImplementedError