class DMgroep:
    def __init__(self, id, naam, maxspelers):
        self.id = id
        self.naam = naam
        self.maxspelers = maxspelers
        self.maxspelers_start = maxspelers
        self.inschrijvingen = []
        self.ranked_cluster_buidel = []
        self.DMlonewolf_buidel = []

    def add_deelnemer(self, deelnemer):
        self.inschrijvingen.append(deelnemer)