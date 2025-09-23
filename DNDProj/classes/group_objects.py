class Group:
    def __init__(self, number):
        self.number = number
        self.members = []


    def add_lid(self, member):
        self.members.append(member)