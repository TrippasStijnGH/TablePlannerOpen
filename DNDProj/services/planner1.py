import repo.groups as Rgroepen
import repo.registrations as Rinschrijvingen
import repo.DMs as RDMs
import repo.tables as Rtafels
import classes.table_objects as Tobs


def planTafels(eventId):

    Tobjects = Rtafels.make_tables(eventId) #returns objects for the available tables

    DMgroepen, RejectedClusters, AllLW = vulDMgroepenclusters(eventId)

    DMLWs = []   #LoneWolfs with DM preference
    NPLWs = []   #LoneWolfs with no preference

    for wolf in AllLW:
        if wolf.DM == 'No preference':
            NPLWs.append(wolf)
        else:
            DMLWs.append(wolf)

    # steek alle lonewolfs met een DMpref bij de gewenste DMpref

    for wolf in DMLWs:
        for DMgroep in DMgroepen:
            if wolf.DM == DMgroep.name:
                DMgroep.DMlonewolf_pouch.append(wolf)
                break

    # om te zien hoeveel mensen er in de clusters zitten, het totaal afgetrokken van hoeveel plaatsen over
    DMgroepen = sorted(DMgroepen, key=lambda DMgroep: DMgroep.max_players_start - DMgroep.max_players + len(
        DMgroep.DMlonewolf_pouch), reverse=True)

    # de items in de clusterbuidel hebben
    i = 0
    for Tobject in Tobjects:
        if i < len(DMgroepen):
            DMgroep = DMgroepen[i]
            # zet de DM bij deze tafel
            Tobject.DM_name = DMgroep.name
            Tobject.DM = DMgroep.id
            Tobject.DM_max_number = DMgroep.max_players_start
            # als het er allemaal in past steek het allemaal in
            if Tobject.max_number <= DMgroep.max_players_start - DMgroep.max_players:
                for cluster in DMgroep.ranked_cluster_pouch:
                    for speler in cluster[0]:
                        Tobject.participants.append(speler)
                        Tobject.participant_number += 1
                        Tobject.DM_max_number -= 1
            else:
                for cluster in DMgroep.ranked_cluster_pouch:
                    # als de hele cluster aan tafel geraakt en de tafel overschrijft de DM maxaantal niet
                    if Tobject.max_number - Tobject.participant_number >= len(cluster[0]):
                        for inschrijving in cluster[0]:
                            Tobject.participants.append(inschrijving)
                            Tobject.participant_number += 1
                            Tobject.DM_max_number -= 1
                    else:
                        RejectedClusters.append(cluster[0])
            # de DM heeft nog plaats en de tafel heeft nog plaats
            # de wolf word bij DM geplaatst of hij wordt bij de NPLW gezet
            for wolf in DMgroep.DMlonewolf_pouch:
                if Tobject.DM_max_number > 0 and Tobject.max_number - Tobject.participant_number > 0:
                    Tobject.participants.append(wolf)
                    Tobject.DM_max_number -= 1
                else:
                    NPLWs.append(wolf)

            i += 1
        else:
            break

    Tobjects = sorted(Tobjects, key=lambda Tobject: len(Tobject.participants), reverse=False)

    # hier kan het zijn dat er met DMloze tafels gewerkt word
    # dus eerst even de lege DMloze tafels eruit halen
    TobjectsmetDM = []
    tafelsZonderDM = []
    for object in Tobjects:
        if object.DM_name == "None":
            tafelsZonderDM.append(object)
        else:
            TobjectsmetDM.append(object)

    Tobjects = TobjectsmetDM





    #new
    #this loop checks if any tables have been assigned earlier players but haven't reached the 3 player minimum

    Tobjects = sorted(Tobjects, key=lambda Tobject: len(Tobject.participants))

    for tafel in Tobjects:

        if len(tafel.participants) > 2:

            break

        # The next loop will look to append a cluster from rejectedcluster
        # if it rejects it because it is too big for this table it will pop it and then put it back for the next table
        RejectedClusters2 = []

        # first it checks if any clusters can be added
        if 1 < len(tafel.participants) < 3:
            while len(tafel.participants) < 3 and len(RejectedClusters) > 0:
                    if tafel.max_number - len(tafel.participants) >= len(RejectedClusters[0]) and tafel.DM_max_number - len(tafel.participants) >= len(RejectedClusters[0]):
                        for inschrijving in RejectedClusters[0]:
                            tafel.participants.append(inschrijving)
                            tafel.DM_max_number -= 1
                        RejectedClusters.pop(0)
                    #here it gets rid of the Rejected cluster that doenst fit this table and puts it aside until we hit the next table
                    else:
                        RejectedClusters2.append(RejectedClusters.pop(0))


        # secondly it checks if any LW can be added
        if 1 < len(tafel.participants) < 3:
            while len(tafel.participants) < 3 and len(NPLWs)>0:

                tafel.participants.append(NPLWs.pop(0))
                tafel.DM_max_number -= 1

        #Adds the ignored clusters back
        RejectedClusters.extend(RejectedClusters2)







    Tobjects = sorted(Tobjects, key=lambda Tobject: len(Tobject.participants), reverse=False)






    for cluster in RejectedClusters:

        i = 0
        # kan de hele cluster in de remaining plaatsen van de tafel met de meeste plaatsen, if not steek erzoveel in en ga door
        if Tobjects[0].max_number - len(Tobjects[0].participants) >= len(cluster) and Tobjects[0].DM_max_number - len(Tobjects[0].participants) >= len(cluster):

            for inschrijving in cluster:
                Tobjects[0].participants.append(inschrijving)
                Tobjects[0].DM_max_number -= 1
                Tobjects = sorted(Tobjects, key=lambda Tobject: len(Tobject.participants), reverse=False)



        # zo niet ga probeer dan zoveel mogelijk inschrijvingen in de tafel te steken

        else:
            for inschrijving in cluster:
                # zit er nog iets in de cluster
                if len(cluster) == 0:
                    break
                # is er nog een plaats aan de tafel, en overschrijd het de DMlimiet niet
                if Tobjects[0].max_number > len(Tobjects[i].participants) and Tobjects[i].DM_max_number > 0:
                    Tobjects[0].participants.append(inschrijving)
                    Tobjects[0].DM_max_number -= 1
                    Tobjects = sorted(Tobjects, key=lambda Tobject: len(Tobject.participants), reverse=False)
                else:
                    Tobjects = sorted(Tobjects, key=lambda Tobject: len(Tobject.participants), reverse=False)

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
        if len(Tobject.participants) == 0:
            Tobjectsempty.append(Tobject)
        elif 0 < len(Tobject.participants) < 3:
            Tobjects2Few.append(Tobject)
        else:
            Tobjectsgood.append(Tobject)

    # eerst er voor zorgen dat de geen tafels van minder als 3 spelers zijn
    if len(lonewolfs) > 0:
        if len(Tobjects2Few) > 0:
            Tobjects2Few = sorted(Tobjects2Few, key=lambda Tobject: len(Tobject.participants), reverse=True)

            # de wolfs bij groepen van minder als drie steken

            i = 0
            while i < len(Tobjects2Few) and len(lonewolfs) > 0:
                if Tobjects2Few[i].participants == 3:
                    i += 1
                else:
                    Tobjects2Few[i].participants.append(lonewolfs.pop())
                    Tobjects2Few[i].DM_max_number -= 1

    # er voor zorgen dat er geen lege tafels zijn
    if len(lonewolfs) > 0:
        if len(Tobjectsempty) > 0:
            # de wolfs bij de lege groepen steken:
            for Tobject in Tobjectsempty:

                if len(lonewolfs) >= 3:
                    for aantal in range(3):
                        Tobject.participants.append(lonewolfs.pop())
                        Tobject.DM_max_number -= 1


                else:
                    break

    TerugSamenObjects = Tobjectsgood + Tobjects2Few + Tobjectsempty

    # de lonewolfs bij de DMs steken die nog plaats hebben
    if len(lonewolfs) > 0:

        TerugSamenObjects = sorted(TerugSamenObjects, key=lambda Tobject: len(Tobject.participants), reverse=False)

        minstaantaldeelnemers = len(TerugSamenObjects[0].participants)
        NietsToegedient = False
        while len(lonewolfs) > 0 and not NietsToegedient:
            NietsToegedient = True



            for table in TerugSamenObjects:
                if len(lonewolfs) > 0:
                    if len(table.participants) == minstaantaldeelnemers:
                        if table.DM_max_number > 0 and table.max_number > len(table.participants):
                            table.participants.append(lonewolfs.pop())
                            table.DM_max_number -= 1
                            NietsToegedient = False
            minstaantaldeelnemers += 1



    # tafels onderschijden die extra plaatse hebben en die niet
    tafelsMetExtraPlaatsen = []
    tafelsZonderExtraPlaatsen = []

    for tafel in TerugSamenObjects:
        if tafel.DM_max_number < tafel.max_number:
            tafelsMetExtraPlaatsen.append(tafel)
        else:
            tafelsZonderExtraPlaatsen.append(tafel)

    # de remaining lonewolfs
    if len(lonewolfs) > 0:

        # dit garandeert dat er eerst bij de grote tafels gekeken word of er nog extra plaatsen zijn, en dan pas bij de kleine tafels
        # het kan zijn dat bij nieuwe DMs nog plaats is
        tafelsMetExtraPlaatsen = sorted(tafelsMetExtraPlaatsen, key=lambda Tobject: Tobject.max_number, reverse=True)

        i = 0
        NietsToegekent = False
        while len(lonewolfs) > 0 and NietsToegekent is False:
            NietsToegekent = True
            for tafel in tafelsMetExtraPlaatsen:
                if tafel.max_number > len(tafel.participants) and len(lonewolfs) > 0:
                    tafel.participants.append(lonewolfs.pop())
                    NietsToegekent = False

    tafelsFinal = tafelsMetExtraPlaatsen + tafelsZonderExtraPlaatsen
    tafelsFinal = sorted(tafelsFinal, key=lambda Tobject: Tobject.max_number, reverse=True)
    i = 1
    for tafel in tafelsFinal:
        tafel.table_number = i
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
                if DMgroep.max_players >= len(cluster[0]):
                    DMgroep.ranked_cluster_pouch.append(cluster)

                    DMgroeplookup[rankedDM[1]].max_players = DMgroep.max_players - len(cluster[0])
                    toegedeeld = True
            else:
                break
        if not toegedeeld:
            RejectedClusters.append(cluster[0])

    # Ik zorg ervoor dat clusters geordend zijn van groot naar klein
    for DMgroep in DMgroepen:
        DMgroep.ranked_cluster_pouch = sorted(DMgroep.ranked_cluster_pouch, key=lambda cluster: len(cluster[0]),
                                              reverse=True)

    return [DMgroepen, RejectedClusters, lonewolfs]





