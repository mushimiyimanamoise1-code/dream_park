"""Tests unitaires de Voiture.

@author: MUSHIMIYIMANA MOISE
"""
import unittest

from dreampark.place import Place
from dreampark.placement import Placement
from dreampark.voiture import Voiture


class TestVoitureCreation(unittest.TestCase):
    def test_attributs_conserves(self):
        """Les valeurs du constructeur sont conservées."""
        v = Voiture("AA-111-AA", 1.5, 4.0)
        self.assertEqual((v.immatriculation, v.hauteur, v.longueur), ("AA-111-AA", 1.5, 4.0))

    def test_aucun_placement_au_depart(self):
        """Une voiture neuve n'a aucun placement."""
        self.assertEqual(Voiture("AA-111-AA", 1.5, 4.0).placements, [])

    def test_immatriculation_vide(self):
        """Immatriculation vide ou composée d'espaces : ValueError."""
        for immat in ("", "   "):
            with self.subTest(immat=immat), self.assertRaises(ValueError):
                Voiture(immat, 1.5, 4.0)

    def test_hauteur_invalide(self):
        """Hauteur <= 0 : ValueError."""
        for hauteur in (0, -1):
            with self.subTest(hauteur=hauteur), self.assertRaises(ValueError):
                Voiture("AA-111-AA", hauteur, 4.0)

    def test_longueur_invalide(self):
        """Longueur <= 0 : ValueError."""
        for longueur in (0, -1):
            with self.subTest(longueur=longueur), self.assertRaises(ValueError):
                Voiture("AA-111-AA", 1.5, longueur)


class TestVoiturePlacements(unittest.TestCase):
    def setUp(self):
        self.voiture = Voiture("AA-111-AA", 1.5, 4.0)
        self.place = Place(1, "A", 5.0, 3.0)

    def _garer(self):
        pl = Placement(self.voiture, self.place)
        self.place.ajouter_placement(pl)
        self.voiture.ajouter_placement(pl)
        return pl

    def test_hors_parking_au_depart(self):
        """Sans placement : estDansParking est faux."""
        self.assertFalse(self.voiture.estDansParking)

    def test_ajouter_placement(self):
        """Le placement est mémorisé."""
        pl = self._garer()
        self.assertIn(pl, self.voiture.placements)

    def test_dans_parking_apres_ajout(self):
        """Avec un placement en cours : estDansParking est vrai."""
        self._garer()
        self.assertTrue(self.voiture.estDansParking)

    def test_hors_parking_apres_depart(self):
        """Placement clôturé : estDansParking redevient faux, l'historique reste."""
        pl = self._garer()
        pl.partir_place()
        self.assertFalse(self.voiture.estDansParking)
        self.assertEqual(len(self.voiture.placements), 1)


if __name__ == "__main__":
    unittest.main()
