import sqlite3

import settings

import pandas as pd

import classes.table_objects as t_obs


def make_tables(event_id):

    excel = settings.EXCEL_AVAILABLE_TABLES

    excel_file = pd.read_excel(excel)

    table_headers = ["Table","Available"]
    tables = []
    table_objects = []



    for index, row in excel_file.iterrows():
        values_table_excel = [row[header] for header in table_headers]
        tables.append(values_table_excel)




    for row in tables:
        if row[1]:
            tafel = t_obs.Tafel(event_id, row[0] - 1)
            table_objects.append(tafel)

    table_objects = sorted(table_objects, key=lambda tobj: tobj.max_number, reverse=True)

    i = 1
    for tafel in table_objects:
        tafel.table_number = i
        i += 1




    return table_objects





















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






