"""La classe Client.

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime
    from .voiture import Voiture
    from .abonnement import Abonnement
    from .acces import Acces


class Client:
    """Client du parking (simple, abonné ou super-abonné = pack garanti)."""

    def __init__(self, nom: str, adresse: str):
        """Inscrit un client (nom et adresse obligatoires).

        :raises ValueError: si le nom ou l'adresse est vide.
        """
        if not nom.strip() or not adresse.strip():
            raise ValueError("Le nom et l'adresse du client sont obligatoires.")

        self.nom = nom
        self.adresse = adresse
        self.est_abonne = False
        self.est_super_abonne = False
        self.nb_frequentations = 0
        self.voitures: list = []
        self.abonnement: Optional["Abonnement"] = None
        self.services: list = []

    def s_abonner(self, ab: "Abonnement") -> None:
        """Souscrit ab : est_abonne=True ; est_super_abonne=True si pack garanti.

        :raises RuntimeError: si le client a déjà un abonnement en cours.
        """
        raise NotImplementedError

    def se_desabonner(self) -> None:
        """Rompt le contrat ; est_abonne et est_super_abonne repassent à False.

        :raises RuntimeError: si le client n'est pas abonné.
        """
        raise NotImplementedError

    def nouvelle_voiture(self, immat: str, haut: float, long: float) -> "Voiture":
        """Crée, rattache et retourne une voiture.

        :raises ValueError: immatriculation déjà utilisée par ce client ou dimensions invalides.
        """
        raise NotImplementedError

    def demander_maintenance(self) -> None:
        """Demande une maintenance du véhicule.

        :raises PermissionError: si le client n'est pas abonné.
        """
        raise NotImplementedError

    def demander_entretien(self) -> None:
        """Demande un entretien du véhicule.

        :raises PermissionError: si le client n'est pas abonné.
        """
        raise NotImplementedError

    def demander_livraison(self, date_liv: "datetime", heure: int, adresse_liv: str) -> None:
        """Demande la livraison de la voiture à une adresse, à une date et une heure.

        :raises PermissionError: si le client n'est pas abonné.
        """
        raise NotImplementedError

    def entrer_parking(self, a: "Acces") -> str:
        """Lance la procédure d'entrée via l'accès a ; incrémente nb_frequentations.

        :return: message de résultat (ticket délivré, ou 'Aucune place disponible pour votre véhicule').
        """
        raise NotImplementedError