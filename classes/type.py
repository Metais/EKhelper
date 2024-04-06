from enum import Enum

effectiveness_matrix = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 1, 0.5],
    [1, 0.5, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1, 2],
    [1, 2, 0.5, 1, 0.5, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1],
    [1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1],
    [1, 0.5, 2, 1, 0.5, 1, 1, 0.5, 2, 0.5, 1, 0.5, 2, 1, 0.5, 1, 0.5],
    [1, 0.5, 0.5, 1, 2, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 0.5],
    [2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 2],
    [1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 0],
    [1, 2, 1, 2, 0.5, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 1, 2],
    [1, 1, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0.5],
    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0, 0.5],
    [1, 0.5, 1, 1, 2, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5],
    [1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 0.5],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 0.5],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0.5],
    [1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 0.5],
    [1, 0.5, 0.5, 0.5, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0.5]
]

# Transpose of effectiveness matrix (without having to import the heavyweight numpy)
vulnerable_matrix = [[row[i] for row in effectiveness_matrix] for i in range(len(effectiveness_matrix[0]))]

def get_physical_types():
    return [Type.Normal, Type.Fighting, Type.Poison, Type.Ground, Type.Flying, Type.Bug, Type.Rock, Type.Ghost, Type.Steel]
    
def get_special_types():
    return [Type.Fire, Type.Water, Type.Electric, Type.Grass, Type.Ice, Type.Psychic, Type.Dragon, Type.Dark]

class Type(Enum):
    Normal = 0
    Fire = 1
    Water = 2
    Electric = 3
    Grass = 4
    Ice = 5
    Fighting = 6
    Poison = 7
    Ground = 8
    Flying = 9
    Psychic = 10
    Bug = 11
    Rock = 12
    Ghost = 13
    Dragon = 14
    Dark = 15
    Steel = 16

    def type_effectiveness_against_types(atk_type, def_types):
        effectiveness = effectiveness_matrix[atk_type.value][def_types[0].value]

        if len(def_types) == 1:
            return effectiveness
        else:
            return effectiveness * effectiveness_matrix[atk_type.value][def_types[1].value]


    def effectivity_against(types):
        # (0x damage against it, 0.25x resistant, 0.5x, 1x, 2x weakness, 4x)
        res = [] * 6

        vulnerable = vulnerable_matrix[types[0].value]

        if len(types) > 1:
            vulnerable_2 = vulnerable_matrix[types[1].value]

        for i in range(0, 17):
            if len(types) > 1:
                vulnerable[i] = vulnerable[i] * vulnerable_2[i]
            
            if vulnerable[i] == 0:
                res[0].append(Type(i))
            elif vulnerable[i] == 0.25:
                res[1].append(Type(i))
            elif vulnerable[i] == 0.5:
                res[2].append(Type(i))
            elif vulnerable[i] == 1:
                res[3].append(Type(i))
            elif vulnerable[i] == 2:
                res[4].append(Type(i))
            else:
                res[5].append(Type(i))
        
        return res

    def get_type(s):
        s = s.lower()
        match s:
            case "normal":
                return Type.Normal
            case "fire":
                return Type.Fire
            case "water":
                return Type.Water
            case "electric":
                return Type.Electric
            case "grass":
                return Type.Grass
            case "ice":
                return Type.Ice
            case "fighting":
                return Type.Fighting
            case "poison":
                return Type.Poison
            case "ground":
                return Type.Ground 
            case "flying":
                return Type.Flying
            case "psychic":
                return Type.Psychic
            case "bug":
                return Type.Bug
            case "rock":
                return Type.Rock
            case "ghost":
                return Type.Ghost
            case "dragon":
                return Type.Dragon
            case "dark":
                return Type.Dark
            case "steel":
                return Type.Steel
            case _:
                raise Exception("Unknown type: " + s) 
