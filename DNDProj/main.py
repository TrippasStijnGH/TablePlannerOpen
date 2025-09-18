#!/usr/bin/env python3
import Repo.events as REvents
import Repo.inschrijvingen as RepoInschrijvingen
import services.Tafelplanner as Tplanner
import services.data_input as DataInput

import tkinter as tk
from tkinter import ttk


# Haalt alle toekomstige evenementen uit de database en steekt ze in een listbox
def populate_events():
    EventObjects = REvents.maakUpcomingEvents()

    for item in EventObjects:
        listItem = f"{item.name} {item.date}"
        events_listbox.insert(tk.END, listItem)

# Haalt alle inschrijvingen op met het gekozen eventId en steekt ze in registration_ text
def show_registrations(event):
    EventObjects = REvents.maakUpcomingEvents()
    i = 0

    selected_index = events_listbox.curselection()
    if selected_index:
        eventInput = selected_index[0]
        chosenEventId = EventObjects[eventInput].id
        lijstInschrijvingen = RepoInschrijvingen.returnRegistrationDP(chosenEventId)

        lijstInschrijvingen.sort(key=lambda obj: obj.participant)


        registrations_text.delete(1.0, tk.END)  # Vorige tekst verwijderen
        for item in lijstInschrijvingen:
            naam = item.participant
            email = item.email
            dm = item.dm
            notes = item.notes if item.notes else ""
            registrations_text.insert(tk.END, f"Naam: {naam}\nEmail: {email}\nGekozen DM: {dm}\nNotes: {notes}\n___\n \n")

def show_description():
    EventObjects = REvents.maakUpcomingEvents()

    selected_index = events_listbox.curselection()
    if selected_index:
        input = selected_index[0]
        selected_event = EventObjects[input].id
        description_text.delete(1.0, tk.END)
        description_text.insert(tk.END, Tplanner.plantafelsAlfa(selected_event))

def naarExcel():
    EventObjects = REvents.maakUpcomingEvents()

    selected_index = events_listbox.curselection()
    if selected_index:
        input = selected_index[0]
        selected_event = EventObjects[input].id
        Tplanner.toExcel(selected_event)




def UploadEFiles():
    DataInput.leesInschrijvingenDoc()


root = tk.Tk()
root.title("Event Registration Viewer")

root.geometry("1200x800")  # Set a wider initial size

events_frame = ttk.Frame(root)
events_frame.grid(row=0, column=0, padx=10, pady=10, sticky="n")

events_label = ttk.Label(events_frame, text="Upcoming Events:")
events_label.grid(row=0, column=0, sticky="w")

events_listbox = tk.Listbox(events_frame, width=50, height=10)
events_listbox.grid(row=1, column=0, sticky="w")

events_scrollbar = ttk.Scrollbar(events_frame, orient="vertical", command=events_listbox.yview)
events_scrollbar.grid(row=1, column=1, sticky="ns")

events_listbox.config(yscrollcommand=events_scrollbar.set)

events_listbox.bind("<<ListboxSelect>>", show_registrations)

button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=(70,400))

description_button = ttk.Button(button_frame, text="Maak planning", command=show_description)
description_button.grid(row=0, column=0, pady=5)

button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=(70, 400), padx=(10,240))

description_button = ttk.Button(button_frame, text="Upload Excel files", command=UploadEFiles)
description_button.grid(row=0, column=0, pady=5)

button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=(70, 400), padx=(200,0))

description_button = ttk.Button(button_frame, text="Save to Excel", command=naarExcel)
description_button.grid(row=0, column=0, pady=5)

registrations_frame = ttk.Frame(root)
registrations_frame.grid(row=0, column=1, padx=10, pady=10)

registrations_label = ttk.Label(registrations_frame, text="Registrations:")
registrations_label.grid(row=0, column=0, sticky="w")

registrations_text = tk.Text(registrations_frame, width=50, height=45)
registrations_text.grid(row=1, column=0, sticky="w")

description_label = ttk.Label(registrations_frame, text="Voorgestelde planning:")
description_label.grid(row=0, column=1, padx=20, sticky="w")

description_text = tk.Text(registrations_frame, width=50, height=45)
description_text.grid(row=1, column=1, padx=20, sticky="w")

populate_events()

root.mainloop()



#
# planning = Tplanner.plantafels("E1")
#
# for tafel in planning:
#     for item in tafel:
#         print(item)
#     print("___")

















