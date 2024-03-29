from PIL import Image

from type import Type

class Pokemon:
    def __init__(self, index, name, types):
        self.index = index
        self.name = name
        self.types = [Type.get_type(x) for x in types]
        self.lvl_moves = []
        self.cur_moves = []
        self.weak_to = None

    def add_move(self, level, move):
        self.lvl_moves.append((level, move))

    def is_weak_to(self):
        if self.weak_to is None:
            self.weak_to = Type.is_weak_to(self.types) 
        return self.weak_to

    def get_gif(self):
        gif_image = Image.open(f"animations/{self.name}.gif")
        return gif_image
    
    def __repr__(self):
        return self.name
