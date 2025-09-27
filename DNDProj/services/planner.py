import repo.groups as r_groups
import repo.registrations as r_registrations
import repo.DMs as r_DMs
import repo.tables as r_tables
import classes.table_objects as Tobs


def plan_tafels(event_id):

    # make table objects
    t_objects = r_tables.make_tables(event_id)

    # fill the DMgroup with  player clusters
    DM_groups, rejected_clusters, all_LWs = fill_DMgroup_clusters(event_id)

    # assign the lone wolves with DM preference to their preferred DM
    # put aside lone wolves that had no preference or could not be assigned to their preferred DM
    DM_groups, LWs = assign_LW_DM(all_LWs, DM_groups)

    # assign the DMgroups to a table
    # put aside player clusters that could not be assigned to a table of their preferred DM
    # put aside lone wolves that could not be assigned to a table of their preferred DM
    t_objects, rejected_clusters, added_LWs = DMgroup_to_tables(DM_groups,t_objects)

    # add the lone wolves to the existing pool of lone wolves
    LWs = LWs + added_LWs

    # assign the rejected player clusters to any available table
    # break up non-assigned rejected player clusters and add them to any available table
    t_objects= assign_rejected_clusters(t_objects, rejected_clusters)

    t_objects, LWs = assign_remaining_LWs(t_objects, LWs)


    return t_objects, LWs



#this creates DMgroup objects who hold ranked clusters and lonewolfs
#ranked clusters are clusters of participants who want to sit together,
def fill_DMgroup_clusters(eventId):
    clusters, LWs = make_clusters(eventId)
    DMgroups, DMgroup_lookup = r_DMs.make_DM_groups()
    ranked_clusters = clusters_ranked(clusters)
    rejected_clusters = []

    for cluster in ranked_clusters:

        assigned = False
        # een rankedDM is een ranknummer en een DMnaam
        # cluster houd een lijst met lijsten van 2 bij, met eerst de cluster en ten tweede de gerankte dms
        # vb: [[inschrijving,inschrijving],[(1,'DM1'),(2,'DM2')]
        for ranked_DM in cluster[1]:
            if not assigned:
                DMgroup = DMgroup_lookup[ranked_DM[1]]
                if DMgroup.max_players >= len(cluster[0]):
                    DMgroup.ranked_cluster_pouch.append(cluster)

                    DMgroup_lookup[ranked_DM[1]].max_players = DMgroup.max_players - len(cluster[0])
                    assigned = True
            else:
                break
        if not assigned:
            rejected_clusters.append(cluster[0])

    # Ik zorg ervoor dat clusters geordend zijn van groot naar klein
    for DMgroup in DMgroups:
        DMgroup.ranked_cluster_pouch = sorted(DMgroup.ranked_cluster_pouch, key=lambda cluster: len(cluster[0]),
                                              reverse=True)

    return [DMgroups, rejected_clusters, LWs]





#
def make_clusters(event_id):
    clusters = []
    LWs = []

    answer = r_groups.make_groups()
    registrations = r_registrations.return_registrations_event(event_id)

    #loop will use this to see who is already assigned
    registration_names = []

    for registration in registrations:
        registration_names.append(registration.name)

    registration_lookup = {}
    for registration in registrations:
        registration_lookup[registration.name] = registration

    # groeplijst is gewoon de excel met namen van groepleden
    group_list = answer[0]
    # dit is een lijst met enkel de namen en niet de groepnummers
    names_group_list = []

    for tupel in group_list:
        names_group_list.append(tupel[1])
    lookupgroup = answer[1]
    groups = answer[2]


    for registration in registrations:
        cluster = []
        name = registration.name

        if name in registration_names:
            if name in names_group_list:
                # zoek groepnummer
                groepnummer = lookupgroup[name]
                # zoek de groep
                groep = groups[groepnummer]
                # zet alle groepleden in de cluster als ze in de inschrijvingen staan
                # en verwijder ze dan uit de inschrijvingen
                for persoon in groep.members:
                    if persoon in registration_names:
                        lidInschrijving = registration_lookup[persoon]
                        cluster.append(lidInschrijving)
                        registration_names.remove(persoon)

            else:
                LWs.append(registration)

        # als er daadwerkelijk iets in de cluster zit
        if len(cluster) > 1:
            clusters.append(cluster)
        # clusters mogen niet te groot zijn
        if len(cluster) > 9:
            for i in range(len(cluster) - 7):
                LWs.append(cluster.pop())

    return [clusters, LWs]

