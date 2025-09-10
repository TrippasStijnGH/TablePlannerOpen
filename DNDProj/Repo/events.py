import sqlite3

import settings

import Classes.eventobjects as Eobs

from datetime import datetime





# Haalt alle events uit de databank en returned ze als een lijst EventObjects
def maakUpcomingEvents():

    events = []

    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("SELECT eventId, NaamEvent, Datum, Plaats, Main  FROM Event")


    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    for row in rows:

        event = Eobs.Event(*row)
        events.append(event)

    return events







def geefDeelnemers ():
    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("SELECT * FROM Deelnemer")

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows
    # Connect to the database



def checkPersoon (items):

    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT Voornaam,Achternaam FROM Deelnemer")

    Deelnemers = cursor.fetchall()

    for item in items:
        if item in Deelnemers:
            print(item)

    conn.close()

def voegEventToe (info):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    # Insert data from the array into the table
    cursor.execute(
        "INSERT INTO Event (EventId, NaamEvent, Datum, Plaats, Main) VALUES (?, ?, ?, ?, ?)",
        info)

    # Commit changes and close connection
    conn.commit()
    conn.close()



def voegPersonenToe ():


    output = []

    # Connect to the SQLite database
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    # Function to retrieve rows from the source table
    cursor.execute("SELECT Voornaam,Achternaam,PersoonId FROM Inschrijvingen")
    Inschrijvingen = cursor.fetchall()

    cursor.execute("SELECT PersoonId FROM Deelnemer")
    Deelnemers = cursor.fetchall()



    manipulated_rows = []
    for row in Inschrijvingen:
        if row[3] in Deelnemers:
            output.append(row)



    #
    #     manipulated_row = (row[0], row[1], row[2])  # Example manipulation
    #     manipulated_rows.append(manipulated_row)
    #
    #
    # cursor.executemany("INSERT INTO destination_table (column1, column2, column3) VALUES (?, ?, ?)", data)
    # conn.commit()


    conn.close()









