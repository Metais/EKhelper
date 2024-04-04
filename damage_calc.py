from type import Type, get_physical_types

# Example return: (Bite(), 26)
def find_highest_damaging_move(source_pkmn, target_pkmn):
    strongest_move = None
    strongest_power = 0

    # Find the highest damaging move...
    for source_pokemon_move in [move for move in source_pkmn.cur_moves if move.power != "N/A"]:
        spm_power = source_pokemon_move.power
        move_effectiveness = Type.type_effectiveness_against_types(source_pokemon_move.type, target_pkmn.types)

        # Check if BP is an standard value or not
        if not isinstance(spm_power, int):
            # For variable/unique power moves, do unique behavior
            if source_pokemon_move.name == "Sonicboom":
                spm_power = 20 if move_effectiveness != 0 else 0
            elif source_pokemon_move.name == "Dragon Rage":
                spm_power = 40
            # For others (such as status moves) skip
            else:
                continue
        else:
            # Following calcs taken from https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_III (not exhaustive!)
            # Multiply level-based (0.4*lvl + 2)
            spm_power = spm_power * (0.4 * float(source_pkmn.lvl) + 2)
            # Gen 3 split between physical and special based on type
            if source_pokemon_move.type in get_physical_types():
                # Assume 31 (strongest) if unknown (aka, foe's)
                atk_iv = source_pkmn.atk_iv if source_pkmn.atk_iv != -1 else 31
                def_iv = target_pkmn.def_iv if target_pkmn.def_iv != -1 else 31

                atk_stat = source_pkmn.get_real_atk_stat(atk_iv)
                def_stat = target_pkmn.get_real_def_stat(def_iv)

                spm_power *= atk_stat / def_stat
                if source_pokemon_move.name == "Selfdestruct":
                    spm_power *= 2  # Selfdestruct halves foe's defense stat
            else:
                # Assume 31 (strongest) if unknown (aka, foe's)
                spa_iv = source_pkmn.spa_iv if source_pkmn.spa_iv != -1 else 31
                spd_iv = target_pkmn.spd_iv if target_pkmn.spd_iv != -1 else 31

                spa_stat = source_pkmn.get_real_spa_stat(spa_iv)
                spd_stat = target_pkmn.get_real_spd_stat(spd_iv)

                spm_power *= spa_stat / spd_stat
            # Divide by 50 for real damage value
            spm_power = spm_power / 50
            # Add 2
            spm_power += 2

            # --- End of large parenthesis (https://wikimedia.org/api/rest_v1/media/math/render/svg/6238dd5679302e5845374613828e184d95c65827) ---
            
            # Multiply move power by STAB (if present)
            if source_pokemon_move.type in source_pkmn.types:
                spm_power = spm_power * 1.5
            # Multiply move power by its effectiveness against target pokemon type
            spm_power = spm_power * move_effectiveness
            # Find held-item specific power changes
            if source_pkmn.held_item is not None:
                spm_power *= source_pkmn.held_item.get_held_item_multiplier(source_pkmn, source_pokemon_move)

        # Compare with other moves and replace if strongest
        if strongest_move is None or spm_power > strongest_power:
            strongest_move = source_pokemon_move
            strongest_power = spm_power

    return strongest_move, int(strongest_power)