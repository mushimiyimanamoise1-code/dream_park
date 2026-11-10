"""
La classe Contrat

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from .outils import maintenant
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


class Contrat:
    """Lien entre un client et un abonnement sur une période donnée."""

    def __init__(self, dateDebut: Optional[datetime] = None, dateFin: Optional[datetime] = None):
        """Crée un contrat.

        :param date_debut: début du contrat (aujourd'hui par défaut)
        :param date_fin: fin du contrat (None = durée illimitée)

        erreur
        :raises ValueError: si date_fin < date_debut.
        """
        if dateDebut is None:
            dateDebut = maintenant()
        if dateFin is not None and dateFin < dateDebut:
            raise ValueError("date_fin ne peut pas précéder date_debut.")

        self.dateDebut = dateDebut
        self.dateFin = dateFin

    @property
    def estEnCours(self) -> bool:
        """Vrai si aujourd'hui est dans [date_debut, date_fin] (date_fin None = illimité)."""
        raise NotImplementedError

    def rompre_contrat(self) -> None:
        """Met date_fin à aujourd'hui.

        :raises RuntimeError: si le contrat n'est pas en cours.
        """
        raise NotImplementedError