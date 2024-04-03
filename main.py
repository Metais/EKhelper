from read_files import *
from type import *

from pokemonbattleGUI import pokemon_battle_gui
from pokemondata.Gen3Save import Gen3Save


with open('config.txt', 'r') as f:
    save_loc = f.readline().strip().split('=')[1]
    save = Gen3Save(save_loc)
    

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
        # Take (special) attack (for attacker) and (special) defense (for defender) into account
        if source_pokemon_move.category == "Physical":
            # Assume 31 (strongest) if unknown (aka, foe's)
            atk_iv = source_pkmn.atk_iv if source_pkmn.atk_iv != -1 else 31
            def_iv = target_pkmn.def_iv if target_pkmn.def_iv != -1 else 31

            atk_stat = source_pkmn.get_real_atk_stat(atk_iv)
            def_stat = target_pkmn.get_real_def_stat(def_iv)

            spm_power *= atk_stat / def_stat
        elif source_pokemon_move.category == "Special":
            # Assume 31 (strongest) if unknown (aka, foe's)
            spa_iv = source_pkmn.spa_iv if source_pkmn.spa_iv != -1 else 31
            spd_iv = target_pkmn.spd_iv if target_pkmn.spd_iv != -1 else 31

            spa_stat = source_pkmn.get_real_spa_stat(spa_iv)
            spd_stat = target_pkmn.get_real_spd_stat(spd_iv)

            spm_power *= spa_stat / spd_stat
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
items = read_items("data/items.csv")
my_pokemons = read_my_pokemon(save, pokemons, moves)

with open('EK Mastersheet.txt', 'r') as f:
    lines = f.readlines()
    while True:
        line_number = int(input("Enter line number at which trainer starts: "))

        print(f"Helping you fight '{lines[line_number - 1].strip()}'!")
    
        trainer_pokemon = read_trainer_pokemon(lines, line_number, pokemons, moves, items)

        # Store my pokemon's variable moves
        my_variable_moves = {}
        for my_pokemon in my_pokemons:
            my_variable_moves[my_pokemon.name] = [move for move in my_pokemon.cur_moves if move.power != "N/A" and not isinstance(move.power, int)]

        # List with each index the corresponding enemy pokemon analysis
        enemy_team_info = []
        his_moves = []
        his_variable_moves = []

        # For each enemy pokemon...
        for enemy_pokemon in trainer_pokemon:
            # Each enemy pokemon has a dictionary containing my pokemon's names as keys
            # except the key/value pair 'variable', which stores the pokemon's variables moves
            enemy_pokemon_analysis = {}

            his_moves.append([move for move in enemy_pokemon.cur_moves])
            his_variable_moves.append([move for move in enemy_pokemon.cur_moves if move.power != "N/A" and not isinstance(move.power, int)])

            # For each of my pokemon...
            for my_pokemon in my_pokemons:
                # Strongest move against me
                strongest_move_vs_me, strongest_power_vs_me = find_highest_damaging_move(enemy_pokemon, my_pokemon)
                # Strongest move against him
                strongest_move_vs_him, strongest_power_vs_him = find_highest_damaging_move(my_pokemon, enemy_pokemon)
                # Who goes first (0 = me, 1 = him) (assume foe's speed stat is max IV)
                goes_first = 0 if my_pokemon.get_real_spe_stat(my_pokemon.spe_iv) > enemy_pokemon.get_real_spe_stat(31) else 1
                
                # Store above 5 values per box pokemon for each enemy pokemon
                enemy_pokemon_analysis[my_pokemon.name] = (strongest_move_vs_me, strongest_power_vs_me, 
                                                            strongest_move_vs_him, strongest_power_vs_him,
                                                            goes_first)
                
            enemy_team_info.append((enemy_pokemon, enemy_pokemon_analysis))

        pokemon_battle_gui(enemy_team_info, my_pokemons, his_moves, his_variable_moves, my_variable_moves)
