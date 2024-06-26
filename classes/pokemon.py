from PIL import Image
from classes.type import Type
from math import floor
from classes.nature import Nature

class Pokemon:
    def __init__(self, name, types, abilities, base_stats):
        self.name = name
        self.types = [Type.get_type(x) for x in types]
        self.abilities = abilities
        self.base_hp = base_stats[0]
        self.base_atk = base_stats[1]
        self.base_def = base_stats[2]
        self.base_spa = base_stats[3]
        self.base_spd = base_stats[4]
        self.base_spe = base_stats[5]

        # Assign later for specific instances
        self.lvl = 0
        self.nature = None
        self.lvl_moves = []
        self.cur_moves = []
        self.held_item = None
        self.ability = None

        # IVs (only known for own pokemon)
        self.hp_iv = -1
        self.atk_iv = -1
        self.def_iv = -1
        self.spa_iv = -1
        self.spd_iv = -1
        self.spe_iv = -1

        # Types vs me
        self.immune_to = None
        self.very_resistant_to = None
        self.resistant_to = None
        self.normal_to = None
        self.vulnerable_to = None
        self.very_vulnerable_to = None

    def __copy__(self):
        return Pokemon(self.name, [x.name for x in self.types], self.abilities,
                       [self.base_hp, self.base_atk, self.base_def, self.base_spa, self.base_spd, self.base_spe])

    def get_real_hp_stat(self, hp_iv):
        return floor((2 * self.base_hp + hp_iv) * self.lvl / 100) + self.lvl + 10
    
    def get_real_atk_stat(self, atk_iv):
        nature_modifier = Nature.get_nature_modifier(self.nature, "atk")
        return floor((floor((2 * self.base_atk + atk_iv) * self.lvl / 100) + 5) * nature_modifier)
    
    def get_real_def_stat(self, def_iv):
        nature_modifier = Nature.get_nature_modifier(self.nature, "def")
        return floor((floor((2 * self.base_def + def_iv) * self.lvl / 100) + 5) * nature_modifier)
    
    def get_real_spa_stat(self, spa_iv):
        nature_modifier = Nature.get_nature_modifier(self.nature, "spa")
        return floor((floor((2 * self.base_spa + spa_iv) * self.lvl / 100) + 5) * nature_modifier)
    
    def get_real_spd_stat(self, spd_iv):
        nature_modifier = Nature.get_nature_modifier(self.nature, "spd")
        return floor((floor((2 * self.base_spd + spd_iv) * self.lvl / 100) + 5) * nature_modifier)
    
    def get_real_spe_stat(self, spe_iv):
        nature_modifier = Nature.get_nature_modifier(self.nature, "spe")
        return floor((floor((2 * self.base_spe + spe_iv) * self.lvl / 100) + 5) * nature_modifier)

    # For if IV is unknown
    def print_estimated_stats(self):
        low_hp, high_hp = self.get_real_hp_stat(0), self.get_real_hp_stat(31)
        low_atk, high_atk = self.get_real_atk_stat(0), self.get_real_atk_stat(31)
        low_def, high_def = self.get_real_def_stat(0), self.get_real_def_stat(31)
        low_spa, high_spa = self.get_real_spa_stat(0), self.get_real_spa_stat(31)
        low_spd, high_spd = self.get_real_spd_stat(0), self.get_real_spd_stat(31)
        low_spe, high_spe = self.get_real_spe_stat(0), self.get_real_spe_stat(31)

        basics = f"Lv. {self.lvl} {self.name} ({self.types[0].name}"
        if len(self.types) > 1:
            basics += f"+{self.types[1].name})"
        else:
            basics += ")"

        return f"{basics}\nEstimated stats:\nHp: {low_hp}-{high_hp}\nAttack: {low_atk}-{high_atk}\nDefense: {low_def}-{high_def}\n" + \
            f"Special Attack: {low_spa}-{high_spa}\nSpecial Defense: {low_spd}-{high_spd}\nSpeed: {low_spe}-{high_spe}"
    
    # For if IV is known
    def print_current_stats(self, with_ability=False):
        hp = self.get_real_hp_stat(self.hp_iv)
        atk = self.get_real_atk_stat(self.atk_iv)
        df = self.get_real_def_stat(self.def_iv)
        spa = self.get_real_spa_stat(self.spa_iv)
        spd = self.get_real_spd_stat(self.spd_iv)
        spe = self.get_real_spe_stat(self.spe_iv)

        basics = f"Lv. {self.lvl} {self.name} ({self.types[0].name}"
        if len(self.types) > 1:
            basics += f"+{self.types[1].name})"
        else:
            basics += ")"

        if with_ability:
            basics += f"\nAbility: {self.ability.name} - {self.ability.description}"

        return f"{basics}\nCurrent stats:\nHp: {hp}\nAttack: {atk}\nDefense: {df}\nSpecial Attack: {spa}\nSpecial Defense: {spd}\nSpeed: {spe}"

    def add_level_move(self, level, move):
        self.lvl_moves.append((level, move))

    def add_cur_move(self, move):
        self.cur_moves.append(move)
    
    def remove_cur_move(self, move_name):
        self.cur_moves = [x for x in self.cur_moves if str(x) != move_name]

    def get_effective_to(self):
        effectivities = Type.effectivity_against(self.types)
        self.immune_to, self.very_resistant_to, self.resistant_to = effectivities[0], effectivities[1], effectivities[2]
        self.normal_to, self.vulnerable_to, self.very_vulnerable_to = effectivities[3], effectivities[4], effectivities[5]

    def is_immune_to(self):
        if self.immune_to is None:
            self.get_effective_to()
        return self.immune_to

    def is_very_resistant_to(self):
        if self.very_resistant_to is None:
            self.get_effective_to()
        return self.very_resistant_to
    
    def is_resistant_to(self):
        if self.resistant_to is None:
            self.get_effective_to()
        return self.resistant_to
    
    def is_normal_to(self):
        if self.normal_to is None:
            self.get_effective_to()
        return self.normal_to

    def is_vulnerable_to(self):
        if self.vulnerable_to is None:
            self.get_effective_to()
        return self.vulnerable_to
    
    def is_very_vulnerable_to(self):
        if self.vulnerable_to is None:
            self.get_effective_to()
        return self.very_vulnerable_to

    def get_gif(self):
        gif_image = Image.open(f"images/pokemons/{self.name}.gif")
        return gif_image
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
