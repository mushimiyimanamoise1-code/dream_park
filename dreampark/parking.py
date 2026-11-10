"""La classe Parking (singleton) : unique dans l'application

@author: MUSHIMIYIMANA MOISE
"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .voiture import Voiture
    from .abonnement import Abonnement
    from .place import Place
    from .acces import Acces 

class Parking:
    """Une seule instance dans l'application ; contient les places et les abonnements."""

    _instance: Optional["Parking"] = None

    def __init__(self, nbNiveaux: int, nbPlacesParNiveau: int, prix: int = 0):
        """Initialise le parking et l'enregistre comme instance unique.

        :param nbNiveaux: nombre de niveaux (>= 1)
        :param nbplacesParNiveau: nombre de places par niveau (>= 1)
        :param prix: tarif du parking (>= 0)

        les Erreurs
        :raises RuntimeError: si une instance existe déjà (singleton).
        :raises ValueError: si nb_niveaux < 1, nb_places_par_niveau < 1 ou prix < 0.
        """
        if Parking._instance is not None:
            raise RuntimeError("Parking est un singleton : utiliser Parking.obtenir_instance().")
        if nbNiveaux < 1 or nbPlacesParNiveau < 1 or prix < 0:
            raise ValueError("nb_niveaux et nb_places_par_niveau doivent être >= 1, prix >= 0.")

        self.nbNiveaux = nbNiveaux
        self.nbNlaces_par_niveau = nbPlacesParNiveau
        self.prix = prix

        self.places: list = []
        self.abonnements: list = []

        self.acces1 = Acces(self)
        self.acces2 = Acces(self)

        Parking._instance = self

    @classmethod
    def obtenir_instance(cls, nbNiveaux: int = 1, nbPlacesParNiveau: int = 1, prix: int = 0) -> "Parking":
        """Retourne l'unique instance (créée au premier appel).

        Si l'instance existe déjà, elle est retournée et les arguments sont ignorés.

        :raises ValueError: si nb_niveaux ou nb_places_par_niveau < 1, ou prix < 0, à la création.
        """
        raise NotImplementedError

    @classmethod
    def reinitialiser(cls) -> None:
        """Détruit l'instance et réinitialise ses valeurs comme à l'initiale."""
        raise NotImplementedError

    @property
    def nb_places_libres(self) -> int:
        """Nombre total de places libres (attribut dérivé)."""
        raise NotImplementedError

    def rechercher_place(self, v: "Voiture") -> Optional["Place"]:
        """Retourne une place libre compatible avec v, ou None si aucune."""
        raise NotImplementedError

    def nb_places_libres_par_niveau(self, niveau: str) -> int:
        """Nombre de places libres du niveau.

        :raises ValueError: si le niveau n'existe pas.
        """
        raise NotImplementedError

    def ajouter_abonnement(self, ab: "Abonnement") -> None:
        """Ajoute une formule d'abonnement au catalogue."""
        raise NotImplementedError
