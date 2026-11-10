"""Tests unitaires de Client.

@author: MUSHIMIYIMANA MOISE
"""
import unittest

from dreampark.abonnement import Abonnement
from dreampark.acces import Acces
from dreampark.client import Client
from dreampark.parking import Parking
from dreampark.voiture import Voiture


class TestClientCreation(unittest.TestCase):
    def test_attributs_conserves(self):
        """Nom et adresse sont conservés."""
        c = Client("Dupont", "1 rue X")
        self.assertEqual((c.nom, c.adresse), ("Dupont", "1 rue X"))

    def test_etat_initial(self):
        """Client neuf : ni abonné ni super-abonné, aucune fréquentation, aucune voiture."""
        c = Client("Dupont", "1 rue X")
        self.assertFalse(c.estAbonne)
        self.assertFalse(c.estSuperAbonne)
        self.assertEqual(c.nbFrequentations, 0)
        self.assertEqual(c.voitures, [])
        self.assertEqual(c.services, [])
        self.assertIsNone(c.abonnement)

    def test_nom_ou_adresse_vide(self):
        """Nom ou adresse vide (ou d'espaces) : ValueError."""
        for nom, adresse in (("", "1 rue X"), ("  ", "1 rue X"), ("Dupont", ""), ("Dupont", "  ")):
            with self.subTest(nom=nom, adresse=adresse), self.assertRaises(ValueError):
                Client(nom, adresse)


class TestAbonnement(unittest.TestCase):
    def setUp(self):
        self.c = Client("Dupont", "1 rue X")

    def test_s_abonner(self):
        """Abonnement standard : abonné, pas super-abonné, abonnement mémorisé."""
        ab = Abonnement("Mensuel", 50)
        self.c.s_abonner(ab)
        self.assertTrue(self.c.estAbonne)
        self.assertFalse(self.c.estSuperAbonne)
        self.assertIs(self.c.abonnement, ab)

    def test_s_abonner_pack_garanti(self):
        """Pack garanti : le client devient super-abonné."""
        self.c.s_abonner(Abonnement("Pack", 90, estPackGaranti=True))
        self.assertTrue(self.c.estAbonne)
        self.assertTrue(self.c.estSuperAbonne)

    def test_s_abonner_deja_abonne(self):
        """Deuxième abonnement en cours : RuntimeError."""
        self.c.s_abonner(Abonnement("Mensuel", 50))
        with self.assertRaises(RuntimeError):
            self.c.s_abonner(Abonnement("Annuel", 400))

    def test_se_desabonner(self):
        """Après désabonnement : plus abonné ni super-abonné."""
        self.c.s_abonner(Abonnement("Pack", 90, estPackGaranti=True))
        self.c.se_desabonner()
        self.assertFalse(self.c.estAbonne)
        self.assertFalse(self.c.estSuperAbonne)

    def test_se_desabonner_sans_abonnement(self):
        """Désabonnement sans abonnement : RuntimeError."""
        with self.assertRaises(RuntimeError):
            self.c.se_desabonner()

    def test_reabonnement_possible(self):
        """Après un désabonnement, le client peut se réabonner."""
        self.c.s_abonner(Abonnement("Mensuel", 50))
        self.c.se_desabonner()
        self.c.s_abonner(Abonnement("Annuel", 400))
        self.assertTrue(self.c.estAbonne)


class TestVoitures(unittest.TestCase):
    def setUp(self):
        self.c = Client("Dupont", "1 rue X")

    def test_nouvelle_voiture(self):
        """La voiture est créée, retournée et rattachée au client."""
        v = self.c.nouvelle_voiture("AA-111-AA", 1.5, 4.0)
        self.assertIsInstance(v, Voiture)
        self.assertIn(v, self.c.voitures)

    def test_plusieurs_voitures(self):
        """Un client peut avoir plusieurs voitures différentes."""
        self.c.nouvelle_voiture("AA-111-AA", 1.5, 4.0)
        self.c.nouvelle_voiture("BB-222-BB", 1.6, 4.2)
        self.assertEqual(len(self.c.voitures), 2)

    def test_immatriculation_en_double(self):
        """Même immatriculation deux fois pour un même client : ValueError."""
        self.c.nouvelle_voiture("AA-111-AA", 1.5, 4.0)
        with self.assertRaises(ValueError):
            self.c.nouvelle_voiture("AA-111-AA", 1.6, 4.2)

    def test_dimensions_invalides(self):
        """Dimensions <= 0 : ValueError, et aucune voiture ajoutée."""
        with self.assertRaises(ValueError):
            self.c.nouvelle_voiture("AA-111-AA", -1, 4.0)
        self.assertEqual(self.c.voitures, [])


class TestServices(unittest.TestCase):
    def setUp(self):
        self.c = Client("Dupont", "1 rue X")

    def test_services_reserves_aux_abonnes(self):
        """Non abonné : PermissionError pour maintenance, entretien et livraison."""
        with self.assertRaises(PermissionError):
            self.c.demander_maintenance()
        with self.assertRaises(PermissionError):
            self.c.demander_entretien()
        with self.assertRaises(PermissionError):
            self.c.demander_livraison(None, 10, "2 rue Y")
        self.assertEqual(self.c.services, [])

    def test_demandes_d_un_abonne(self):
        """Abonné : chaque demande ajoute un service."""
        self.c.s_abonner(Abonnement("Mensuel", 50))
        self.c.demander_maintenance()
        self.c.demander_entretien()
        self.c.demander_livraison(None, 10, "2 rue Y")
        self.assertEqual(len(self.c.services), 3)


class TestEntrerParking(unittest.TestCase):
    def setUp(self):
        Parking.reinitialiser()
        self.parking = Parking.obtenir_instance(1, 2)
        self.c = Client("Dupont", "1 rue X")
        self.c.nouvelle_voiture("AA-111-AA", 1.5, 4.0)

    def tearDown(self):
        Parking.reinitialiser()

    def test_entree_reussie(self):
        """Place disponible : message de succès, fréquentation +1."""
        msg = self.c.entrer_parking(Acces(self.parking))
        self.assertIsInstance(msg, str)
        self.assertNotIn("Aucune place", msg)
        self.assertEqual(self.c.nbFrequentations, 1)

    def test_parking_plein(self):
        """Parking plein : message 'Aucune place disponible'."""
        for place in self.parking.places:
            place.estLibre = False
        msg = self.c.entrer_parking(Acces(self.parking))
        self.assertIn("Aucune place disponible", msg)


if __name__ == "__main__":
    unittest.main()
