import sqlite3

import math

import settings

import Classes.inschrijvingobjects as Iobs

import Repo.deelnemers as Rdeelnemers

import pandas as pd

# Haalt inschrijvingen, gelinkt aan een eventid, uit de databank en returned ze als een lijst InschrijvingObjects
def geefInschrijvingenEvent (eventid):

    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
        SELECT Inschrijving.*, DM.voornaam, DM.achternaam 
        FROM Inschrijving
        JOIN DM ON Inschrijving.DMpref = DM.PersoonId
        WHERE Inschrijving.EventId = ?
    """,(eventid,))

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    inschrijving_objects = []

    for row in rows:

        # Combine the third and fourth values to make "naam"
        naam = row[2] + " " + row[3]

        # Combine the last two values to make "dm"
        dm = row[-2] + " " + row[-1]


        # Create Inschrijving object
        inschrijving = Iobs.Inschrijving(row[0], row[1], naam, row[4], dm, row[6])

        # Append Inschrijving object to the list
        inschrijving_objects.append(inschrijving)


    return inschrijving_objects












    # Print the array of values for each row



def maakingschrijving(row):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    # Insert data from the array into the table
    cursor.execute("INSERT INTO Inschrijving (InschrijvingId, PersoonId, Voornaam, Achternaam, EventId, DMpref, Remarks, Datum, VorigeDM) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)", row)

    # Commit changes and close connection
    conn.commit()
    conn.close()



def zoekInschrijving(id, code):
    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
            SELECT PersoonId
            FROM Inschrijving
            WHERE PersoonId = ? 
            AND EventId = ?
        """, (id, code))

    # Fetch all rows
    rows = cursor.fetchone()


    # Close the connection
    conn.close()

    return rows is not None

def verwijderInschrijvingen(eventId):


    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()


    delete_query = "DELETE FROM Inschrijving WHERE eventId = ?"


    cursor.execute(delete_query, (eventId,))


    conn.commit()



def zoekInschrijving(eventId):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    # Prepare the SELECT query
    select_query = f"SELECT 1 FROM Inschrijving WHERE EventId = ? LIMIT 1"

    # Execute the SELECT query
    cursor.execute(select_query, (eventId,))

    # Fetch one row
    result = cursor.fetchone()

    # Return True if a row exists, otherwise False
    return result is not None



















