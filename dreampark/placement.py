"""La classe Placement

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from datetime import date
from typing import Optional, TYPE_CHECKING

from .outils import maintenant

if TYPE_CHECKING:
    from .voiture import Voiture
    from .place import Place


class Placement:
    """Occupation d'une place par une voiture sur une période."""

    def __init__(self, voiture: "Voiture", place: "Place", date_debut: Optional[date] = None):
        """Crée un placement en cours (date_fin = None).

        :param voiture: la voiture garée
        :param place: la place occupée
        :param date_debut: début du placement (aujourd'hui en France par défaut)
        :raises ValueError: si voiture ou place est None.
        """
        if voiture is None or place is None:
            raise ValueError("Un placement nécessite une voiture et une place.")
        if date_debut is None:
            date_debut = maintenant()

        self.voiture = voiture
        self.place = place
        self.date_debut = date_debut
        self.date_fin: Optional[date] = None

    @property
    def est_en_cours(self) -> bool:
        """Vrai tant que date_fin n'est pas renseignée."""
        raise NotImplementedError

    def partir_place(self) -> None:
        """Clôture le placement (date_fin = aujourd'hui) et libère la place.

        :raises RuntimeError: si le placement est déjà terminé.
        """
        raise NotImplementedError