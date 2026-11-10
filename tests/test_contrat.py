"""Tests unitaires de Contrat.

@author: MUSHIMIYIMANA MOISE
"""
import unittest
from datetime import timedelta

from dreampark.contrat import Contrat
from dreampark.outils import aujourd_hui


class TestContrat(unittest.TestCase):
    def setUp(self):
        self.auj = aujourd_hui()

    def test_debut_par_defaut(self):
        """Sans date, dateDebut = aujourd'hui ; dateFin vide."""
        c = Contrat()
        self.assertEqual(c.dateDebut, self.auj)
        self.assertIsNone(c.dateFin)

    def test_dates_conservees(self):
        """Les dates données sont conservées."""
        debut, fin = self.auj - timedelta(days=5), self.auj + timedelta(days=5)
        c = Contrat(debut, fin)
        self.assertEqual((c.dateDebut, c.dateFin), (debut, fin))

    def test_dates_incoherentes(self):
        """dateFin avant dateDebut : ValueError."""
        with self.assertRaises(ValueError):
            Contrat(self.auj, self.auj - timedelta(days=1))

    def test_meme_jour_accepte(self):
        """dateDebut == dateFin est accepté."""
        Contrat(self.auj, self.auj)

    def test_en_cours_sans_fin(self):
        """Sans date de fin : en cours."""
        self.assertTrue(Contrat(self.auj - timedelta(days=3)).estEnCours)

    def test_en_cours_dernier_jour_inclus(self):
        """Le jour de dateFin, le contrat est encore en cours."""
        self.assertTrue(Contrat(self.auj - timedelta(days=3), self.auj).estEnCours)

    def test_termine(self):
        """dateFin passée : plus en cours."""
        c = Contrat(self.auj - timedelta(days=10), self.auj - timedelta(days=1))
        self.assertFalse(c.estEnCours)

    def test_pas_encore_commence(self):
        """dateDebut dans le futur : pas encore en cours."""
        self.assertFalse(Contrat(self.auj + timedelta(days=1)).estEnCours)

    def test_rompre_contrat(self):
        """rompre_contrat() fixe dateFin à aujourd'hui et termine le contrat."""
        c = Contrat(self.auj - timedelta(days=3))
        c.rompre_contrat()
        self.assertEqual(c.dateFin, self.auj)

    def test_rompre_contrat_deja_termine(self):
        """Rompre un contrat déjà terminé : RuntimeError."""
        c = Contrat(self.auj - timedelta(days=10), self.auj - timedelta(days=1))
        with self.assertRaises(RuntimeError):
            c.rompre_contrat()


if __name__ == "__main__":
    unittest.main()
