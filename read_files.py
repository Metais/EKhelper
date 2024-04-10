import openpyxl
import re
import copy
import csv
import json

from classes.pokemon import Pokemon
from classes.move import Move
from classes.nature import Nature
from classes.item import Item
from classes.ability import Ability
from pokemondata.Gen3Save import Gen3Save

def read_moves_sheet():
    moves = {}
    moves_sheet = openpyxl.load_workbook("data/gen3moves.xlsx").active
    
    for row in moves_sheet.iter_rows(min_row=2, values_only=True):
        name, description, type, pp, power, acc, category = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
        if acc != 'N/A':
            acc = str(acc * 100) + '%'
        moves[name.lower()] = Move(name, description, type, pp, power, acc, category)

    return moves


def read_pokemon_file(moves, abilities):
    pokemons = {}

    with open('data/pokemons.json', 'r', encoding='utf-8') as f:
        pokemon_data = json.load(f)

        for pokemon_name, pokemon in pokemon_data.items():
            poke_abilities = []
            for ability in pokemon["Abilities"]:
                if ability.lower() in abilities:
                    poke_abilities.append(abilities[ability.lower()])
                else:
                    poke_abilities.append(Ability(ability, "Undefined"))

            # Create a Pokemon object and store it in the dictionary
            pokemons[pokemon_name] = Pokemon(pokemon_name, pokemon["Types"], poke_abilities, pokemon["Base Stats"])

    # Add level moves to the pokemon
    with open('data/EK learnsets.txt', 'r') as f:
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


def read_items():
    items = {}
    
    with open("data/items.csv", 'r') as f:
        csvreader = csv.reader(f, delimiter=';')
        for i, row in enumerate(csvreader):
            if i == 0:
                continue

            items[row[0].lower()] = Item(row[0], row[1])

    return items


def read_abilities():
    abilities = {}

    with open('data/abilities.json', 'r') as f:
        ability_data = json.load(f)

        for key, value in ability_data.items():
            abilities[key.lower()] = Ability(key, value)

    return abilities


def handle_move_name_exceptions(move):
    # hard-code move name differences between save file and data files (...annoying)
    match move:
        case "bubble beam":
            return "bubblebeam"
        case "smelling salts":
            return "smellingsalt"
        case "sand attack":
            return "sand-attack"
        case "arm thrust":
            return "force palm"
        case "thunder shock":
            return "thundershock"
        case "sonic boom":
            return "sonicboom"
        case "metal sound":
            return "flash cannon"
        case "spark":
            return "wild charge"
        case "ancient power":
            return "ancientpower"
        case "soft-boiled":
            return "softboiled"
        case "icicle spear":
            return "ice shard"
        case _:
            raise Exception(f'Move name {move} has wrong syntax. Add to handle_move_name_exceptions()')


def read_my_pokemon(game_info):
    # Read save file
    with open('config.txt', 'r') as f:
        save_loc = f.readline().strip().split('=')[1]
        save = Gen3Save(save_loc)

    my_pokemon = []
    
    for gen3pokemon in save.team + save.boxes:
        pokemon = copy.copy(game_info.pokemons[gen3pokemon.species['name']])
        pokemon.lvl = gen3pokemon.level
        pokemon.nature = Nature.get_nature(gen3pokemon.nature)
        pokemon.ability = pokemon.abilities[0]

        if len(pokemon.abilities) == 2 and gen3pokemon.ability[-1] == 1:
            pokemon.ability = pokemon.abilities[1]

        # IVs
        pokemon.hp_iv = gen3pokemon.ivs['hp']
        pokemon.atk_iv = gen3pokemon.ivs['attack']
        pokemon.def_iv = gen3pokemon.ivs['defence']
        pokemon.spa_iv = gen3pokemon.ivs['spatk']
        pokemon.spd_iv = gen3pokemon.ivs['spdef']
        pokemon.spe_iv = gen3pokemon.ivs['speed']

        for move in gen3pokemon.moves:
            if move['name'].lower() in game_info.moves:
                pokemon.add_cur_move(game_info.moves[move['name'].lower()])
            else:
                modified_move_name = handle_move_name_exceptions(move['name'].lower())
                pokemon.add_cur_move(game_info.moves[modified_move_name])
        
        my_pokemon.append(pokemon)
        
    return my_pokemon


