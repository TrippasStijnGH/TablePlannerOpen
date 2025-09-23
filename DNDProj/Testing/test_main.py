import tkinter as tk
from tkinter import ttk
import unittest
from unittest.mock import MagicMock
import repo.registrations as RepoInschrijvingen

def populate_events(events_listbox, EventObjects):
    events_listbox.delete(0, tk.END)
    for item in EventObjects:
        listItem = f"{item.name} {item.main} {item.date}"
        events_listbox.insert(tk.END, listItem)

def show_registrations(events_listbox, registrations_text, EventObjects, chosenEventId):
    registrations_text.delete(1.0, tk.END)  # Clear previous text
    lijstInschrijvingen = RepoInschrijvingen.return_registrations_event(chosenEventId)
    for item in lijstInschrijvingen:
        naam = item.name
        dm = item.DM
        remarks = item.remarks if item.remarks else ""
        registrations_text.insert(tk.END, f"Naam: {naam}\nGekozen DM: {dm}\nRemarks: {remarks}\n___\n \n")

class TestEventFunctions(unittest.TestCase):

    def setUp(self):
        self.events_listbox = tk.Listbox()
        self.registrations_text = tk.Text()

    def test_populate_events(self):
        EventObjects = [
            MagicMock(name="Event 1", main="Main 1", date="Date 1"),
            MagicMock(name="Event 2", main="Main 2", date="Date 2"),
        ]

        populate_events(self.events_listbox, EventObjects)

        self.assertEqual(self.events_listbox.size(), 2)

    def test_show_registrations(self):
        EventObjects = [
            MagicMock(name="Event1", id=1),
            MagicMock(name="Event2", id=2),
        ]

        chosenEventId = 1
        RepoInschrijvingen.return_registrations_event = MagicMock(return_value=[
            MagicMock(naam="John Doe", dm="DM1", remarks="Remark 1"),
            MagicMock(naam="Jane Doe", dm="DM2", remarks=None),
        ])

        show_registrations(self.events_listbox, self.registrations_text, EventObjects, chosenEventId)

        expected_text = "Naam: John Doe\nGekozen DM: DM1\nRemarks: Remark 1\n___\n \nNaam: Jane Doe\nGekozen DM: DM2\nRemarks: \n___\n \n"

        self.assertEqual(self.registrations_text.get(1.0, tk.END).strip(), expected_text.strip())


if __name__ == '__main__':
    unittest.main()