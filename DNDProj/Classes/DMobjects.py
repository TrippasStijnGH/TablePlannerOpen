class DM:
    def __init__(self, id, naam, maxspelers, email=None, geboortedatum=None, postcode=None ):
        self.id = id
        self.naam = naam
        self.email = email
        self.geboortedatum = geboortedatum
        self.postcode = postcode
        self.maxspelers = maxspelers