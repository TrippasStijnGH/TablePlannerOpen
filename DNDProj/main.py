#!/usr/bin/env python3
import repo.events as r_events
import repo.registrations as r_registrations
import services.planning_display as s_plan
import services.data_input as s_input

import tkinter as tk
from tkinter import ttk


# Haalt alle toekomstige evenementen uit de database en steekt ze in een listbox
def populate_events():
    event_objects = r_events.make_upcoming_events()

    for item in event_objects:
        list_item = f"{item.name} {item.date}"
        events_listbox.insert(tk.END, list_item)

# Haalt alle inschrijvingen op met het gekozen eventId en steekt ze in registration_ text
def show_registrations(event):
    event_objects = r_events.make_upcoming_events()
    i = 0

    selected_index = events_listbox.curselection()
    if selected_index:
        event_input = selected_index[0]
        chosen_event_id = event_objects[event_input].id
        list_registrations = r_registrations.return_registration_DP(chosen_event_id)

        list_registrations.sort(key=lambda obj: obj.participant)


        registrations_text.delete(1.0, tk.END)  # Vorige tekst verwijderen
        for item in list_registrations:
            name = item.participant
            email = item.email
            DM = item.DM
            notes = item.notes if item.notes else ""
            registrations_text.insert(tk.END, f"Naam: {name}\nEmail: {email}\nGekozen DM: {DM}\nNotes: {notes}\n___\n \n")

def show_description():
    event_objects = r_events.make_upcoming_events()

    selected_index = events_listbox.curselection()
    if selected_index:
        event_input = selected_index[0]
        selected_event = event_objects[event_input].id
        description_text.delete(1.0, tk.END)
        description_text.insert(tk.END, s_plan.return_planning(selected_event))

def to_excel():
    event_objects = r_events.make_upcoming_events()

    selected_index = events_listbox.curselection()
    if selected_index:
        event_input = selected_index[0]
        selected_event = event_objects[event_input].id
        s_plan.to_excel(selected_event)



def upload_files():
    s_input.save_participants()


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

description_button = ttk.Button(button_frame, text="Upload Excel files", command=upload_files)
description_button.grid(row=0, column=0, pady=5)

button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=(70, 400), padx=(200,0))

description_button = ttk.Button(button_frame, text="Save to Excel", command=to_excel)
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

















