class Registration:
    def __init__(self, persoon_id, name, DM):

        self.persoon_id = persoon_id
        self.name = name
        self.DM = DM


class RegistrationDP:
    def __init__(self, participant, email, DM, notes):

        self.participant = participant
        self.email = email
        self.DM = DM
        self.notes = notes