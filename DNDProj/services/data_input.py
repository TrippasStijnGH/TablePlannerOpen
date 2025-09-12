import sqlite3
import os



import settings

import Repo.inschrijvingen as Rinschrijvingen

import Classes.inschrijvingobjects as Iobs

import Repo.deelnemers as Rdeelnemers

import Repo.events as Revents

import Repo.DMs as RDMs

import pandas as pd

def leesInschrijvingenDoc():

    excel = settings.EXCELINSCHRIJVINGEN


    excel_file = pd.read_excel(excel)

    eventCode = os.path.splitext(os.path.basename(excel))[0]

    # kijkt of er al inschrijvingen zijn met deze eventId en verwijdert ze allemaal
    testEnverwijders(eventCode)

    # Go through the data and create new participants and registrations
    for _, row in excel_file.iterrows():

        createNewParticipant(row['FirstName'],row['LastName'],row['Email'],row['BirthDate'].strftime('%Y-%m-%d'),row['Postcode'])

        ParticId = Rdeelnemers.getParticipantIdByEmail(row['Email'])

        DM = row['DMPreference']

        if isinstance(DM, str) and DM != "No preference":
            voor, achter = DM.split(maxsplit=1)
            voor = voor.strip()
            achter = achter.strip()
            DMprefId = RDMs.getDMId(voor, achter)


        Rinschrijvingen.maakingschrijving(eventCode, ParticId, DMprefId)






def createNewParticipant(first_name, last_name, email, date_birth, postcode=None):

    if not Rdeelnemers.knownEmail(email):

        Rdeelnemers.maakNieuweSpeler(first_name,last_name,email,date_birth,postcode)







def naamgekend(naam):
    result = False
    if naam in Rdeelnemers.geefAllenamen():
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








