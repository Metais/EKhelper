from read_files import *

# Storage class for all static data
class GameInfo:
    def __init__(self):
        self.moves = read_moves_sheet()
        self.pokemons = read_pokemon_sheet(self.moves)
        self.items = read_items()
        self.abilities = read_abilities()
