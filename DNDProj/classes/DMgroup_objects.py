class DMgroup:
    #max_players_pref keeps track of the prefered max number of players the DM likes to have

    #availabel_spots keepts track of how many more players can be added to this in either pouch

    #
    def __init__(self, id, name, max_players):
        self.id = id
        self.name = name
        self.available_spots = max_players
        self.max_players_pref = max_players
        self.ranked_cluster_pouch = []
        self.DMlonewolf_pouch = []

