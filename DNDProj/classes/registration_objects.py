class Registration:
    def __init__(self, persoon_id, name, dm):

        self.persoon_id = persoon_id
        self.name = name
        self.dm = dm


class RegistrationDP:
    def __init__(self, participant, email, dm, notes):

        self.participant = participant
        self.email = email
        self.dm = dm
        self.notes = notes