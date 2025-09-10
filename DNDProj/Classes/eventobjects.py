
class Event:
    def __init__(self, event_id, name, date, plaats, main, tafels=None):
        self.id = event_id
        self.name = name
        self.date = date
        self.plaats = plaats
        self.main = main
        self.tafels = tafels
