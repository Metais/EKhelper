from classes.type import Type, get_physical_types


def get_move_power(source_pkmn, target_pkmn, source_pokemon_move, spm_power, move_effectiveness):
    # Check if BP is an standard value or not
    if not isinstance(spm_power, int):
        # For variable/unique power moves, do unique behavior
        if source_pokemon_move.name == "Sonicboom":
            return 20 if move_effectiveness != 0 else 0
        if source_pokemon_move.name == "Night Shade":
            return source_pkmn.lvl if move_effectiveness != 0 else 0
        elif source_pokemon_move.name == "Dragon Rage":
            return 40
        elif source_pokemon_move.name == "Seismic Toss":
            return source_pkmn.lvl
        # For others (such as status moves) skip
        else:
            return 0
        
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

        # Huge power always doubles the atk
        if source_pkmn.ability.name in ["Huge Power", "Pure Power"]:
            atk_stat *= 2
        # Hustle ups atk by 50% but accuracy down 20%
        if source_pkmn.ability.name == "Hustle":
            atk_stat *= 1.5
        # Thick fat ability halves fire and ice atk/spa stat
        if target_pkmn.ability.name == "Thick Fat" and (source_pokemon_move.type == Type.Fire or source_pokemon_move.type == Type.Ice):
            atk_stat /= 2
        # Selfdestruct/Explosion halves foe's defense stat
        if source_pokemon_move.name in ["Selfdestruct", "Explosion"]:
            def_stat /= 2  

        spm_power *= atk_stat / def_stat
    else:
        # Assume 31 (strongest) if unknown (aka, foe's)
        spa_iv = source_pkmn.spa_iv if source_pkmn.spa_iv != -1 else 31
        spd_iv = target_pkmn.spd_iv if target_pkmn.spd_iv != -1 else 31

        spa_stat = source_pkmn.get_real_spa_stat(spa_iv)
        spd_stat = target_pkmn.get_real_spd_stat(spd_iv)

        # Thick fat ability halves fire and ice atk/spa stat
        if target_pkmn.ability.name == "Thick Fat" and (source_pokemon_move.type == Type.Fire or source_pokemon_move.type == Type.Ice):
            spa_stat /= 2

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

    return spm_power


def apply_ability_on_effectiveness(source_pokemon_move, target_pkmn, move_effectiveness):
    if target_pkmn.ability.name == "Flash Fire" and source_pokemon_move.type == Type.Fire:
        move_effectiveness = 0
    elif target_pkmn.ability.name == "Levitate" and source_pokemon_move.type == Type.Ground:
        move_effectiveness = 0
    elif target_pkmn.ability.name == "Volt Absorb" and source_pokemon_move.type == Type.Electric:
        move_effectiveness = 0
    elif target_pkmn.ability.name == "Water Absorb" and source_pokemon_move.type == Type.Water:
        move_effectiveness = 0
    elif target_pkmn.ability.name == "Soundproof" and source_pokemon_move.name in ["Grasswhistle", "Growl", "Heal Bell", "Hyper Voice", 
                                                                                    "Metal Sound", "Perish Song", "Sing", "Sonicboom", 
                                                                                    "Supersonic", "Screech", "Snore", "Uproar"]:
        move_effectiveness = 0
    elif target_pkmn.ability.name == "Wonder Guard" and move_effectiveness < 2:
        move_effectiveness = 0
    return move_effectiveness


def get_move_details(source_pkmn, target_pkmn):
    # [(Move, 59), (Move2, 36), (Move3, 19)]  (Move4 is non-damaging)
    moves = []

    # For each move
    for source_pokemon_move in [move for move in source_pkmn.cur_moves if move.power != "N/A"]:
        move_effectiveness = Type.type_effectiveness_against_types(source_pokemon_move.type, target_pkmn.types)
        move_effectiveness = apply_ability_on_effectiveness(source_pokemon_move, target_pkmn, move_effectiveness)

        spm_power = source_pokemon_move.power
        # Magnitude's power can range from 10 to 150. Take 150 and adjust in the GUI by dividing lower bound by 15
        if source_pokemon_move.name == "Magnitude":
            spm_power = 150
        spm_power = get_move_power(source_pkmn, target_pkmn, source_pokemon_move, spm_power, move_effectiveness)

        moves.append((source_pokemon_move, spm_power))

    moves = sorted(moves, key=lambda x: x[1], reverse=True)

    # For any moves not included (status moves, weird moves, etc.), add to end with power=0
    processed_moves = [move.name for move, _ in moves]
    [moves.append((x, 0)) for x in source_pkmn.cur_moves if x.name not in processed_moves]

    return moves