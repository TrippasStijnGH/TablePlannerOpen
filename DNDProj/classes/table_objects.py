class Tafel:
    def __init__(self, event_id, max_number, table_number=0, DM_id=0):
        self.event_id = event_id
        self.max_number = max_number
        self.participant_number = 0
        self.table_number = table_number
        self.DM = DM_id
        self.DM_name = "None"
        self.DM_max_number = 0
        self.participants = []

    def add_deelnemer(self, participant):
        self.participants.append(participant)