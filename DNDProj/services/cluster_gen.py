import repo.groups as r_groups
import repo.registrations as r_registrations
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