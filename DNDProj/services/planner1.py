import Repo.groepen as Rgroepen
import Repo.inschrijvingen as Rinschrijvingen
import Repo.DMs as RDMs
import Repo.tafels as Rtafels
import Classes.tafelobjects as Tobs


def planTafels(eventId):
    DMLWs = []
    NPLWs = []

    Tobjects = Rtafels.maakTafels(eventId)

    DMgroepen, RejectedClusters, AllLW = vulDMgroepenclusters(eventId)

    for wolf in AllLW:
        if wolf.dm == 'No preference':
            NPLWs.append(wolf)
        else:
            DMLWs.append(wolf)

    # steek alle lonewolfs met een DMpref bij de gewenste DMpref

    for wolf in DMLWs:
        for DMgroep in DMgroepen:
            if wolf.dm == DMgroep.naam:
                DMgroep.DMlonewolf_buidel.append(wolf)
                break

    # om te zien hoeveel mensen er in de clusters zitten, het totaal afgetrokken van hoeveel plaatsen over
    DMgroepen = sorted(DMgroepen, key=lambda DMgroep: DMgroep.maxspelers_start - DMgroep.maxspelers + len(
        DMgroep.DMlonewolf_buidel), reverse=True)

    # de items in de clusterbuidel hebben
    i = 0
    for Tobject in Tobjects:
        if i < len(DMgroepen):
            DMgroep = DMgroepen[i]
            # zet de DM bij deze tafel
            Tobject.dmName = DMgroep.naam
            Tobject.dmMaxAantal = DMgroep.maxspelers_start
            # als het er allemaal in past steek het allemaal in
            if Tobject.maxAantal <= DMgroep.maxspelers_start - DMgroep.maxspelers:
                for cluster in DMgroep.ranked_cluster_buidel:
                    for speler in cluster[0]:
                        Tobject.deelnemers.append(speler)
                        Tobject.deelnemeraantal += 1
                        Tobject.dmMaxAantal -= 1
            else:
                for cluster in DMgroep.ranked_cluster_buidel:
                    # als de hele cluster aan tafel geraakt en de tafel overschrijft de DM maxaantal niet
                    if Tobject.maxAantal - Tobject.deelnemeraantal >= len(cluster[0]):
                        for inschrijving in cluster[0]:
                            Tobject.deelnemers.append(inschrijving)
                            Tobject.deelnemeraantal += 1
                            Tobject.dmMaxAantal -= 1
                    else:
                        RejectedClusters.append(cluster[0])
            # de DM heeft nog plaats en de tafel heeft nog plaats
            # de wolf word bij DM geplaatst of hij word bij de NPLW gezet
            for wolf in DMgroep.DMlonewolf_buidel:
                if Tobject.dmMaxAantal > 0 and Tobject.maxAantal - Tobject.deelnemeraantal > 0:
                    Tobject.deelnemers.append(wolf)
                    Tobject.dmMaxAantal -= 1
                else:
                    NPLWs.append(wolf)

            i += 1
        else:
            break

    Tobjects = sorted(Tobjects, key=lambda Tobject: len(Tobject.deelnemers), reverse=False)

    # hier kan het zijn dat er met DMloze tafels gewerkt word
    # dus eerst even de lege DMloze tafels eruit halen
    TobjectsmetDM = []
    tafelsZonderDM = []
    for object in Tobjects:
        if object.dmName == "None":
            tafelsZonderDM.append(object)
        else:
            TobjectsmetDM.append(object)

    Tobjects = TobjectsmetDM

    Tobjects = sorted(Tobjects, key=lambda Tobject: len(Tobject.deelnemers), reverse=False)

    i = 0
    for cluster in RejectedClusters:
        # kan de hele cluster in de remaining plaatsen van de tafel met de meeste plaatsen, if not steek erzoveel in en ga door
        if Tobjects[i].maxAantal - len(Tobjects[i].deelnemers) >= len(cluster) and Tobjects[i].dmMaxAantal - len(Tobjects[i].deelnemers) >= len(cluster):
            for inschrijving in cluster:
                Tobjects[i].deelnemers.append(inschrijving)
                Tobjects[i].dmMaxAantal -= 1
        # zo niet ga probeer dan zoveel mogelijk inschrijvingen in de tafel te steken
        else:
            for inschrijving in cluster:
                # zit er nog iets in de cluster
                if len(cluster) == 0:
                    break
                # is er nog een plaats aan de tafel, en overschrijd het de DMlimiet niet
                if Tobjects[i].maxAantal > len(Tobjects[i].deelnemers) and Tobjects[i].dmMaxAantal > 0:
                    Tobjects[i].deelnemers.append(inschrijving)
                    Tobjects[i].dmMaxAantal -= 1
                else:
                    i += 1

    # op het einde van deze loop:
    # hebben all tafels een DM
    # zijn alle clusters en rejectedclusters toegekent
    # Nu nog de wolfs en lone wolfs

    Tobjects = verdeelLonewolfs([Tobjects, NPLWs])

    return Tobjects


