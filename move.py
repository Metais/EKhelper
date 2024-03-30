from type import Type

class Move:
    def __init__(self, name, description, type, pp, power, acc, category):
        self.name = name
        self.description = description
        self.type = Type.get_type(type)
        self.pp = pp
        self.power = power
        self.acc = acc
        self.category = category

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    