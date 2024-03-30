import openpyxl
import re

from pokemon import Pokemon
from move import Move

def read_moves_sheet(workbook):
    moves = {}
    moves_sheet = openpyxl.load_workbook(workbook).active
    
    for row in moves_sheet.iter_rows(min_row=2, values_only=True):
        name, description, type, pp, power, acc, category = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        if acc != 'N/A':
            acc = str(int(acc) * 100) + '%'
        moves[name.lower()] = Move(name, description, type, pp, power, acc, category)

    return moves


def read_pokemon_sheet(workbook, moves):
    pokemons = {}
    pokemon_sheet = openpyxl.load_workbook(workbook).active
    
    # Establish the collection of pokemon
    for row in pokemon_sheet.iter_rows(min_row=3, values_only=True):
        index = row[0]
        name = row[1]
        base_hp, base_atk, base_def, base_sa, base_sd, base_spd = row[2], row[3], row[4], row[5], row[6], row[7]
        types = [x for x in row[8:] if x is not None]

        # Create a Pokemon object and store it in the dictionary
        pokemons[name] = Pokemon(index, name, types, base_hp, base_atk, base_def, base_sa, base_sd, base_spd)

    # Add level moves to the pokemon
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
                pokemons[cur_pokemon].add_level_move(level, move)

    return pokemons


def read_box(pokemons, moves):
    with open('current_box.txt', 'r') as f:
        box_pokemons = []
        
        for line in f.readlines():
            splitted = line.strip().split('|')
            pokemon_name = splitted[0]
            pokemon_level = int(splitted[1])
            pokemon_moves = splitted[2].split(',')
            
            pokemon = pokemons[pokemon_name]
            pokemon.lvl = pokemon_level
            for pokemon_move in pokemon_moves:
                pokemon.add_cur_move(moves[pokemon_move])

            box_pokemons.append(pokemon)

        return box_pokemons
    
def read_trainer_pokemon(lines, line_number, pokemons, moves):
    trainer_pokemon = []

    # Trainer info exists until whiteline
    while lines[line_number] != '\n':
        pokemon_line = lines[line_number].strip()

        # Get pokemon name
        pokemon_name = "" 
        for char in pokemon_line:
            if char == '(' or char == ' ':
                break
            pokemon_name += char
        
        # Make an exception for nidoran(m)/nidoran(f)
        if pokemon_name == "Nidoran":
            pokemon_name = pokemon_line.split(' ')[0]

        pokemon = pokemons[pokemon_name]

        pattern = r"Lv\.(\d+)\s"
        match = re.search(pattern, pokemon_line)
        pokemon_level = match.group(1)
        pokemon.lvl = pokemon_level

        pokemon_moves = pokemon_line.split(': ')[1].split(', ')
        pokemon_moves[3] = pokemon_moves[3].split(' [')[0].split(' +')[0]  # Last move has extra fluff info to the right
        pokemon_moves = [x for x in pokemon_moves if x != '-----']
        pokemon_moves = [moves[x.lower()] for x in pokemon_moves]
        pokemon.cur_moves = pokemon_moves

        trainer_pokemon.append(pokemon)
        line_number += 1

    return trainer_pokemon
