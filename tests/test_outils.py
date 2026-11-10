"""Tests unitaires de outils (date et heure en France).

@author: MUSHIMIYIMANA MOISE
"""
import unittest
from datetime import date, datetime

from dreampark.outils import maintenant, aujourd_hui


class TestOutils(unittest.TestCase):
    def test_maintenant_est_un_datetime(self):
        """maintenant() retourne un datetime."""
        self.assertIsInstance(maintenant(), datetime)

    def test_maintenant_sans_fuseau(self):
        """maintenant() est 'naïf' : pas d'information de fuseau."""
        self.assertIsNone(maintenant().tzinfo)

    def test_maintenant_comparable_a_un_datetime_naif(self):
        """Comparable à un datetime construit à la main (pas de TypeError)."""
        self.assertGreater(maintenant(), datetime(2020, 1, 1))

    def test_aujourd_hui_est_une_date(self):
        """aujourd_hui() retourne une date (pas un datetime)."""
        self.assertIsInstance(aujourd_hui(), date)
        self.assertNotIsInstance(aujourd_hui(), datetime)

    def test_aujourd_hui_coherent_avec_maintenant(self):
        """aujourd_hui() correspond à la date de maintenant()."""
        self.assertEqual(aujourd_hui(), maintenant().date())


if __name__ == "__main__":
    unittest.main()
