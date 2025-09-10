import sqlite3

import settings

import pandas as pd

import Classes.tafelobjects as Tobs


def maakTafels(eventId):

    excel = settings.EXCELBESCHIKBARETAFELS

    excel_file = pd.read_excel(excel)

    tafelHeaders = ["Tafel","Beschikbaarheid"]
    tafels = []
    tafelobjects = []



    for index, row in excel_file.iterrows():
        valuesTafelExcel = [row[header] for header in tafelHeaders]
        tafels.append(valuesTafelExcel)




    for row in tafels:
        if row[1]:
            tafel = Tobs.Tafel(eventId,row[0]-1)
            tafelobjects.append(tafel)

    tafelobjects = sorted(tafelobjects, key=lambda tobj: tobj.maxAantal, reverse=True)

    i = 1
    for tafel in tafelobjects:
        tafel.tafelnummer = i
        i += 1




    return (tafelobjects)





















# Haalt inschrijvingen, gelinkt aan een eventid, uit de databank en returned ze als een lijst InschrijvingObjects
# def geeftafelsEvent (eventid):
#
#     conn = sqlite3.connect(settings.DATABASE)
#
#     cursor = conn.cursor()
#
#     # Select all rows from the table
#     cursor.execute("""
#         SELECT EventId, MaxSpelerAantal, Tafelnummer
#         FROM tafel
#         WHERE tafel.EventId = ?
#     """,(eventid,))
#
#     # Fetch all rows
#     rows = cursor.fetchall()
#
#     # Close the connection
#     conn.close()
#
#     tafel_objects = []
#
#     for row in rows:
#
#
#         # Create Inschrijving object
#         tafel = Tobs.Tafel(row[0], row[1], row[2])
#
#         # Append Inschrijving object to the list
#         tafel_objects.append(tafel)
#
#
#     return tafel_objects






