import settings
import sqlite3

import classes.participant_objects as p_obs

def return_all_participants():
    participant_objects = []

    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
                    SELECT Participant.* 
                    FROM Participant

                """)

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    for row in rows:
        # Combine the third and fourth values to make "naam"
        naam = row[1] + " " + row[2]

        # Create Inschrijving object
        deelnemer = p_obs.Participant(row[0], naam, row[2], row[3], row[4])

        # Append Inschrijving object to the list
        participant_objects.append(deelnemer)

    return participant_objects


def known_email(email):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 
        FROM Deelnemer 
        WHERE Email = ? 
        LIMIT 1;
    """, (email,))

    result = cursor.fetchone()
    conn.close()

    return result is not None




def return_participants(id_list):
    participants = []

    participant_objects = []

    for id in id_list:
        conn = sqlite3.connect(settings.DATABASE)

        cursor = conn.cursor()

        # Select all rows from the table
        cursor.execute("""
                SELECT Participant.* 
                FROM Participant

                WHERE Participant.id = ?
            """, (id,))

        # Fetch all rows
        rows = cursor.fetchall()

        # Close the connection
        conn.close()

        participants.append(rows[0])

    for row in participants:
        # Combine the third and fourth values to make "naam"
        name = row[1] + " " + row[2]

        # Create Inschrijving object
        participant_obj = p_obs.Participant(row[0], name, row[2], row[3], row[4])

        # Append Inschrijving object to the list
        participant_objects.append(participant_obj)

    return participant_objects



def return_names(partic_obj_list):
    names = []
    for participant in partic_obj_list:
        names.append(participant.name)
    return names

def return_all_names():
    names = []
    for particpant in return_all_participants():
        names.append(particpant.name)
    return names

def return_all_emails():
    emails = []
    for deelnemer in return_all_participants():
        emails.append(deelnemer.email)
    return emails

def make_new_participant(first_name, last_name, email, birth_day, postcode):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()



    # Insert data from the array into the table
    cursor.execute("INSERT INTO Deelnemer (first_name, last_name, email, birth_date, postcode ) VALUES (?, ?, ?, ?, ?)",
                   (first_name, last_name, email, birth_day, postcode)
                   )


    # Commit changes and close connection
    conn.commit()
    conn.close()

def get_participant_id(first_name, last_name):


    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
                        SELECT id 
                        FROM Participant
                        WHERE first_name = ? AND last_name = ?;

                    """, (first_name, last_name))

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows[0][0]

def get_participant_id_by_email(email):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id 
        FROM Participant
        WHERE email = ?;
    """, (email,))  # Note the comma after email to make it a tuple

    rows = cursor.fetchall()
    conn.close()

    if rows:  # Check if any rows were found
        return rows[0][0]
    else:
        return None
