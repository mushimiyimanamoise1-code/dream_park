"""Tests unitaires de Acces.

@author: MUSHIMIYIMANA MOISE
"""
import unittest

from dreampark.acces import Acces
from dreampark.client import Client
from dreampark.equipements import Camera, BorneTicket, PanneauAffichage, Teleporteur
from dreampark.parking import Parking
from dreampark.voiture import Voiture


class TestAcces(unittest.TestCase):
    def setUp(self):
        Parking.reinitialiser()
        self.parking = Parking.obtenir_instance(1, 1)
        self.acces = Acces(self.parking)
        self.client = Client("Dupont", "1 rue X")
        self.voiture = self.client.nouvelle_voiture("AA-111-AA", 1.5, 4.0)

    def tearDown(self):
        Parking.reinitialiser()

    def test_composition(self):
        """Un accès connaît son parking et possède caméra, borne, panneau et deux téléporteurs."""
        self.assertIs(self.acces.parking, self.parking)
        self.assertIsInstance(self.acces.camera, Camera)
        self.assertIsInstance(self.acces.borne, BorneTicket)
        self.assertIsInstance(self.acces.panneau, PanneauAffichage)
        self.assertIsInstance(self.acces.telEntree, Teleporteur)
        self.assertIsInstance(self.acces.telSortie, Teleporteur)
        self.assertIsNot(self.acces.telEntree, self.acces.telSortie)

    def test_deux_acces_independants(self):
        """Deux accès ont leurs propres équipements mais partagent le même parking."""
        autre = Acces(self.parking)
        self.assertIsNot(self.acces.camera, autre.camera)
        self.assertIs(self.acces.parking, autre.parking)

    def test_actionner_camera(self):
        """La caméra identifie la voiture du client."""
        self.assertIs(self.acces.actionner_camera(self.client), self.voiture)

    def test_actionner_panneau(self):
        """Le panneau affiche le nombre de places libres."""
        self.assertIn("1", self.acces.actionner_panneau())

    def test_procedure_entree_reussie(self):
        """Place disponible : un ticket est retourné et la place devient occupée."""
        resultat = self.acces.lancer_procedure_entree(self.client)
        self.assertIsInstance(resultat, str)
        self.assertNotIn("Aucune place", resultat)
        self.assertEqual(self.parking.nbPlacesLibres, 0)
        self.assertTrue(self.voiture.estDansParking)

    def test_procedure_entree_parking_plein(self):
        """Parking plein : message d'absence de place, rien n'est modifié."""
        self.parking.places[0].estLibre = False
        resultat = self.acces.lancer_procedure_entree(self.client)
        self.assertIn("Aucune place disponible", resultat)
        self.assertFalse(self.voiture.estDansParking)

    def test_panneau_mis_a_jour_apres_entree(self):
        """Après une entrée, le panneau indique que le parking est complet."""
        self.acces.lancer_procedure_entree(self.client)
        self.assertIn("COMPLET", self.acces.actionner_panneau())

    @unittest.skip("À activer si Parking possède acces1 et acces2 (modification à justifier).")
    def test_parking_possede_deux_acces(self):
        """Le parking a deux accès distincts, qui pointent vers lui."""
        self.assertIsNot(self.parking.acces1, self.parking.acces2)
        self.assertIs(self.parking.acces1.parking, self.parking)
        self.assertIs(self.parking.acces2.parking, self.parking)


if __name__ == "__main__":
    unittest.main()
