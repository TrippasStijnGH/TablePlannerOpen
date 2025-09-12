import settings
import sqlite3

import Classes.deelnemerobjects as Dobs

def geefAlleSpelers():
    deelnemer_objects = []

    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
                    SELECT Deelnemer.* 
                    FROM Deelnemer

                """)

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    for row in rows:
        # Combine the third and fourth values to make "naam"
        naam = row[1] + " " + row[2]

        # Create Inschrijving object
        deelnemer = Dobs.Deelnemer(row[0], naam, row[2], row[3], row[4])

        # Append Inschrijving object to the list
        deelnemer_objects.append(deelnemer)

    return deelnemer_objects


def knownEmail(email):
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




def geefSpelers(idlijst):
    lijstmensen = []

    deelnemer_objects = []

    for id in idlijst:
        conn = sqlite3.connect(settings.DATABASE)

        cursor = conn.cursor()

        # Select all rows from the table
        cursor.execute("""
                SELECT Deelnemer.* 
                FROM Deelnemer

                WHERE Deelnemer.PersoonId = ?
            """, (id,))

        # Fetch all rows
        rows = cursor.fetchall()

        # Close the connection
        conn.close()

        lijstmensen.append(rows[0])

    for row in lijstmensen:
        # Combine the third and fourth values to make "naam"
        naam = row[1] + " " + row[2]

        # Create Inschrijving object
        deelnemer = Dobs.Deelnemer(row[0], naam, row[2], row[3], row[4])

        # Append Inschrijving object to the list
        deelnemer_objects.append(deelnemer)

    return deelnemer_objects



def geefnamen(lijst):
    namen = []
    for deelnemer in lijst:
        namen.append(deelnemer.naam)
    return namen

def geefAllenamen():
    namen = []
    for deelnemer in geefAlleSpelers():
        namen.append(deelnemer.naam)
    return namen

def returnAllEmails():
    emails = []
    for deelnemer in geefAlleSpelers():
        emails.append(deelnemer.email)
    return emails

def maakNieuweSpeler(FirstName,LastName,Email,BirthDay,Postcode):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()



    # Insert data from the array into the table
    cursor.execute("INSERT INTO Deelnemer (Voornaam, Achternaam, Email, Geboortedatum, Postcode ) VALUES (?, ?, ?, ?, ?)",
                   (FirstName,LastName,Email,BirthDay,Postcode)
                   )


    # Commit changes and close connection
    conn.commit()
    conn.close()

def getDeelnemerId(voor, achter):


    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
                        SELECT PersoonId 
                        FROM Deelnemer
                        WHERE Voornaam = ? AND Achternaam = ?;

                    """,(voor,achter))

    # Fetch all rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    return rows[0][0]

def getParticipantIdByEmail(email):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT PersoonId 
        FROM Deelnemer
        WHERE Email = ?;
    """, (email,))  # Note the comma after email to make it a tuple

    rows = cursor.fetchall()
    conn.close()

    if rows:  # Check if any rows were found
        return rows[0][0]
    else:
        return None
