from read_files import *
from type import *

from pokemonbattleGUI import pokemon_battle_gui
from pokemondata.Gen3Save import Gen3Save


def find_highest_damaging_move(source_pkmn, target_pkmn):
    strongest_move = None
    strongest_power = 0

    # Find the highest damaging move...
    for source_pokemon_move in [move for move in source_pkmn.cur_moves if move.power != "N/A"]:
        spm_power = source_pokemon_move.power

        # For variable/unique power moves, skip. TODO: find a way to save/record this
        if not isinstance(spm_power, int):
            continue

        # Following calcs taken from https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_III (not exhaustive!)
        # Multiply move power by its effectiveness against target pokemon type
        spm_power = int(spm_power) * Type.type_effectiveness_against_types(source_pokemon_move.type, target_pkmn.types)
        # Multiply move power by STAB (if present)
        if source_pokemon_move.type in source_pkmn.types:
            spm_power = spm_power * 1.5
        # Multiply level-based (0.4*lvl + 2)
        spm_power = spm_power * (0.4 * float(source_pkmn.lvl) + 2)
        # Take predicted (special) attack (for attacker) and (special) defense (for defender) into account
        # Assumes pokemon same level
        # Does not consider natures (TODO)
        if source_pokemon_move.category == "Physical":
            spm_power *= source_pkmn.base_atk / target_pkmn.base_def
        elif source_pokemon_move.category == "Special":
            spm_power *= source_pkmn.base_sa / target_pkmn.base_sd
        else:
            raise Exception(f"Damaging move {source_pokemon_move} is not Phys/Spec but {source_pokemon_move.category}")
        # Divide by 50 for real damage value
        spm_power = spm_power / 50

        # Compare with other moves and replace if strongest
        if strongest_move is None or spm_power > strongest_power:
            strongest_move = source_pokemon_move
            strongest_power = spm_power

    return strongest_move, int(strongest_power)


moves = read_moves_sheet("data/gen3moves.xlsx")
pokemons = read_pokemon_sheet("data/pokemon.xlsx", moves)
box = read_box(pokemons, moves)

save = Gen3Save("D:\Pokemon\emerald kaizo\Pokemon - Emerald Version (U).sav")

with open('EK Mastersheet.txt', 'r') as f:
    lines = f.readlines()
    while True:
        line_number = int(input("Enter line number at which trainer starts: "))

        print(f"Helping you fight '{lines[line_number - 1].strip()}'!")
    
        trainer_pokemon = read_trainer_pokemon(lines, line_number, pokemons, moves)

        # List with each index the corresponding enemy pokemon analysis
        enemy_team_info = []

        # For each enemy pokemon...
        for enemy_pokemon in trainer_pokemon:
            enemy_pokemon_analysis = {}

            # For each of my pokemon...
            for box_pokemon in box:
                # Strongest move against me
                strongest_move_against_me, strongest_power_against_me = find_highest_damaging_move(enemy_pokemon, box_pokemon)
                # Strongest move against him
                strongest_move_against_him, strongest_power_against_him = find_highest_damaging_move(box_pokemon, enemy_pokemon)
                
                # Store above 4 values per box pokemon for each enemy pokemon
                enemy_pokemon_analysis[box_pokemon.name] = (strongest_move_against_me, strongest_power_against_me, 
                                                            strongest_move_against_him, strongest_power_against_him)
                
            enemy_team_info.append((enemy_pokemon.name, enemy_pokemon_analysis))

        pokemon_battle_gui(enemy_team_info)
