import unittest
import sqlite3
import settings
import Classes.inschrijvingobjects as Iobs
from Repo.inschrijvingen import geefInschrijvingenEvent  # Replace 'your_module' with the actual module name

class TestGeefInschrijvingenEvent(unittest.TestCase):


    def test_geefInschrijvingenEvent(self):
        # Call the function being tested
        inschrijvingen = geefInschrijvingenEvent("E1")  # Assuming eventid 1 exists in the test data

        # Assert that the result is not empty
        self.assertTrue(inschrijvingen)

        # Assert that the length of the result matches the number of rows in the test database
        self.assertEqual(len(inschrijvingen), 3)

        # Assert that the retrieved Inschrijving object has the expected attributes
        inschrijving = inschrijvingen[0]
        self.assertEqual(inschrijving.id, "I1")
        self.assertEqual(inschrijving.naam, "Stijn Trippas")
        self.assertEqual(inschrijving.dm, "Sigurd Joostens")
        self.assertEqual(inschrijving.remarks, "Graag met Shriya Bajpai")


if __name__ == '__main__':
    unittest.main()