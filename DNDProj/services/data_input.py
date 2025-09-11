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

    eventCode = os.path.splitext(excel)[0]


    for _, row in excel_file.iterrows():

        createNewParticipant(row['FirstName'],row['LastName'],row['email'],row['BirthDate'].strftime('%Y-%m-%d'),row['Postcode'])

        ParticId = Rdeelnemers.getDeelnemerId(row['email'])

        DM = row['DMPreference']

        if isinstance(DM, str) and DM != "No preference":
            voor, achter = DM.split(maxsplit=1)

            DMprefId = RDMs.getDMId(voor, achter)

        inschrijvinginfo = [eventCode, ParticId, inschrijving[2], inschrijving[3], DMprefId]

        Rinschrijvingen.maakingschrijving(eventCode, ParticId, DMprefId)

    #kijkt of er al inschrijvingen zijn met deze eventId en verwijdert ze allemaal
    testEnverwijders(eventCode)










def createNewParticipant(first_name, last_name, email, date_birth, postcode=None):

    if not knownEmail(email):

        Rdeelnemers.maakNieuweSpeler(first_name,last_name,email,date_birth,postcode)





def knownEmail(email):
    result = False
    if email in Rdeelnemers.returnAllEmails():
        return True
    return result

def naamgekend(naam):
    result = False
    if naam in Rdeelnemers.geefAllenamen():
        return True
    return result





def maaknieuweDM(naam):
    if naam.find(" ") == -1:

        voor = naam
        achter = "x"
    else:

        voor, achter = naam.split(maxsplit=1)

    fullname = voor + " " + achter

    if not DMgekend(fullname):
        info = ["",voor,achter,"","","", 7]
        info[0] = len(RDMs.geefDMs()) + 1

        RDMs.maakNieuweDM(info)




def DMgekend(naam):

    result = False
    if naam in RDMs.geefDMnamen():

        return True
    return result

### PreviousDM functios



### Inschrijving functies

def inschrijvinggekend(id,code):
    return Rinschrijvingen.zoekInschrijving(id,code)

def maakNewInschrijving(info):
    if inschrijvinggekend():
        print("hi")


def filterToString(value):
    terug = " "
    if not isinstance(value,float):
        terug = value
    return terug

def vorigeDM(mainwaarde,repeatwaarde,repeat):
    if repeat == "ja":
        return filterToString(mainwaarde)
    else:
        return filterToString(repeatwaarde)

def testEnverwijders(eventId):
     Rinschrijvingen.verwijderInschrijvingen(id)








