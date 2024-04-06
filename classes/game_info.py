from read_files import *

# Storage class for all static data
class GameInfo:
    def __init__(self):
        self.moves = read_moves_sheet()
        self.abilities = read_abilities()
        self.pokemons = read_pokemon_file(self.moves, self.abilities)
        self.items = read_items()
        
