"""Équipements des accès : caméra, téléporteur, borne, panneau.

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client
    from .voiture import Voiture
    from .place import Place
    from .placement import Placement
    from .parking import Parking


class Camera:
    """Caméra d'un accès : capture les caractéristiques d'une voiture."""

    def capturer_hauteur(self, v: "Voiture") -> float:
        """Retourne la hauteur de v (m)."""
        raise NotImplementedError

    def capturer_longueur(self, v: "Voiture") -> float:
        """Retourne la longueur de v (m)."""
        raise NotImplementedError

    def capturer_immatriculation(self, v: "Voiture") -> str:
        """Retourne l'immatriculation de v."""
        raise NotImplementedError


class Teleporteur:
    """Téléporte une voiture entre l'accès et sa place."""

    def teleporter_voiture(self, v: "Voiture", p: "Place") -> "Placement":
        """Téléporte v sur p, crée et retourne le Placement.

        :raises ValueError: si p n'est pas libre ou ne convient pas à v.
        """
        raise NotImplementedError

    def teleporter_voiture_super_abonne(self, v: "Voiture") -> str:
        """Téléporte v d'un super-abonné (place garantie, éventuellement autre parking).

        :return: message de résultat.
        """
        raise NotImplementedError


class BorneTicket:
    """Borne de ticket et de paiement."""

    def delivrer_ticket(self, c: "Client") -> str:
        """Retourne le ticket (identifiant unique) pour le client c."""
        raise NotImplementedError

    def proposer_services(self) -> str:
        """Liste des services proposés aux abonnés."""
        raise NotImplementedError

    def proposer_abonnements(self, c: "Client", p: "Parking") -> str:
        """Liste des abonnements de p proposés à un client non abonné."""
        raise NotImplementedError

    def recuperer_infos_carte(self, c: "Client") -> str:
        """Lit la carte d'abonnement de c ; retourne son statut."""
        raise NotImplementedError

    def proposer_type_paiement(self) -> str:
        """Retourne 'CB' ou 'ESPECES' selon le choix du client."""
        raise NotImplementedError


class PanneauAffichage:
    """Panneau extérieur indiquant les places disponibles."""

    def afficher_nb_places_disponibles(self, p: "Parking") -> str:
        """Retourne le texte affiché (ex. '12 places disponibles', 'COMPLET' si 0)."""
        raise NotImplementedError