def verdeelLonewolfs(antwoord):
    Tobjects = antwoord[0]
    lonewolfs = antwoord[1]
    Tobjects2Few = []
    Tobjectsgood = []
    Tobjectsempty = []

    # wroden lege tafels onderscheiden van tafels met meer als 3 en tafels met minder als 3
    for Tobject in Tobjects:
        if len(Tobject.deelnemers) == 0:
            Tobjectsempty.append(Tobject)
        elif 0 < len(Tobject.deelnemers) < 3:
            Tobjects2Few.append(Tobject)
        else:
            Tobjectsgood.append(Tobject)

    # eerst er voor zorgen dat de geen tafels van minder als 3 spelers zijn
    if len(lonewolfs) > 0:
        if len(Tobjects2Few) > 0:
            Tobjects2Few = sorted(Tobjects2Few, key=lambda Tobject: len(Tobject.deelnemers), reverse=True)

            # de wolfs bij groepen van minder als drie steken

            i = 0
            while i < len(Tobjects2Few) and len(lonewolfs) > 0:
                if Tobjects2Few[i].deelnemers == 3:
                    i += 1
                else:
                    Tobjects2Few[i].deelnemers.append(lonewolfs.pop())
                    Tobjects2Few[i].dmMaxAantal -= 1

    # er voor zorgen dat er geen lege tafels zijn
    if len(lonewolfs) > 0:
        if len(Tobjectsempty) > 0:
            # de wolfs bij de lege groepen steken:
            for Tobject in Tobjectsempty:

                if len(lonewolfs) >= 3:
                    for aantal in range(3):
                        Tobject.deelnemers.append(lonewolfs.pop())
                        Tobject.dmMaxAantal -= 1


                else:
                    break

    TerugSamenObjects = Tobjectsgood + Tobjects2Few + Tobjectsempty

    # de lonewolfs bij de DMs steken die nog plaats hebben
    if len(lonewolfs) > 0:

        TerugSamenObjects = sorted(TerugSamenObjects, key=lambda Tobject: len(Tobject.deelnemers), reverse=False)

        minstaantaldeelnemers = len(TerugSamenObjects[0].deelnemers)
        NietsToegedient = False
        while len(lonewolfs) > 0 and not NietsToegedient:
            NietsToegedient = True
            for table in TerugSamenObjects:
                if len(lonewolfs) > 0:
                    if len(table.deelnemers) == minstaantaldeelnemers:
                        if table.dmMaxAantal > 0 and table.maxAantal > len(table.deelnemers):
                            table.deelnemers.append(lonewolfs.pop())
                            table.dmMaxAantal -= 1
                            NietsToegedient = False
            minstaantaldeelnemers += 1



    # tafels onderschijden die extra plaatse hebben en die niet
    tafelsMetExtraPlaatsen = []
    tafelsZonderExtraPlaatsen = []

    for tafel in TerugSamenObjects:
        if tafel.dmMaxAantal < tafel.maxAantal:
            tafelsMetExtraPlaatsen.append(tafel)
        else:
            tafelsZonderExtraPlaatsen.append(tafel)

    # de remaining lonewolfs
    if len(lonewolfs) > 0:

        # dit garandeert dat er eerst bij de grote tafels gekeken word of er nog extra plaatsen zijn, en dan pas bij de kleine tafels
        # het kan zijn dat bij nieuwe DMs nog plaats is
        tafelsMetExtraPlaatsen = sorted(tafelsMetExtraPlaatsen, key=lambda Tobject: Tobject.maxAantal, reverse=True)

        i = 0
        NietsToegekent = False
        while len(lonewolfs) > 0 and NietsToegekent is False:
            NietsToegekent = True
            for tafel in tafelsMetExtraPlaatsen:
                if tafel.maxAantal > len(tafel.deelnemers) and len(lonewolfs) > 0:
                    tafel.deelnemers.append(lonewolfs.pop())
                    NietsToegekent = False

    tafelsFinal = tafelsMetExtraPlaatsen + tafelsZonderExtraPlaatsen
    tafelsFinal = sorted(tafelsFinal, key=lambda Tobject: Tobject.maxAantal, reverse=True)
    i = 1
    for tafel in tafelsFinal:
        tafel.tafelnummer = i
        i += 1

    return [tafelsFinal,lonewolfs]



