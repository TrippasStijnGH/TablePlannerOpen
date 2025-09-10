import pandas as pd
import settings
import Classes.groepobjects as GroepObs



def maakGroepen():

    excel = settings.EXCELGROEPEN

    excel_file = pd.read_excel(excel)

    groepHeaders = ["Groep","Naam"]
    groeplijst = []
    lookupgroup = {}


    for index, row in excel_file.iterrows():
        valuesGroep = [row[header] for header in groepHeaders]
        groeplijst.append(valuesGroep)
        lookupgroup[valuesGroep[1]] = valuesGroep[0]

    groups = {}

    for row in groeplijst:
        number, name = row
        if number not in groups:
            groups[number] = GroepObs.Groep(number)
        # Append name to the existing group object
        groups[number].leden.append(name)

    #groeplijst is de originele excel
    #loopupgroup is voor een naam te vinden bij welke groep
    #groups zijn objecten die een lijst namen hebben en een veld met de nummer van de groep
    antwoord = [groeplijst,lookupgroup,groups]

    return (antwoord)


maakGroepen()














