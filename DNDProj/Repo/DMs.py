import sqlite3

import settings

import Classes.DMobjects as DMobs
import Classes.DMgroepobjects as DMgroepobs

import pandas as pd

def geefDMs():

    conn = sqlite3.connect(settings.DATABASE)

    cursor = conn.cursor()

    # Select all rows from the table
    cursor.execute("""
            SELECT DM.* 
            FROM DM
        """)

    # Fetch all rows
    rows = cursor.fetchall()


    # Close the connection
    conn.close()


    DM_objects = maakDMobjects(rows)

    return DM_objects

def geefSomeDms(lijst):

    DMrows = []
    for DMnaam in lijst:
        voor, achter = DMnaam.split(maxsplit=1)
        conn = sqlite3.connect(settings.DATABASE)

        cursor = conn.cursor()

        # Select all rows from the table
        cursor.execute("""
                    SELECT DM.* 
                    FROM DM
                    WHERE Voornaam = ?
                    AND Achternaam = ?
                """, (voor,achter))

        # Fetch all rows
        result = cursor.fetchone()
        DMrows.append(result)

        # Close the connection
        conn.close()

    DM_objects = maakDMobjects(DMrows)



    return DM_objects




def geefDMnamen():
    result = []
    for obj in geefDMs():
        result.append(obj.naam)
    return result

def maakNieuweDM(info):

    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()



    # Insert data from the array into the table
    cursor.execute("INSERT INTO DM (PersoonId, Voornaam, Achternaam, Email, Geboortedatum, Postcode, Maxspelers ) VALUES (?, ?, ?, ?, ?, ?, ?)", info)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def getDMId(voor, achter):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT PersoonId 
        FROM DM
        WHERE Voornaam = ? AND Achternaam = ?;
    """, (voor, achter))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def maakDMobject(row):
    naam = row[1] + " " + row[2]

    # Create DM object
    DM = DMobs.DM(row[0], naam, row[6])

    return DM

def maakDMobjects(lijst):
    DMobjects = []

    for row in lijst:
        if not row[0] == 0:
            DMobjects.append(maakDMobject(row))
    return DMobjects






def geefBeschikbareDms():
    excel = settings.EXCELBESCHIKBAREDMS

    excel_file = pd.read_excel(excel)

    BDMHeaders = ["Beschikbare DM's"]
    BeschikbareDMlijst = []


    for index, row in excel_file.iterrows():
        valuesDM = [row[header] for header in BDMHeaders]
        BeschikbareDMlijst.append(valuesDM[0])

    return BeschikbareDMlijst


def maakLookupDMgroep(DMgroepen):
    lookupDMgroepen = {}
    for DMgroep in DMgroepen:
        lookupDMgroepen[DMgroep.naam] = DMgroep

    return lookupDMgroepen

def maakDMgroepen():
    beschikbareDMs = geefBeschikbareDms()

    DMobjecten = geefSomeDms(beschikbareDMs)
    DMgroepen = []
    for dm in DMobjecten:
        DMgroep = DMgroepobs.DMgroep(dm.id,dm.naam,dm.maxspelers)
        DMgroepen.append(DMgroep)

    lookup = maakLookupDMgroep(DMgroepen)
    return ([DMgroepen,lookup])








