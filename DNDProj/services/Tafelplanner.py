import repo.tables as tafelRepo
import repo.registrations as inschrijvingenRepo
import repo.groups as Rgroepen
import services.planner1 as p1
import pandas as pd


def plantafelsAlfa(eventId):
    lookupgroepnummer = Rgroepen.make_groups()[1]
    groeplijst = Rgroepen.make_groups()[0]
    groepmembers = list(map(lambda x: x[1], groeplijst))
    tafelobjecten, remainingwolfs = p1.planTafels(eventId)
    j = 1
    tafels = []
    if len(remainingwolfs) > 0:
        message = []
        message.append("!!!!!")
        message.append("Teweinig plaatsen!")
        message.append("Onderstaande spelers zijn niet toegekent")
        for wolf in remainingwolfs:
            message.append(wolf.name)
        tafels.append(message)

    for tafelObj in tafelobjecten:
        i = 0
        tafel = []

        tafel.append(f"__{tafelObj.max_number + 1}__   >>>Tafel: {tafelObj.table_number} <<<")

        tafel.append(f"<{i}> > {tafelObj.DM_name} {tafelObj.DM}")
        i += 1

        for inschrijving in tafelObj.participants:
            groepnummer = 0
            if inschrijving.name in groepmembers:
                groepnummer = lookupgroepnummer[inschrijving.name]
            happy = ":)"

            if inschrijving.DM != tafelObj.DM_name:
                happy = ":("
            if inschrijving.DM == "No preference":
                happy = "NP"

            tinput = f"<{i}> o {groepnummer} {j} {happy} {inschrijving.name}"
            i += 1
            j += 1
            tafel.append(tinput)

        for legePlaats in range(tafelObj.max_number - len(tafelObj.participants)):
            tafel.append(f"<{i}> (x)")
            i+=1

        tafels.append(tafel)




    planning = tafelsToString(tafels)

    return planning


def tafelsToString(planning):
    planningString = ""

    for tafel in planning:
        for item in tafel:
            planningString += item +"\n"
        planningString += "\n"
    return planningString

def toExcel(eventId):
    tafelobjecten, remainingwolfs = p1.planTafels(eventId)
    output = []
    for tafel in tafelobjecten:
        output.append(tafel.DM_name)
        for inschrijving in tafel.participants:
            output.append(inschrijving.name)
        output.append(" ")

    df = pd.DataFrame(output, columns=["Planning"])

    # Write the DataFrame to an Excel file
    df.to_excel("output.xlsx", index=False)


















