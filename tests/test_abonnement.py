"""Tests unitaires de Abonnement.

@author: MUSHIMIYIMANA MOISE
"""
import unittest

from dreampark.abonnement import Abonnement
from dreampark.contrat import Contrat


class TestAbonnement(unittest.TestCase):
    def test_attributs_conserves(self):
        """Les valeurs du constructeur sont conservées."""
        ab = Abonnement("Mensuel", 50)
        self.assertEqual((ab.libelle, ab.prix), ("Mensuel", 50))

    def test_pack_garanti_faux_par_defaut(self):
        """Par défaut, ce n'est pas un pack garanti."""
        self.assertFalse(Abonnement("Mensuel", 50).estPackGaranti)

    def test_pack_garanti(self):
        """estPackGaranti=True est conservé."""
        self.assertTrue(Abonnement("Pack", 90, estPackGaranti=True).estPackGaranti)

    def test_aucun_contrat_au_depart(self):
        """Une formule neuve n'a aucun contrat."""
        self.assertEqual(Abonnement("Mensuel", 50).contrats, [])

    def test_prix_zero_accepte(self):
        """Un prix de 0 est accepté."""
        Abonnement("Gratuit", 0)

    def test_prix_negatif(self):
        """Prix < 0 : ValueError."""
        with self.assertRaises(ValueError):
            Abonnement("Mensuel", -5)

    def test_libelle_vide(self):
        """Libellé vide ou d'espaces : ValueError."""
        for libelle in ("", "  "):
            with self.subTest(libelle=libelle), self.assertRaises(ValueError):
                Abonnement(libelle, 10)

    def test_ajouter_contrat(self):
        """Le contrat est rattaché à l'abonnement."""
        ab, c = Abonnement("Mensuel", 50), Contrat()
        ab.ajouter_contrat(c)
        self.assertEqual(ab.contrats, [c])

    def test_ajouter_plusieurs_contrats(self):
        """Plusieurs clients peuvent avoir un contrat sur la même formule."""
        ab = Abonnement("Mensuel", 50)
        ab.ajouter_contrat(Contrat())
        ab.ajouter_contrat(Contrat())
        self.assertEqual(len(ab.contrats), 2)


if __name__ == "__main__":
    unittest.main()
