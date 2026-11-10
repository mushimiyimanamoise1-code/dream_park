"""Services proposés aux abonnés.

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from .outils import maintenant

if TYPE_CHECKING:
    from datetime import date, datetime
    from .voiture import Voiture


class Service(ABC):
    """Service demandé par un client abonné."""

    def __init__(self, dateDemande: Optional[datetime] = None,
                 dateService: Optional[datetime] = None):
        """:param dateDemande: date de la demande (maintenant par défaut)
        :param dateService: date de réalisation (None tant que non effectué)
        """
        if dateDemande is None:
            dateDemande = maintenant()
        self.dateDemande = dateDemande
        self.dateService = dateService
        self.rapport = ""

    @abstractmethod
    def effectuer(self) -> None:
        """Réalise le service et renseigne rapport et dateService."""


class Maintenance(Service):
    """Maintenance du véhicule."""

    def effectuer(self) -> None:
        """Réalise la maintenance (délègue à effectuer_maintenance)."""
        raise NotImplementedError

    def effectuer_maintenance(self, v: "Voiture") -> None:
        """Prend la voiture en charge, la répare, la regare au retour."""
        raise NotImplementedError


class Entretien(Service):
    """Entretien courant du véhicule."""

    def effectuer(self) -> None:
        """Réalise l'entretien (délègue à effectuer_entretien)."""
        raise NotImplementedError

    def effectuer_entretien(self) -> None:
        """Réalise l'entretien courant du véhicule."""
        raise NotImplementedError


class Voiturier:
    """Employé qui livre les voitures (pas de classe pour l'UC 'Se garer')."""

    def __init__(self, numVoiturier: int):
        self.numVoiturier = numVoiturier

    def livrer_voiture(self, v: "Voiture", jour: "date", heure: int) -> None:
        """Livre v à la date et à l'heure (0-23) demandées.

        :raises ValueError: si l'heure est hors [0, 23] ou le jour est passé.
        """
        raise NotImplementedError


class Livraison(Service):
    """Livraison de la voiture à une adresse, à une heure donnée."""

    def __init__(self, dateDemande: Optional[datetime], adresse: str, voiturier: Voiturier,
                 dateService: Optional[datetime] = None):
        """
        :param dateDemande: date de la demande (None = maintenant)
        :param adresse: adresse de livraison
        :param voiturier: voiturier chargé de la livraison
        """
        super().__init__(dateDemande, dateService)
        self.adresse = adresse
        self.voiturier = voiturier

    def effectuer(self) -> None:
        """Réalise la livraison (délègue à effectuer_livraison)."""
        raise NotImplementedError

    def effectuer_livraison(self) -> None:
        """Délègue au voiturier la livraison à l'adresse demandée."""
        raise NotImplementedError