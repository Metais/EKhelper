import tkinter as tk

from game_info import GameInfo
from trainerselectionGUI import TrainerSelectionGUI
from read_files import read_my_pokemon

# TODO: Add enemy pokemon abilities
# TODO: Add badge boosts
# TODO: Add weather effects

game_info = GameInfo()
my_pokemons = read_my_pokemon(game_info)

root = tk.Tk()
app = TrainerSelectionGUI(root, game_info, my_pokemons)
root.mainloop()
