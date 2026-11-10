"""Accès du parking.

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from .equipements import Camera, BorneTicket, PanneauAffichage, Teleporteur

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
    from .voiture import Voiture
    from .parking import Parking


class Acces:
    """Entrée/sortie du parking : 1 caméra, 1 borne, 1 panneau, 2 téléporteurs."""

    def __init__(self, parking: "Parking"):
        self.parking = parking
        self.camera = Camera()
        self.borne = BorneTicket()
        self.panneau = PanneauAffichage()
        self.tel_entree = Teleporteur()
        self.tel_sortie = Teleporteur()

    def actionner_camera(self, c: "Client") -> "Voiture":
        """Photographie la voiture du client et retourne la Voiture identifiée."""
        raise NotImplementedError

    def actionner_panneau(self) -> str:
        """Met à jour et retourne l'affichage du panneau."""
        raise NotImplementedError

    def lancer_procedure_entree(self, c: "Client") -> str:
        """Déroule l'activité 'Se garer' (cf. diagramme d'activité).

        :return: ticket, ou 'Aucune place disponible pour votre véhicule'.
        """
        raise NotImplementedError
