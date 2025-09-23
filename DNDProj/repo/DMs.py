import sqlite3

import settings

import classes.DM_objects as DMobs
import classes.DMgroup_objects as DMgroepobs

import pandas as pd

def return_all_DMs():

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


    DM_objects = make_DM_objects(rows)

    return DM_objects

def return_some_DMs(lijst):

    DMrows = []
    for DMnaam in lijst:
        voor, achter = DMnaam.split(maxsplit=1)
        conn = sqlite3.connect(settings.DATABASE)

        cursor = conn.cursor()

        # Select all rows from the table
        cursor.execute("""
                    SELECT DM.* 
                    FROM DM
                    WHERE first_name = ?
                    AND last_name = ?
                """, (voor, achter))

        # Fetch all rows
        result = cursor.fetchone()
        DMrows.append(result)

        # Close the connection
        conn.close()

    DM_objects = make_DM_objects(DMrows)



    return DM_objects




def return_DM_names():
    result = []
    for obj in return_all_DMs():
        result.append(obj.name)
    return result

def make_new_DM(info):

    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()



    # Insert data from the array into the table
    cursor.execute("INSERT INTO DM (id, first_name, last_name, email, birth_date, postcode, max_players ) VALUES (?, ?, ?, ?, ?, ?, ?)", info)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def get_DM_id(first_name, last_name):
    conn = sqlite3.connect(settings.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id 
        FROM DM
        WHERE first_name = ? AND last_name = ?;
    """, (first_name, last_name))

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def make_DM_object(row):
    naam = row[1] + " " + row[2]

    # Create DM object
    DM = DMobs.DM(row[0], naam, row[6])

    return DM

def make_DM_objects(lijst):
    DMobjects = []

    for row in lijst:
        if not row[0] == 0:
            DMobjects.append(make_DM_object(row))
    return DMobjects






def geefBeschikbareDms():
    excel = settings.EXCEL_AVAILABLE_DMS

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
        lookupDMgroepen[DMgroep.name] = DMgroep

    return lookupDMgroepen

def maakDMgroepen():
    beschikbareDMs = geefBeschikbareDms()

    DMobjecten = return_some_DMs(beschikbareDMs)
    DMgroepen = []
    for dm in DMobjecten:
        DMgroep = DMgroepobs.DMgroup(dm.id, dm.name, dm.max_players)
        DMgroepen.append(DMgroep)

    lookup = maakLookupDMgroep(DMgroepen)
    return ([DMgroepen,lookup])








