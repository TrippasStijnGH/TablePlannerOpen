class DM:
    def __init__(self, id, name, max_players, email=None, birth_date=None, postcode=None):
        self.id = id
        self.name = name
        self.email = email
        self.birth_date = birth_date
        self.postcode = postcode
        self.max_players = max_players