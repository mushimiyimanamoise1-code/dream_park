"""Tests unitaires de Parking (singleton).

@author: MUSHIMIYIMANA MOISE
"""
import unittest

from dreampark.abonnement import Abonnement
from dreampark.parking import Parking
from dreampark.voiture import Voiture


def une_voiture(hauteur=1.5, longueur=4.0):
    return Voiture("AA-111-AA", hauteur, longueur)


class TestParking(unittest.TestCase):
    def setUp(self):
        Parking.reinitialiser()
        self.p = Parking.obtenir_instance(2, 3, 5)

    def tearDown(self):
        Parking.reinitialiser()

    # --- singleton ---
    def test_singleton(self):
        """Deux appels retournent le même objet."""
        self.assertIs(self.p, Parking.obtenir_instance())

    def test_instanciation_directe_interdite(self):
        """Parking(...) alors qu'une instance existe : RuntimeError."""
        with self.assertRaises(RuntimeError):
            Parking(1, 1, 3)

    def test_instanciation_directe_enregistre_instance(self):
        """Parking(1, 1, 3) sans instance existante : enregistré comme singleton."""
        Parking.reinitialiser()
        parc = Parking(1, 1, 3)
        self.assertIs(parc, Parking.obtenir_instance())
        with self.assertRaises(RuntimeError):
            Parking(2, 2, 5)

    def test_obtenir_instance_ignore_arguments_si_existante(self):
        """Instance existante : les arguments sont ignorés."""
        autre = Parking.obtenir_instance(5, 20, 9)
        self.assertIs(autre, self.p)
        self.assertEqual(autre.nbNiveaux, 2)

    def test_reinitialiser(self):
        """Après reinitialiser(), une nouvelle instance est créée."""
        Parking.reinitialiser()
        nouveau = Parking.obtenir_instance(1, 1)
        self.assertIsNot(nouveau, self.p)
        self.assertEqual(nouveau.nbNiveaux, 1)

    # --- création ---
    def test_attributs(self):
        """Les paramètres de création sont conservés."""
        self.assertEqual((self.p.nbNiveaux, self.p.nbPlacesParNiveau, self.p.prix), (2, 3, 5))

    def test_valeurs_invalides(self):
        """nbNiveaux < 1, nbPlacesParNiveau < 1 ou prix < 0 : ValueError."""
        for args in ((0, 3, 5), (2, 0, 5), (2, 3, -1)):
            Parking.reinitialiser()
            with self.subTest(args=args), self.assertRaises(ValueError):
                Parking.obtenir_instance(*args)

    def test_echec_creation_ne_laisse_pas_d_instance(self):
        """Une création refusée n'enregistre rien : on peut ensuite créer normalement."""
        Parking.reinitialiser()
        with self.assertRaises(ValueError):
            Parking(0, 1, 1)
        self.assertEqual(Parking.obtenir_instance(1, 1).nbNiveaux, 1)

    def test_nombre_de_places(self):
        """nbNiveaux x nbPlacesParNiveau places sont créées (2 x 3 = 6)."""
        self.assertEqual(len(self.p.places), 6)

    def test_identifiants_uniques(self):
        """Chaque place a un identifiant unique, sur les niveaux A et B."""
        ids = [pl.idPlace for pl in self.p.places]
        self.assertEqual(len(set(ids)), 6)
        self.assertEqual({pl.niveau for pl in self.p.places}, {"A", "B"})

    def test_aucun_abonnement_au_depart(self):
        """Le catalogue d'abonnements est vide au départ."""
        self.assertEqual(self.p.abonnements, [])

    # --- places libres ---
    def test_places_libres_initiales(self):
        """Parking neuf : toutes les places sont libres."""
        self.assertEqual(self.p.nbPlacesLibres, 6)

    def test_places_libres_diminuent(self):
        """Occuper une place diminue nbPlacesLibres."""
        self.p.places[0].estLibre = False
        self.assertEqual(self.p.nbPlacesLibres, 5)

    def test_places_libres_par_niveau(self):
        """Niveau 'A' : 3 places libres au départ, 2 après occupation d'une place de A."""
        self.assertEqual(self.p.nb_places_libres_par_niveau("A"), 3)
        place_a = next(pl for pl in self.p.places if pl.niveau == "A")
        place_a.estLibre = False
        self.assertEqual(self.p.nb_places_libres_par_niveau("A"), 2)
        self.assertEqual(self.p.nb_places_libres_par_niveau("B"), 3)

    def test_niveau_inconnu(self):
        """Niveau inexistant : ValueError."""
        with self.assertRaises(ValueError):
            self.p.nb_places_libres_par_niveau("Z")

    # --- recherche ---
    def test_rechercher_place_libre(self):
        """Voiture standard : une place libre compatible est retournée."""
        v = une_voiture()
        place = self.p.rechercher_place(v)
        self.assertIsNotNone(place)
        self.assertTrue(place.estLibre)
        self.assertTrue(place.convient_a(v))

    def test_rechercher_place_parking_plein(self):
        """Parking plein : None."""
        for pl in self.p.places:
            pl.estLibre = False
        self.assertIsNone(self.p.rechercher_place(une_voiture()))

    def test_rechercher_place_voiture_trop_haute(self):
        """Voiture plus haute que toute place : None."""
        self.assertIsNone(self.p.rechercher_place(une_voiture(hauteur=9.0)))

    def test_rechercher_place_voiture_trop_longue(self):
        """Voiture plus longue que toute place : None."""
        self.assertIsNone(self.p.rechercher_place(une_voiture(longueur=12.0)))

    def test_rechercher_place_ne_choisit_pas_une_place_occupee(self):
        """Une seule place libre : c'est celle-là qui est retournée."""
        for pl in self.p.places[1:]:
            pl.estLibre = False
        self.assertIs(self.p.rechercher_place(une_voiture()), self.p.places[0])

    # --- abonnements ---
    def test_ajouter_abonnement(self):
        """L'abonnement est ajouté au catalogue."""
        ab = Abonnement("Mensuel", 50)
        self.p.ajouter_abonnement(ab)
        self.assertEqual(self.p.abonnements, [ab])


if __name__ == "__main__":
    unittest.main()