def vulDMgroepenclusters(eventId):
    Clusters, lonewolfs = maakClusters(eventId)
    DMgroepen, DMgroeplookup = RDMs.maakDMgroepen()
    RankedCLusters = ClustersRanked(Clusters)
    RejectedClusters = []

    for cluster in RankedCLusters:

        toegedeeld = False
        # een rankedDM is een ranknummer en een DMnaam
        # cluster houd een lijst met lijsten van 2 bij, met eerst de cluster en ten tweede de gerankte dms
        # vb: [[inschrijving,inschrijving],[(1,'DM1'),(2,'DM2')]
        for rankedDM in cluster[1]:
            if not toegedeeld:
                DMgroep = DMgroeplookup[rankedDM[1]]
                if DMgroep.maxspelers >= len(cluster[0]):
                    DMgroep.ranked_cluster_buidel.append(cluster)

                    DMgroeplookup[rankedDM[1]].maxspelers = DMgroep.maxspelers - len(cluster[0])
                    toegedeeld = True
            else:
                break
        if not toegedeeld:
            RejectedClusters.append(cluster[0])

    # Ik zorg ervoor dat clusters geordend zijn van groot naar klein
    for DMgroep in DMgroepen:
        DMgroep.ranked_cluster_buidel = sorted(DMgroep.ranked_cluster_buidel, key=lambda cluster: len(cluster[0]),
                                               reverse=True)

    return [DMgroepen, RejectedClusters, lonewolfs]





# Nodig
def maakClusters(eventId):
    Clusters = []
    lonewolfs = []

    antwoord = Rgroepen.maakGroepen()
    inschrijvingen = Rinschrijvingen.geefInschrijvingenEvent(eventId)
    #De loop gaat dit gebruiken om bij te houden wie al assigned is en wie niet
    namenInschrijvingen = []

    for inschrijving in inschrijvingen:
        namenInschrijvingen.append(inschrijving.naam)

    lookupInschrijving = {}
    for inschrijving in inschrijvingen:
        lookupInschrijving[inschrijving.naam] = inschrijving

    # groeplijst is gewoon de excel met namen van groepleden
    groeplijst = antwoord[0]
    # dit is een lijstmet enkel de namen en niet de groepnummers
    namenGroeplijst = []
    for koppel in groeplijst:
        namenGroeplijst.append(koppel[1])
    lookupgroup = antwoord[1]
    groups = antwoord[2]


    for inschrijving in inschrijvingen:
        cluster = []
        naam = inschrijving.naam

        if naam in namenInschrijvingen:
            if naam in namenGroeplijst:
                # zoek groepnummer
                groepnummer = lookupgroup[naam]
                # zoek de groep
                groep = groups[groepnummer]
                # zet alle groepleden in de cluster als ze in de inschrijvingen staan
                # en verwijder ze dan uit de inschrijvingen
                for persoon in groep.leden:
                    if persoon in namenInschrijvingen:
                        lidInschrijving = lookupInschrijving[persoon]
                        cluster.append(lidInschrijving)
                        namenInschrijvingen.remove(persoon)

            else:
                lonewolfs.append(inschrijving)

        # als er daadwerkelijk iets in de cluster zit
        if len(cluster) > 1:
            Clusters.append(cluster)
        # clusters mogen niet te groot zijn
        if len(cluster) > 9:
            for i in range(len(cluster) - 7):
                lonewolfs.append(cluster.pop())

    return [Clusters, lonewolfs]

# Nodig
def ClustersRanked(Clusters):
    ClusterWithRanked = []

    for cluster in Clusters:
        DMCounts = {}
        for inschrijving in cluster:
            if inschrijving.dm in DMCounts and inschrijving.dm != "No preference":
                DMCounts[inschrijving.dm] += 1
            else:
                DMCounts[inschrijving.dm] = 1
        ###bugfix Als DM no preferecen is mag niet meegeteld worden
        sorted_DMs = sorted(DMCounts.items(), key=lambda item: item[1], reverse=True)[:3]

        ranked_DMs = [(rank + 1, dm) for rank, (dm, count) in enumerate(sorted_DMs)]

        ClusterWithRanked.append([cluster, ranked_DMs])

    return ClusterWithRanked




