
class Event:
    def __init__(self, event_id, name, date, location, tables=None):
        self.id = event_id
        self.name = name
        self.date = date
        self.location = location
        self.tables = tables
