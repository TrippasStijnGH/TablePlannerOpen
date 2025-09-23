import sqlite3

import settings

import classes.event_objects as E_obs

from datetime import datetime





# Haalt alle events uit de databank en returned ze als een lijst EventObjects
def make_upcoming_events():

    events = []

    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("SELECT id, event_name, event_date, location  FROM Event")


    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    for row in rows:

        event = E_obs.Event(*row)
        events.append(event)

    return events







def return_participants():
    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("SELECT * FROM Participant")

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows
    # Connect to the database



def check_participant(items):

    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT first_name, last_name FROM Participant")

    participants = cursor.fetchall()

    for item in items:
        if item in participants:
            print(item)

    conn.close()

def add_event(info):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    # Insert data from the array into the table
    cursor.execute(
        "INSERT INTO Event (id, event_name, event_date, location) VALUES (?, ?, ?, ?)",
        info)

    # Commit changes and close connection
    conn.commit()
    conn.close()



def add_participants ():


    output = []

    # Connect to the SQLite database
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    # Function to retrieve rows from the source table
    cursor.execute("SELECT first_name ,last_name ,id FROM Registration")
    registrations = cursor.fetchall()

    cursor.execute("SELECT id FROM Participant")
    participants = cursor.fetchall()



    manipulated_rows = []
    for row in registrations:
        if row[3] in participants:
            output.append(row)




    #
    #     manipulated_row = (row[0], row[1], row[2])  # Example manipulation
    #     manipulated_rows.append(manipulated_row)
    #
    #
    # cursor.executemany("INSERT INTO destination_table (column1, column2, column3) VALUES (?, ?, ?)", data)
    # conn.commit()


    conn.close()









