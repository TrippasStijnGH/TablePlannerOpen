class Inschrijving:
    def __init__(self, inschrijving_id, persoon_id, naam, eventid, dm=None, remarks=None, datum=None, vorige_dm=None):
        self.id = inschrijving_id
        self.persoon_id = persoon_id
        self.naam = naam
        self.eventid = eventid
        self.dm = dm
        self.remarks = remarks
        self.datum = datum
        self.vorige_dm = vorige_dm

