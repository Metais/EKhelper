import unicodedata
from classes.type import Type, get_physical_types

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        image_path_name = self.remove_accents(name)
        image_path_name = image_path_name.lower().replace(' ', '-').replace("'", "")
        self.image_path = f'images/items/{image_path_name}.gif'

    def remove_accents(self, input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    def get_held_item_multiplier(self, pokemon, move):        
        match self.name:
            case "Black Belt":
                return 1.1 if move.type == Type.Fighting else 1
            case "BlackGlasses":
                return 1.1 if move.type == Type.Dark else 1
            case "Charcoal":
                return 1.1 if move.type == Type.Fire else 1
            case "Choice Band":
                return 1.5 if move.type in get_physical_types() else 1
            case "DeepSeaTooth":
                return 2 if pokemon.name == "Clamperl" and move.category == "Special" else 1
            case "Dragon Fang":
                return 1.1 if move.type == Type.Dragon else 1
            case "Hard Stone":
                return 1.1 if move.type == Type.Rock else 1
            case "Light Ball":
                return 2 if pokemon.name == "Pikachu" and move.category == "Special" else 1
            case "Magnet":
                return 1.1 if move.type == Type.Electric else 1
            case "Metal Coat":
                return 1.1 if move.type == Type.Steel else 1
            case "Miracle Seed":
                return 1.1 if move.type == Type.Grass else 1
            case "Mystic Water":
                return 1.1 if move.type == Type.Water else 1
            case "NeverMeltIce":
                return 1.1 if move.type == Type.Ice else 1
            case "Poison Barb":
                return 1.1 if move.type == Type.Poison else 1
            case "Sea Incense":
                return 1.05 if move.type == Type.Water else 1
            case "Sharp Beak":
                return 1.1 if move.type == Type.Flying else 1
            case "Silk Scarf":
                return 1.1 if move.type == Type.Normal else 1
            case "SilverPowder":
                return 1.1 if move.type == Type.Bug else 1
            case "Soft Sand":
                return 1.1 if move.type == Type.Ground else 1
            case "Soul Dew":
                return 1.1 if pokemon.name == "Latias" and move.category == "Special" else 1
            case "Spell Tag":
                return 1.1 if move.type == Type.Ghost else 1
            case "Thick Club":
                return 2 if pokemon.name in ["Cubone", "Marowak"] and move.category == "Physical" else 1
            case "TwistedSpoon":
                return 1.1 if move.type == Type.Psychic else 1
            case _:
                return 1


    def __str__(self):
        return f'{self.name}: {self.description}'

    def __repr__(self):
        return self.name