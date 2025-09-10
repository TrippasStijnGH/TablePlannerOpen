import sqlite3



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

    EventHeaders = ['SessionCode', 'MainSessionDate', 'RepeatSessionDate']
    DeelnemerHeaders = ['NameNaam_First', 'NameNaam_Last', 'Email', 'DateOfBirth', 'PostcodePostalCodeOfDomicile']
    InschrijvingHeaders = ['SessionCode','NameNaam_First', 'NameNaam_Last', 'MainSession_ThisSessionIWantToSitAtTheTableOf', 'RepeatSession', 'MainSession_MyPreviousDMWas', 'AnyRemarks','Entry_DateUpdated']
    DMHeaders = ["MainSession_ThisSessionIWantToSitAtTheTableOf","RepeatSession_ThisSessionIWantToSitAtTheTableOf","RepeatSession"]
    PreviousDMHeaders = ["MainSession_MyPreviousDMWas","RepeatSession_MyPreviousDMWas","RepeatSession"]


    # raw info extractie voor alle domein objecten
    lijstDeelnemers = []
    lijstInschrijvingen = []
    lijstDMs = []
    lijstPreviousDMs = []

    for index, row in excel_file.iterrows():

        valuesDeelname = [row[header] for header in DeelnemerHeaders]
        valuesInschrijving = [row[header] for header in InschrijvingHeaders]
        valuesInschrijving = [row.iloc[0]] + valuesInschrijving
        valuesDM = [row[header] for header in DMHeaders]
        valuesPreviousDM = [row[header] for header in PreviousDMHeaders]

        lijstDeelnemers.append(valuesDeelname)
        lijstInschrijvingen.append(valuesInschrijving)
        lijstDMs.append(valuesDM)
        lijstPreviousDMs.append(valuesPreviousDM)




    #Data groomen voor event extractie


    eventInfo = [excel_file[header][1] for header in EventHeaders]

    rawEventNaam = excel_file.columns[0]

    eventNaam = rawEventNaam[6:rawEventNaam.index("_")]

    maakNewEvent(eventNaam, eventInfo)

    #kijkt of er al inschrijvingen zijn met deze eventId en verwijdert ze allemaal
    testEnverwijders(eventInfo[0])


    #Data groomen voor deelnemer extractie
    modList = []

    for info in lijstDeelnemers: #zie raw info extractie voor alle domein objecten
        naam = info[0] + " " + info[1]
        if not isinstance(info[2], str):
            info[2] = " "

        Bday = info[3].strftime('%Y-%m-%d')

        if not isinstance(info[4], str):
            info[4] = " "

        modList.append(info[:3] + [Bday] + [info[4]])

    for info in modList:
        maakNieweDeelnemer(info)

    ###Data groomen voor DM extractie
    # lijstDMs = excel_file["MainSession_ThisSessionIWantToSitAtTheTableOf"].tolist()


    unifiedlijstDMs = DMsnaar1lijst(lijstDMs)

    modListDMs = []



    for i in range(len(unifiedlijstDMs)):
        if isinstance(unifiedlijstDMs[i], str) and unifiedlijstDMs[i] != "No preference":
            modvalue = unifiedlijstDMs[i][:unifiedlijstDMs[i].find(" -")]
            modListDMs.append(modvalue)

    DMs = list(set(modListDMs))
    for dm in DMs:
        maaknieuweDM(dm)

    #Data groomen voor PreviousDM extractie

    unifiedPreviousDMlijst = DMsnaar1lijst(lijstPreviousDMs)


    #Data groomen voor Inschrijving extractie


    for inschrijving, DM, PDM in zip(lijstInschrijvingen, unifiedlijstDMs, unifiedPreviousDMlijst):

        id = Rdeelnemers.getDeelnemerId(inschrijving[2],inschrijving[3])
        code = " "
        DMprefmod = 0
        iremarks = filterToString(inschrijving[7])
        idatum = inschrijving[8].strftime("%Y-%m-%d %H:%M:%S")
        vorigeDM = PDM




        #EventCode
        if inschrijving[5] == "Ja":
            code = inschrijving[1]+"R"
        else:
            code = inschrijving[1]+"M"


        #DMprefId

        if isinstance(DM, str) and DM != "No preference":
            DMpref = DM[:DM.find(" -")]

            voor = " "
            achter = " "
            if DMpref.find(" ") == -1:

                voor = DMpref
                achter = "x"
            else:

                voor, achter = DMpref.split(maxsplit=1)

            DMprefmod = RDMs.getDMId(voor,achter)

        inschrijvinginfo = [inschrijving[0],id,inschrijving[2],inschrijving[3],code,DMprefmod,iremarks ,idatum,vorigeDM]




        Rinschrijvingen.maakingschrijving(inschrijvinginfo)






### Event extracting fucnties
def maakNewEvent(naam, info):
    if not eventgekend(info[0]):
        main = [info[0]+"M", naam, info[1].strftime('%Y-%m-%d'), " ", "Main"]
        repeat = [info[0]+"R", naam, info[2].strftime('%Y-%m-%d'), " ", "Repeat"]
        Revents.voegEventToe(main)
        Revents.voegEventToe(repeat)




def eventgekend(code):
    events = Revents.maakUpcomingEvents()
    codes = [event.id for event in events]
    result = False
    if code + 'M' in codes: result = True
    return result



### Deelnemer extracting functies
def maakNieweDeelnemer(deelnemerinfo):


    if not naamgekend(deelnemerinfo[0] + " " + deelnemerinfo[1]):

        newId = len(Rdeelnemers.geefAlleSpelers()) + 1
        newinfo = [newId] + deelnemerinfo




        Rdeelnemers.maakNieuweSpeler(newinfo)


def naamgekend(naam):
    result = False
    if naam in Rdeelnemers.geefAllenamen():
        return True
    return result

### DM extractie functie

def DMsnaar1lijst(lijst):

    antwoordlijst = []
    for row in lijst:

        if row[2]=="Ja":

            antwoordlijst.append(filterToString(row[1]))
        if row[2]=="Nee":

            antwoordlijst.append(filterToString(row[0]))

    return antwoordlijst

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
    eventIds = [eventId+"M", eventId+"R"]
    if Rinschrijvingen.zoekInschrijving(eventId+"M"):
        for id in eventIds:
            Rinschrijvingen.verwijderInschrijvingen(id)








