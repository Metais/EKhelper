from type import Type

class Move:
    def __init__(self, name, description, type, pp, power, acc):
        self.name = name
        self.description = description
        self.type = Type.get_type(type)
        self.pp = pp
        self.power = power
        self.acc = acc

    def __repr__(self):
        return self.name
    