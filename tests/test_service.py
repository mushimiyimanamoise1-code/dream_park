"""Tests unitaires de Service, Maintenance, Entretien, Livraison et Voiturier.

@author: MUSHIMIYIMANA MOISE
"""
import unittest
from datetime import datetime, timedelta

from dreampark.outils import aujourd_hui, maintenant
from dreampark.service import Service, Maintenance, Entretien, Livraison, Voiturier
from dreampark.voiture import Voiture


class TestService(unittest.TestCase):
    def test_service_abstrait(self):
        """Service ne peut pas être instancié directement."""
        with self.assertRaises(TypeError):
            Service()

    def test_date_demande_par_defaut(self):
        """Sans date, dateDemande est l'instant présent."""
        avant = maintenant()
        s = Maintenance()
        self.assertGreaterEqual(s.dateDemande, avant)
        self.assertLessEqual(s.dateDemande, maintenant())

    def test_date_demande_explicite(self):
        """Une dateDemande explicite est conservée."""
        d = datetime(2026, 11, 10, 9, 0)
        self.assertEqual(Entretien(d).dateDemande, d)

    def test_service_non_effectue_au_depart(self):
        """Avant effectuer() : dateService vide et rapport vide."""
        s = Maintenance()
        self.assertIsNone(s.dateService)
        self.assertEqual(s.rapport, "")


class TestEffectuer(unittest.TestCase):
    def test_maintenance(self):
        """effectuer() renseigne dateService et rapport."""
        s = Maintenance()
        s.effectuer()
        self.assertIsNotNone(s.dateService)
        self.assertNotEqual(s.rapport, "")

    def test_entretien(self):
        """effectuer() renseigne dateService et rapport."""
        s = Entretien()
        s.effectuer()
        self.assertIsNotNone(s.dateService)
        self.assertNotEqual(s.rapport, "")

    def test_livraison(self):
        """effectuer() renseigne dateService et rapport."""
        s = Livraison(None, "1 rue X", Voiturier(1))
        s.effectuer()
        self.assertIsNotNone(s.dateService)
        self.assertNotEqual(s.rapport, "")


class TestLivraison(unittest.TestCase):
    def test_attributs(self):
        """Adresse et voiturier sont conservés."""
        vt = Voiturier(7)
        liv = Livraison(None, "1 rue X", vt)
        self.assertEqual(liv.adresse, "1 rue X")
        self.assertIs(liv.voiturier, vt)

    def test_date_demande_par_defaut(self):
        """dateDemande None : l'instant présent est utilisé."""
        self.assertIsNotNone(Livraison(None, "1 rue X", Voiturier(1)).dateDemande)


class TestVoiturier(unittest.TestCase):
    def setUp(self):
        self.voiture = Voiture("AA-111-AA", 1.5, 4.0)

    def test_numero_conserve(self):
        """Le numéro du voiturier est conservé."""
        self.assertEqual(Voiturier(42).numVoiturier, 42)

    def test_heure_invalide(self):
        """Heure hors [0, 23] : ValueError."""
        for heure in (-1, 24, 25):
            with self.subTest(heure=heure), self.assertRaises(ValueError):
                Voiturier(1).livrer_voiture(self.voiture, aujourd_hui(), heure)

    def test_jour_passe(self):
        """Jour déjà passé : ValueError."""
        hier = aujourd_hui() - timedelta(days=1)
        with self.assertRaises(ValueError):
            Voiturier(1).livrer_voiture(self.voiture, hier, 10)

    def test_livraison_valide(self):
        """Jour futur et heure valide : aucune erreur."""
        demain = aujourd_hui() + timedelta(days=1)
        Voiturier(1).livrer_voiture(self.voiture, demain, 10)


if __name__ == "__main__":
    unittest.main()