def read_trainer_pokemon_from_json(trainer_name, game_info):
    with open('data/trainers.json', 'r', encoding='utf-8') as f:
        trainer_pokemon_names = json.load(f)[trainer_name]

    trainer_pokemons = []

    with open('data/trainer_pokemon.json', 'r', encoding='utf-8') as f:
        pokemon_to_trainer = json.load(f)
        for trainer_pokemon_name in trainer_pokemon_names:
            trainers_with_pokemon = pokemon_to_trainer[trainer_pokemon_name]

            # Append (#) to trainer pokemon name if they have more than 1 of the same pokemon
            if len([x for x in trainer_pokemon_names if x == trainer_pokemon_name]) > 1:
                # Check how many already recorded
                already_in = len([x for x in trainer_pokemons if x.name == trainer_pokemon_name])
                pokemon_json = trainers_with_pokemon[f'{trainer_name} ({already_in + 1})']
            else:
                pokemon_json = trainers_with_pokemon[trainer_name]
            
            pokemon = copy.copy(game_info.pokemons[trainer_pokemon_name])
            pokemon.lvl = pokemon_json['level']
            pokemon.ability = game_info.abilities[pokemon_json['ability'].lower()]
            pokemon.nature = Nature.get_nature(pokemon_json['nature'])
            pokemon.cur_moves = [game_info.moves[x.lower()] for x in pokemon_json['moves']]

            if 'item' in pokemon_json:
                pokemon.held_item = game_info.items[pokemon_json['item'].lower()]

            # If IV's not present, they are all 31
            if 'ivs' in pokemon_json:
                ivs = pokemon_json['ivs']
                pokemon.hp_iv, pokemon.atk_iv, pokemon.def_iv = ivs['hp'], ivs['at'], ivs['df']
                pokemon.spa_iv, pokemon.spd_iv, pokemon.spe_iv = ivs['sa'], ivs['sd'], ivs['sp']
            else:
                pokemon.hp_iv, pokemon.atk_iv, pokemon.def_iv = 31, 31, 31
                pokemon.spa_iv, pokemon.spd_iv, pokemon.spe_iv = 31, 31, 31

            trainer_pokemons.append(pokemon)

        return trainer_pokemons


# Deprecated -- now reads trainer pokemon from json
def read_trainer_pokemon(lines, line_number, pokemons, moves, items):
    trainer_pokemon = []

    # Trainer info exists until whiteline
    while lines[line_number] != '\n' and not lines[line_number].isspace():
        pokemon_line = lines[line_number].strip()

        # Get pokemon name
        pokemon_name = "" 
        for char in pokemon_line:
            if char == '(' or char == ' ':
                break
            pokemon_name += char
        
        # Make an exception for nidoran(m)/nidoran(f)
        if pokemon_name.lower() == "nidoran":
            pokemon_name = pokemon_line.split(' ')[0]

        # Sometimes written in all-caps
        pokemon_name = pokemon_name.capitalize()

        # Mr. Mime is the only pokemon with a space, which it reads wrong
        if pokemon_name == "Mr.":
            pokemon_name = "Mr. Mime"

        pokemon = copy.copy(pokemons[pokemon_name])

        # Get its level
        pattern = r"Lv\.(\d+)[\s:]"
        match = re.search(pattern, pokemon_line)
        pokemon_level = match.group(1)
        pokemon.lvl = int(pokemon_level)

        # Get its held item (if present)
        if "@" in pokemon_line:
            pattern = r'@([^:]+):'
            match = re.search(pattern, pokemon_line)
            pokemon.held_item = items[match.group(1).lower()]

        # Get its moves
        pokemon_moves = pokemon_line.split(': ')[1].split(', ')
        pokemon_moves[3] = pokemon_moves[3].split(' [')[0].split(' +')[0]  # Last move has extra fluff info to the right
        pokemon_moves = [x for x in pokemon_moves if x != '-----']
        pokemon_moves = [moves[x.lower()] for x in pokemon_moves]
        pokemon.cur_moves = pokemon_moves

        # Get its nature (if present)
        for nature in Nature.get_nature_names():
            if f'{nature}]' in pokemon_line:
                pokemon.nature = Nature.get_nature(nature)
                break

        trainer_pokemon.append(pokemon)
        line_number += 1

    return trainer_pokemon