# Nodig
def maakClusters(eventId):
    Clusters = []
    lonewolfs = []

    antwoord = Rgroepen.make_groups()
    inschrijvingen = Rinschrijvingen.return_registrations_event(eventId)
    #De loop gaat dit gebruiken om bij te houden wie al assigned is en wie niet
    namenInschrijvingen = []

    for inschrijving in inschrijvingen:
        namenInschrijvingen.append(inschrijving.name)

    lookupInschrijving = {}
    for inschrijving in inschrijvingen:
        lookupInschrijving[inschrijving.name] = inschrijving

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
        naam = inschrijving.name

        if naam in namenInschrijvingen:
            if naam in namenGroeplijst:
                # zoek groepnummer
                groepnummer = lookupgroup[naam]
                # zoek de groep
                groep = groups[groepnummer]
                # zet alle groepleden in de cluster als ze in de inschrijvingen staan
                # en verwijder ze dan uit de inschrijvingen
                for persoon in groep.members:
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
            if inschrijving.DM != "No preference":
                if inschrijving.DM in DMCounts:
                    DMCounts[inschrijving.DM] += 1
                else:
                    DMCounts[inschrijving.DM] = 1
        ###bugfix Als DM no preferecen is mag niet meegeteld worden
        sorted_DMs = sorted(DMCounts.items(), key=lambda item: item[1], reverse=True)[:3]

        ranked_DMs = [(rank + 1, dm) for rank, (dm, count) in enumerate(sorted_DMs)]

        ClusterWithRanked.append([cluster, ranked_DMs])

    return ClusterWithRanked




