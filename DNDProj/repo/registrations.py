import sqlite3

import math

import settings

import classes.registration_objects as reg_obs

import repo.participants as Rdeelnemers

import pandas as pd

# Haalt inschrijvingen, gelinkt aan een eventid, uit de databank en returned ze als een lijst InschrijvingObjects
def return_registrations_event(event_id):

    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
        SELECT
        Registration.participant_id,
        Participant.first_name, 
        Participant.last_name,   
        DM.first_name, 
        DM.last_name
        FROM Registration
        JOIN DM ON Registration.pref_DM_id = DM.id
        JOIN Participant ON Registration.Participant_id = Participant.id
        WHERE Registration.event_id = ?
    """, (event_id,))

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    registration_objects = []

    for row in rows:

        participant_id = row[0]

        # Combine the third and fourth values to make "naam"
        name = row[1] + " " + row[2]

        # Combine the last two values to make "dm"
        DM = row[3] + " " + row[4]


        # Create Inschrijving object
        registration = reg_obs.Registration(participant_id, name, DM)

        # Append Inschrijving object to the list
        registration_objects.append(registration)


    return registration_objects


def return_registration_DP(event_id):
    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
            SELECT
            Participant.first_name, 
            Participant.last_name, 
            Participant.email,  
            DM.first_name, 
            DM.last_name,
            Notes
            FROM Registration
            JOIN DM ON Registration.pref_DM_id = DM.id
            JOIN Participant ON Registration.participant_id = Participant.id
            WHERE Registration.event_id = ?
        """, (event_id,))

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    registration_objects = []

    for row in rows:

        name = row[0] + " " + row[1]

        email = row[2]

        dm = row[3] + " " + row[4]

        notes = row[5]

        # Create Inschrijving object
        registration = reg_obs.RegistrationDP(name, email, dm, notes)

        # Append Inschrijving object to the list
        registration_objects.append(registration)

    return registration_objects


    # Print the array of values for each row



def make_registration(event_code, partic_id, dm_prefid=0, notes=None):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    # Insert data from the array into the table
    cursor.execute("INSERT INTO Registration (event_id, participant_id, pref_DM_id, notes) VALUES (?, ?, ?, ?)",
                   (event_code, partic_id, dm_prefid, notes))

    # Commit changes and close connection
    conn.commit()
    conn.close()



def find_participant_event(player_id, event_id):
    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
            SELECT participant_id
            FROM Registration
            WHERE participant_id = ? 
            AND event_id = ?
        """, (player_id, event_id))

    # Fetch all rows
    rows = cursor.fetchone()


    # Close the connection
    conn.close()

    return rows is not None

def delete_registration(event_id):


    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()


    delete_query = "DELETE FROM Inschrijving WHERE event_id = ?"


    cursor.execute(delete_query, (event_id,))


    conn.commit()



def find_registration(event_id):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    # Prepare the SELECT query
    select_query = f"SELECT 1 FROM Inschrijving WHERE EventId = ? LIMIT 1"

    # Execute the SELECT query
    cursor.execute(select_query, (event_id,))

    # Fetch one row
    result = cursor.fetchone()

    # Return True if a row exists, otherwise False
    return result is not None



















