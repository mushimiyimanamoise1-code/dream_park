"""Tests unitaires de Place.

@author: MUSHIMIYIMANA MOISE
"""
import unittest

from dreampark.place import Place
from dreampark.placement import Placement
from dreampark.voiture import Voiture


def une_voiture(hauteur=1.5, longueur=4.0):
    return Voiture("AA-111-AA", hauteur, longueur)


class TestPlaceCreation(unittest.TestCase):
    def test_attributs_conserves(self):
        """Les valeurs passées au constructeur sont conservées."""
        p = Place(15, "C", 5.0, 3.0)
        self.assertEqual((p.numero, p.niveau, p.longueur, p.hauteur), (15, "C", 5.0, 3.0))

    def test_place_neuve_est_libre(self):
        """Une place créée est libre."""
        self.assertTrue(Place(1, "A", 5.0, 3.0).estLibre)

    def test_numero_invalide(self):
        """Numéro < 1 : ValueError."""
        for numero in (0, -3):
            with self.subTest(numero=numero), self.assertRaises(ValueError):
                Place(numero, "A", 5.0, 3.0)

    def test_niveau_invalide(self):
        """Niveau qui n'est pas une lettre majuscule unique : ValueError."""
        for niveau in ("", "AB", "a", "1", " "):
            with self.subTest(niveau=niveau), self.assertRaises(ValueError):
                Place(1, niveau, 5.0, 3.0)

    def test_longueur_hors_limites(self):
        """Longueur < 4 m ou > 6 m : ValueError."""
        for longueur in (3.9, 6.1):
            with self.subTest(longueur=longueur), self.assertRaises(ValueError):
                Place(1, "A", longueur, 3.0)

    def test_hauteur_hors_limites(self):
        """Hauteur < 2 m ou > 4 m : ValueError."""
        for hauteur in (1.9, 4.1):
            with self.subTest(hauteur=hauteur), self.assertRaises(ValueError):
                Place(1, "A", 5.0, hauteur)

    def test_bornes_incluses(self):
        """Les valeurs limites (4 / 6 m et 2 / 4 m) sont acceptées."""
        Place(1, "A", 4.0, 2.0)
        Place(1, "A", 6.0, 4.0)


class TestIdPlace(unittest.TestCase):
    def test_id_place_niveau_puis_numero(self):
        """idPlace = niveau + numéro."""
        self.assertEqual(Place(15, "C", 5.0, 3.0).idPlace, "C15")
        self.assertEqual(Place(1, "A", 5.0, 3.0).idPlace, "A1")

    def test_id_place_distincts(self):
        """Deux places différentes ont des identifiants différents."""
        self.assertNotEqual(Place(1, "A", 5.0, 3.0).idPlace, Place(1, "B", 5.0, 3.0).idPlace)


class TestConvientA(unittest.TestCase):
    def setUp(self):
        self.place = Place(15, "C", 5.0, 3.0)

    def test_voiture_plus_petite(self):
        """Voiture plus petite que la place : convient."""
        self.assertTrue(self.place.convient_a(une_voiture(1.5, 4.0)))

    def test_voiture_aux_dimensions_exactes(self):
        """Voiture exactement aux dimensions de la place : convient (<=)."""
        self.assertTrue(self.place.convient_a(une_voiture(3.0, 5.0)))

    def test_voiture_trop_haute(self):
        """Voiture trop haute : ne convient pas."""
        self.assertFalse(self.place.convient_a(une_voiture(3.5, 4.0)))

    def test_voiture_trop_longue(self):
        """Voiture trop longue : ne convient pas."""
        self.assertFalse(self.place.convient_a(une_voiture(1.5, 5.5)))

    def test_place_occupee(self):
        """Place occupée : ne convient pas, même si les dimensions sont bonnes."""
        v = une_voiture()
        self.place.ajouter_placement(Placement(v, self.place))
        self.assertFalse(self.place.convient_a(v))


class TestAjouterPlacementEtLiberer(unittest.TestCase):
    def setUp(self):
        self.place = Place(1, "A", 5.0, 3.0)

    def test_ajouter_placement_occupe_la_place(self):
        """Après ajouter_placement, la place n'est plus libre."""
        self.place.ajouter_placement(Placement(une_voiture(), self.place))
        self.assertFalse(self.place.estLibre)

    def test_liberer(self):
        """liberer() remet la place libre."""
        self.place.ajouter_placement(Placement(une_voiture(), self.place))
        self.place.liberer()
        self.assertTrue(self.place.estLibre)


if __name__ == "__main__":
    unittest.main()
