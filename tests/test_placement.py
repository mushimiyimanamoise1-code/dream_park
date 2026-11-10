"""Tests unitaires de Placement.

@author: MUSHIMIYIMANA MOISE
"""
import unittest
from datetime import timedelta

from dreampark.outils import aujourd_hui
from dreampark.place import Place
from dreampark.placement import Placement
from dreampark.voiture import Voiture


class TestPlacement(unittest.TestCase):
    def setUp(self):
        self.place = Place(1, "A", 5.0, 3.0)
        self.voiture = Voiture("AA-111-AA", 1.5, 4.0)

    def _placement_actif(self):
        pl = Placement(self.voiture, self.place)
        self.place.ajouter_placement(pl)
        return pl

    def test_creation_sans_date(self):
        """Sans date, dateDebut = aujourd'hui ; dateFin vide."""
        pl = Placement(self.voiture, self.place)
        self.assertEqual(pl.dateDebut, aujourd_hui())
        self.assertIsNone(pl.dateFin)

    def test_creation_avec_date(self):
        """Une date de début explicite est conservée."""
        d = aujourd_hui() - timedelta(days=2)
        self.assertEqual(Placement(self.voiture, self.place, d).dateDebut, d)

    def test_voiture_et_place_conservees(self):
        """Le placement référence la voiture et la place données."""
        pl = Placement(self.voiture, self.place)
        self.assertIs(pl.voiture, self.voiture)
        self.assertIs(pl.place, self.place)

    def test_voiture_none(self):
        """Voiture None : ValueError."""
        with self.assertRaises(ValueError):
            Placement(None, self.place)

    def test_place_none(self):
        """Place None : ValueError."""
        with self.assertRaises(ValueError):
            Placement(self.voiture, None)

    def test_en_cours_a_la_creation(self):
        """Un placement neuf est en cours."""
        self.assertTrue(Placement(self.voiture, self.place).estEnCours)

    def test_partir_place_cloture_le_placement(self):
        """partir_place() termine le placement et renseigne dateFin."""
        pl = self._placement_actif()
        pl.partir_place()
        self.assertFalse(pl.estEnCours)
        self.assertEqual(pl.dateFin, aujourd_hui())

    def test_partir_place_libere_la_place(self):
        """partir_place() libère la place occupée."""
        pl = self._placement_actif()
        pl.partir_place()
        self.assertTrue(self.place.estLibre)

    def test_partir_place_deux_fois(self):
        """Clôturer un placement déjà terminé : RuntimeError."""
        pl = self._placement_actif()
        pl.partir_place()
        with self.assertRaises(RuntimeError):
            pl.partir_place()


if __name__ == "__main__":
    unittest.main()
