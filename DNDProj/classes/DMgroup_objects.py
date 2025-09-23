class DMgroup:
    def __init__(self, id, name, max_players):
        self.id = id
        self.naam = name
        self.max_players = max_players
        self.max_players_start = max_players
        self.registrations = []
        self.ranked_cluster_pouch = []
        self.DMlonewolf_pouch = []

    def add_participant(self, participant):
        self.registrations.append(participant)