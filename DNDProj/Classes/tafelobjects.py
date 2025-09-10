class Tafel:
    def __init__(self, event_id, maxAantal, tafelnummer=0, dm_id=0):
        self.event_id = event_id
        self.maxAantal = maxAantal
        self.deelnemeraantal = 0
        self.tafelnummer = tafelnummer
        self.dm = dm_id
        self.dmName = "None"
        self.dmMaxAantal = 0
        self.deelnemers = []

    def add_deelnemer(self, deelnemer):
        self.deelnemers.append(deelnemer)