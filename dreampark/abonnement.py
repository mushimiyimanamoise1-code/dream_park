"""
la classe Abonnements

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .contrat import Contrat


class Abonnement:
    """Formule d'abonnement (le pack garanti est un abonnement particulier).
    
    NB un particulier peut avoir plusieurs contrat pour chacune de ses voiture.
    """

    def __init__(self, libelle: str, prix: float, estPackGar: bool = False):

        """:raises ValueError: libellé vide ou prix < 0."""
        self.libelle = libelle
        self.prix = prix
        self.estPackGar = estPackGar
        
        self.contrats: list = []

    def ajouter_contrat(self, contrat: "Contrat") -> None:
        """Rattache un contrat à cet abonnement."""
        raise NotImplementedError

    def afficher_contrat(self) -> list:
        """affiche les contrats de cet abonnement.
        """
        raise NotImplementedError