#
def clusters_ranked(clusters):
    """
    Rank DMs by popularity within each cluster.

    Args:
        clusters (list): List of clusters, each containing registration objects
                        with a 'DM' attribute.

    Returns:
        list: List of [cluster, ranked_DMs] pairs, where ranked_DMs is a
              list of (rank, dm_name) tuples for the top 3 most popular DMs.

    Example:
         clusters = [[reg1, reg2], [reg3, reg4]]
         result = clusters_ranked(clusters)
         Returns: [[cluster1, [(1, "Alice"), (2, "Bob")]], ...]
    """

    ranked_clusters = []

    for cluster in clusters:
        DM_counts = {} #dictionary of how many participants chose this DM
        for registration in cluster:
            if registration.DM != "No preference":
                if registration.DM in DM_counts:
                    DM_counts[registration.DM] += 1
                else:
                    DM_counts[registration.DM] = 1

        #sorts the most chosen DMs and leaves only 3 most popular
        sorted_DMs = sorted(DM_counts.items(), key=lambda item: item[1], reverse=True)[:3]

        #turns the dictionary into an enumerate exm: [(1, "Alice"), (2, "Bob"), (3, "Charlie")]
        ranked_DMs = [(rank + 1, dm) for rank, (dm, count) in enumerate(sorted_DMs)]

        ranked_clusters.append([cluster, ranked_DMs])

    return ranked_clusters

def assign_LW_DM(all_LWs, DM_groups):

    DMLWs = []  # LoneWolfs with DM preference
    NPLWs = []  # LoneWolfs with no preference

    for wolf in all_LWs:
        if wolf.DM == 'No preference':
            NPLWs.append(wolf)
        else:
            DMLWs.append(wolf)

    # steek alle lonewolfs met een DMpref bij de gewenste DMpref

    for wolf in DMLWs:
        for DM_group in DM_groups:
            if wolf.DM == DM_group.name:
                DM_group.DMlonewolf_pouch.append(wolf)
                break

    return (DM_groups, NPLWs)


def DMgroup_to_tables(DM_groups, t_objects):

    # om te zien hoeveel mensen er in de clusters zitten, het totaal afgetrokken van hoeveel plaatsen over
    DM_groups = sorted(DM_groups, key=lambda DM_group: DM_group.max_players_start - DM_group.max_players + len(
        DM_group.DMlonewolf_pouch), reverse=True)

    NPLWs = []

    rejected_clusters = []

    # de items in de clusterbuidel hebben
    i = 0
    for t_object in t_objects:
        if i < len(DM_groups):
            DM_group = DM_groups[i]
            # zet de DM bij deze tafel
            t_object.DM_name = DM_group.name
            t_object.DM = DM_group.id
            t_object.DM_max_number = DM_group.max_players_start
            # als het er allemaal in past steek het allemaal in
            if t_object.max_number <= DM_group.max_players_start - DM_group.max_players:
                for cluster in DM_group.ranked_cluster_pouch:
                    for speler in cluster[0]:
                        t_object.participants.append(speler)
                        t_object.participant_number += 1
                        t_object.DM_max_number -= 1
            else:
                for cluster in DM_group.ranked_cluster_pouch:
                    # als de hele cluster aan tafel geraakt en de tafel overschrijft de DM maxaantal niet
                    if t_object.max_number - t_object.participant_number >= len(cluster[0]):
                        for registration in cluster[0]:
                            t_object.participants.append(registration)
                            t_object.participant_number += 1
                            t_object.DM_max_number -= 1
                    else:
                        rejected_clusters.append(cluster[0])
            # de DM heeft nog plaats en de tafel heeft nog plaats
            # de wolf word bij DM geplaatst of hij wordt bij de NPLW gezet
            for wolf in DM_group.DMlonewolf_pouch:
                if t_object.DM_max_number > 0 and t_object.max_number - t_object.participant_number > 0:
                    t_object.participants.append(wolf)
                    t_object.DM_max_number -= 1
                else:
                    NPLWs.append(wolf)

            i += 1
        else:
            break

    t_objects = sorted(t_objects, key=lambda t_object: len(t_object.participants), reverse=False)

    # hier kan het zijn dat er met DMloze tafels gewerkt word
    # dus eerst even de lege DMloze tafels eruit halen
    t_objects_with_DM = []
    t_objects_no_DM = []
    for object in t_objects:
        if object.DM_name == "None":
            t_objects_no_DM.append(object)
        else:
            t_objects_with_DM.append(object)

    t_objects = t_objects_with_DM

    return (t_objects, rejected_clusters, NPLWs)

