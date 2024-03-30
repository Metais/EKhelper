from PIL import Image

from type import Type

class Pokemon:
    def __init__(self, index, name, types, base_hp, base_atk, base_def, base_sa, base_sd, base_spd):
        self.index = index
        self.name = name
        self.types = [Type.get_type(x) for x in types]
        self.base_hp = base_hp
        self.base_atk = base_atk
        self.base_def = base_def
        self.base_sa = base_sa
        self.base_sd = base_sd
        self.base_spd = base_spd

        self.lvl = 0
        
        self.lvl_moves = []
        self.cur_moves = []

        # Types vs me
        self.immune_to = None
        self.very_resistant_to = None
        self.resistant_to = None
        self.normal_to = None
        self.vulnerable_to = None
        self.very_vulnerable_to = None

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
        gif_image = Image.open(f"animations/{self.name}.gif")
        return gif_image
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
