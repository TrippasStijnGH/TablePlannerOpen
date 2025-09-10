class Groep:
    def __init__(self, nummer):
        self.nummer = nummer
        self.leden = []


    def add_lid(self, lid):
        self.leden.append(lid)