# problem for some reason the rejected clusters part already tries to add lonewolfs

def assign_rejected_clusters(t_objects, rejected_clusters):

    t_objects = sorted(t_objects, key=lambda Tobject: len(Tobject.participants))

    LWs = []

    for tafel in t_objects:

        if len(tafel.participants) > 2:
            break

        # The next loop will look to append a cluster from rejectedcluster
        # if it rejects it because it is too big for this table it will pop it and then put it back for the next table
        twice_rejected_clusters = []

        # first it checks if any clusters can be added to places where there are to few players
        if 1 < len(tafel.participants) < 3:
            while len(tafel.participants) < 3 and len(rejected_clusters) > 0:
                if tafel.max_number - len(tafel.participants) >= len(
                        rejected_clusters[0]) and tafel.DM_max_number - len(tafel.participants) >= len(
                        rejected_clusters[0]):
                    for registration in rejected_clusters[0]:
                        tafel.participants.append(registration)
                        tafel.DM_max_number -= 1
                    rejected_clusters.pop(0)
                # here it gets rid of the Rejected cluster that doenst fit this table and puts it aside until we hit the next table
                else:
                    twice_rejected_clusters.append(rejected_clusters.pop(0))

        # Adds the ignored clusters back
        rejected_clusters.extend(twice_rejected_clusters)

    # secondly it checks any tables starting with the least crowded, starting with the biggest tables
    t_objects = sorted(t_objects, key=lambda table: (len(table.participants), table.max_number), reverse=False)

    for cluster in rejected_clusters:

        # the list of table objects is sorted as to make the tables with the lowest members first
        # if the entire cluster fits put it at the table

        if t_objects[0].max_number - len(t_objects[0].participants) >= len(cluster) and t_objects[0].DM_max_number - len(t_objects[0].participants) >= len(cluster):

            for registration in cluster:
                t_objects[0].participants.append(registration)
                t_objects[0].DM_max_number -= 1
                t_objects = sorted(t_objects, key=lambda table: (len(table.participants), table.max_number),
                                   reverse=False)

        # at this point if the cluster does not fit, break it up and assign the remaining players

        else:

            t_objects = sorted(t_objects, key=lambda table: (table.max_number - len(table.participants)), reverse=True)

            for registration in cluster:
                # is there anything left in the cluster
                if len(cluster) == 0:
                    break
                # is er nog een plaats aan de tafel, en overschrijd het de DMlimiet niet
                if t_objects[0].max_number > len(t_objects[0].participants) and t_objects[0].DM_max_number > 0:
                    t_objects[0].participants.append(registration)
                    t_objects[0].DM_max_number -= 1
                    t_objects = sorted(t_objects, key=lambda table: (len(table.participants), table.max_number),
                                       reverse=False)
                else:
                    t_objects = sorted(t_objects, key=lambda table: (len(table.participants), table.max_number),
                                       reverse=False)


    # op het einde van deze loop:
    # hebben all tafels een DM
    # zijn alle clusters en rejectedclusters toegekent
    # Nu nog de wolfs en lone wolfs
    return t_objects

