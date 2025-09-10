import unittest
import sqlite3
import settings  # Make sure settings.DATABASE points to your SQLite database
import Repo.events as repoevents

class TestMakeUpcomingEvents(unittest.TestCase):

    def test_maakUpcomingEvents(self):
        # Call the function being tested
        events = repoevents.maakUpcomingEvents()

        # Assert that the result is not empty
        self.assertTrue(events)

        # Assert that the length of the result matches the number of rows in the test database
        self.assertEqual(len(events), 2)

        # Assert that the retrieved event has the expected attributes
        event = events[0]
        self.assertEqual(event.name, "Storm King's Thunder session 16")
        self.assertEqual(event.date, "17/04/2024")
        self.assertIsNone(event.plaats)
        self.assertEqual(event.main, 'Main')

if __name__ == '__main__':
    unittest.main()