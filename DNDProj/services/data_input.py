import sqlite3
import os



import settings

import repo.registrations as Rinschrijvingen

import classes.registration_objects as Iobs

import repo.participants as Rdeelnemers

import repo.events as Revents

import repo.DMs as RDMs

import pandas as pd

def leesInschrijvingenDoc():

    excel = settings.EXCEL_REGISTRATIONS


    excel_file = pd.read_excel(excel)

    eventCode = os.path.splitext(os.path.basename(excel))[0]

    # kijkt of er al inschrijvingen zijn met deze eventId en verwijdert ze allemaal
    testEnverwijders(eventCode)

    # Go through the data and create new participants and registrations
    for _, row in excel_file.iterrows():

        createNewParticipant(row['FirstName'],row['LastName'],row['Email'],row['BirthDate'].strftime('%Y-%m-%d'),row['Postcode'])

        ParticId = Rdeelnemers.get_participant_id_by_email(row['Email'])

        DM = row['DMPreference']

        DMprefId = 0

        Notes = row['Notes']

        if isinstance(DM, str) and DM != "No preference":
            voor, achter = DM.split(maxsplit=1)
            voor = voor.strip()
            achter = achter.strip()
            DMprefId = RDMs.get_DM_id(voor, achter)


        Rinschrijvingen.maakingschrijving(eventCode, ParticId, DMprefId, Notes)






def createNewParticipant(first_name, last_name, email, date_birth, postcode=None):

    if not Rdeelnemers.known_email(email):

        Rdeelnemers.make_new_participant(first_name, last_name, email, date_birth, postcode)







def naamgekend(naam):
    result = False
    if naam in Rdeelnemers.return_all_names():
        return True
    return result









### Inschrijving functies

def inschrijvinggekend(id,code):
    return Rinschrijvingen.zoekInschrijving(id,code)



def filterToString(value):
    terug = " "
    if not isinstance(value,float):
        terug = value
    return terug



def testEnverwijders(eventId):
     Rinschrijvingen.verwijderInschrijvingen(eventId)