def assign_remaining_LWs(t_objects, LWs):

    t_objects_2_few = []
    t_objects_good = []
    t_objects_empty = []

    # wroden lege tafels onderscheiden van tafels met meer als 3 en tafels met minder als 3
    for t_objects in t_objects:
        if len(t_objects.participants) == 0:
            t_objects_empty.append(t_objects)
        elif 0 < len(t_objects.participants) < 3:
            t_objects_2_few.append(t_objects)
        else:
            t_objects_good.append(t_objects)

    # eerst er voor zorgen dat de geen tafels van minder als 3 spelers zijn
    if len(LWs) > 0:
        if len(t_objects_2_few) > 0:
            t_objects_2_few = sorted(t_objects_2_few, key=lambda table: (len(table.participants),table.max_number), reverse=False)

            # de wolfs bij groepen van minder als drie steken

            i = 0
            while i < len(t_objects_2_few) and len(LWs) > 0:
                if t_objects_2_few[i].participants == 3:
                    i += 1
                else:
                    t_objects_2_few[i].participants.append(LWs.pop())
                    t_objects_2_few[i].DM_max_number -= 1

    # er voor zorgen dat er geen lege tafels zijn
    if len(LWs) > 0:
        if len(t_objects_empty) > 0:
            # de wolfs bij de lege groepen steken:
            for t_objects in t_objects_empty:

                if len(LWs) >= 3:
                    for aantal in range(3):
                        t_objects.participants.append(LWs.pop())
                        t_objects.DM_max_number -= 1


                else:
                    break

    tables_united = t_objects_good + t_objects_2_few + t_objects_empty

    # de lonewolfs bij de DMs steken die nog plaats hebben
    if len(LWs) > 0:

        tables_united = sorted(tables_united, key=lambda table: (len(table.participants),table.max_number), reverse=False)

        fewest_participants = len(tables_united[0].participants)
        nothing_assigned = False
        while len(LWs) > 0 and not nothing_assigned:
            nothing_assigned = True


            for table in tables_united:
                if len(LWs) > 0:
                    if len(table.participants) == fewest_participants:
                        if table.DM_max_number > 0 and table.max_number > len(table.participants):
                            table.participants.append(LWs.pop())
                            table.DM_max_number -= 1
                            nothing_assigned = False
            fewest_participants += 1



    # tafels onderschijden die extra plaatse hebben en die niet
    tables_free_spots = []
    tables_full = []

    for table in tables_united:
        if table.DM_max_number < table.max_number:
            tables_free_spots.append(table)
        else:
            tables_full.append(table)

    # de remaining lonewolfs
    if len(LWs) > 0:

        # dit garandeert dat er eerst bij de grote tafels gekeken word of er nog extra plaatsen zijn, en dan pas bij de kleine tafels
        # het kan zijn dat bij nieuwe DMs nog plaats is
        tables_free_spots = sorted(tables_free_spots, key=lambda Tobject: Tobject.max_number, reverse=True)

        i = 0
        nothing_assigned = False
        while len(LWs) > 0 and nothing_assigned is False:
            nothing_assigned = True
            for table in tables_free_spots:
                if table.max_number > len(table.participants) and len(LWs) > 0:
                    table.participants.append(LWs.pop())
                    nothing_assigned = False

    tables_final = tables_free_spots + tables_full
    tables_final = sorted(tables_final, key=lambda Tobject: (Tobject.max_number, len(Tobject.participants)),
                          reverse=True)

    i = 1
    for table in tables_final:
        table.table_number = i
        i += 1

    return (tables_final,LWs)


