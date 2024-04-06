from enum import Enum

class Nature(Enum):
    Hardy = ("atk", "atk")
    Lonely = ("atk", "def")
    Adamant = ("atk", "spa")
    Naughty = ("atk", "spd")
    Brave = ("atk", "spe")
    Bold = ("def", "atk")
    Docile = ("def", "def")
    Impish = ("def", "spa")
    Lax = ("def", "spd")
    Relaxed = ("def", "spe")
    Modest = ("spa", "atk")
    Mild = ("spa", "def")
    Bashful = ("spa", "spa")
    Rash = ("spa", "spd")
    Quiet = ("spa", "spe")
    Calm = ("spd", "atk")
    Gentle = ("spd", "def")
    Careful = ("spd", "spa")
    Quirky = ("spd", "spd")
    Sassy = ("spd", "spe")
    Timid = ("spe", "atk")
    Hasty = ("spe", "def")
    Jolly = ("spe", "spa")
    Naive = ("spe", "spd")
    Serious = ("spe", "spe")

    def get_nature_names():
        return ["Hardy", "Lonely", "Adamant", "Naughty", "Brave", "Bold", "Docile", "Impish", "Lax", "Relaxed", "Modest", "Mild", "Bashful", 
                "Rash", "Quiet", "Calm", "Gentle", "Careful", "Quirky", "Sassy", "Timid", "Hasty", "Jolly", "Naive", "Serious"]
    
    def get_nature_modifier(nature, stat_type):
        # if nature is neutral or non-existent
        if nature == "" or nature.value[0] == nature.value[1]:
            return 1
        elif nature.value[0] == stat_type:
            return 1.1
        elif nature.value[1] == stat_type:
            return 0.9
        else:
            return 1
    
    def get_nature(s):
        s = s.lower()
        match s:
            case "hardy":
                return Nature.Hardy
            case "lonely":
                return Nature.Lonely
            case "adamant":
                return Nature.Adamant
            case "naughty":
                return Nature.Naughty
            case "brave":
                return Nature.Brave
            case "bold":
                return Nature.Bold
            case "docile":
                return Nature.Docile
            case "impish":
                return Nature.Impish
            case "lax":
                return Nature.Lax
            case "relaxed":
                return Nature.Relaxed
            case "modest":
                return Nature.Modest
            case "mild":
                return Nature.Mild
            case "bashful":
                return Nature.Bashful
            case "rash":
                return Nature.Rash
            case "quiet":
                return Nature.Quiet
            case "calm":
                return Nature.Calm
            case "gentle":
                return Nature.Gentle
            case "careful":
                return Nature.Careful
            case "quirky":
                return Nature.Quirky
            case "sassy":
                return Nature.Sassy
            case "timid":
                return Nature.Timid
            case "hasty":
                return Nature.Hasty
            case "jolly":
                return Nature.Jolly
            case "naive":
                return Nature.Naive
            case "serious":
                return Nature.Serious
            case _:
                raise Exception(f"Can't interpret nature {s}")
