import openpyxl

from pokemon import Pokemon
from move import Move

def read_moves_sheet(workbook):
    moves = {}
    moves_sheet = openpyxl.load_workbook(workbook).active
    
    for row in moves_sheet.iter_rows(min_row=2, values_only=True):
        name, description, type, pp, power, acc = row[0], row[1], row[2], row[3], row[4], row[5]
        if acc != 'N/A':
            acc = str(int(acc) * 100) + '%'
        moves[name.lower()] = Move(name, description, type, pp, power, acc)

    return moves


def read_pokemon_sheet(workbook, moves):
    pokemons = {}
    pokemon_sheet = openpyxl.load_workbook(workbook).active
    
    # Establish the collectin of pokemon
    for row in pokemon_sheet.iter_rows(min_row=3, values_only=True):
        index = row[0]
        name = row[1]
        types = [x for x in row[2:] if x is not None]

        # Create a Pokemon object and store it in the dictionary
        pokemons[name] = Pokemon(index, name, types)

    # Add moves to the pokemon
    with open('EK learnsets.txt', 'r') as f:
        next = True
        cur_pokemon = 'Bulbasaur'

        for line in f.readlines():
            parts = [x for x in line.strip().split(' ') if x and x != '\t']
            # Transition between pokemon
            if line == '\n':
                next = True
            # New pokemon
            elif next:
                cur_pokemon = ' '.join(parts[1:])
                next = False
            # Pokemon move
            elif line.startswith('Lv. '):
                level = int(parts[1])
                move = moves[' '.join(parts[2:]).lower()]
                pokemons[cur_pokemon].add_move(level, move)

    return pokemons

def read_box():
    with open('current_box.txt', 'r') as f:
        pokemon = []
        
        for line in f.readlines():

            