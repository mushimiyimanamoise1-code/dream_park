"""Tests unitaires de Camera, Teleporteur, BorneTicket et PanneauAffichage.

@author: MUSHIMIYIMANA MOISE
"""
import unittest

from dreampark.abonnement import Abonnement
from dreampark.client import Client
from dreampark.equipements import Camera, Teleporteur, BorneTicket, PanneauAffichage
from dreampark.parking import Parking
from dreampark.place import Place
from dreampark.placement import Placement
from dreampark.voiture import Voiture


class TestCamera(unittest.TestCase):
    def setUp(self):
        self.voiture = Voiture("AA-111-AA", 1.5, 4.0)
        self.camera = Camera()

    def test_capturer_hauteur(self):
        """Retourne la hauteur de la voiture."""
        self.assertEqual(self.camera.capturer_hauteur(self.voiture), 1.5)

    def test_capturer_longueur(self):
        """Retourne la longueur de la voiture."""
        self.assertEqual(self.camera.capturer_longueur(self.voiture), 4.0)

    def test_capturer_immatriculation(self):
        """Retourne l'immatriculation de la voiture."""
        self.assertEqual(self.camera.capturer_immatriculation(self.voiture), "AA-111-AA")


class TestTeleporteur(unittest.TestCase):
    def setUp(self):
        self.voiture = Voiture("AA-111-AA", 1.5, 4.0)
        self.place = Place(1, "A", 5.0, 3.0)

    def test_teleporter_voiture(self):
        """Retourne un Placement en cours ; la place est occupée, la voiture dans le parking."""
        pl = Teleporteur().teleporter_voiture(self.voiture, self.place)
        self.assertIsInstance(pl, Placement)
        self.assertTrue(pl.estEnCours)
        self.assertFalse(self.place.estLibre)
        self.assertTrue(self.voiture.estDansParking)

    def test_teleporter_place_occupee(self):
        """Place déjà occupée : ValueError."""
        self.place.ajouter_placement(Placement(self.voiture, self.place))
        with self.assertRaises(ValueError):
            Teleporteur().teleporter_voiture(Voiture("BB-222-BB", 1.5, 4.0), self.place)

    def test_teleporter_place_trop_petite(self):
        """Voiture trop haute pour la place : ValueError, place toujours libre."""
        grande = Voiture("CC-333-CC", 3.5, 4.0)
        with self.assertRaises(ValueError):
            Teleporteur().teleporter_voiture(grande, self.place)
        self.assertTrue(self.place.estLibre)

    def test_teleporter_super_abonne(self):
        """Retourne un message de résultat."""
        self.assertIsInstance(Teleporteur().teleporter_voiture_super_abonne(self.voiture), str)


class TestBorneTicket(unittest.TestCase):
    def setUp(self):
        self.borne = BorneTicket()
        self.client = Client("Dupont", "1 rue X")

    def tearDown(self):
        Parking.reinitialiser()

    def test_delivrer_ticket(self):
        """Le ticket est un texte non vide."""
        ticket = self.borne.delivrer_ticket(self.client)
        self.assertIsInstance(ticket, str)
        self.assertNotEqual(ticket, "")

    def test_tickets_uniques(self):
        """Deux tickets délivrés sont différents."""
        self.assertNotEqual(self.borne.delivrer_ticket(self.client),
                            self.borne.delivrer_ticket(self.client))

    def test_type_paiement_valide(self):
        """Le paiement proposé est 'CB' ou 'ESPECES'."""
        self.assertIn(self.borne.proposer_type_paiement(), ("CB", "ESPECES"))

    def test_proposer_services(self):
        """Retourne la liste des services (texte non vide)."""
        self.assertNotEqual(self.borne.proposer_services(), "")

    def test_proposer_abonnements(self):
        """La liste proposée contient les abonnements du parking."""
        Parking.reinitialiser()
        parking = Parking.obtenir_instance(1, 1)
        parking.ajouter_abonnement(Abonnement("Mensuel", 50))
        self.assertIn("Mensuel", self.borne.proposer_abonnements(self.client, parking))

    def test_recuperer_infos_carte(self):
        """Retourne un texte pour tout client."""
        self.assertIsInstance(self.borne.recuperer_infos_carte(self.client), str)


class TestPanneauAffichage(unittest.TestCase):
    def setUp(self):
        Parking.reinitialiser()
        self.parking = Parking.obtenir_instance(1, 2)

    def tearDown(self):
        Parking.reinitialiser()

    def test_affiche_le_nombre_de_places(self):
        """Affiche le nombre de places libres."""
        self.assertIn("2", PanneauAffichage().afficher_nb_places_disponibles(self.parking))

    def test_affichage_mis_a_jour(self):
        """L'affichage suit l'état du parking."""
        self.parking.places[0].estLibre = False
        self.assertIn("1", PanneauAffichage().afficher_nb_places_disponibles(self.parking))

    def test_affichage_complet(self):
        """Parking plein : 'COMPLET'."""
        for pl in self.parking.places:
            pl.estLibre = False
        self.assertIn("COMPLET", PanneauAffichage().afficher_nb_places_disponibles(self.parking))


if __name__ == "__main__":
    unittest.main()
