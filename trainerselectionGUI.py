from tkinter import ttk

import tkinter as tk
import json

from read_files import read_my_pokemon

class TrainerSelectionGUI:
    def __init__(self, root, game_info, my_pokemons, selected_trainer=None):
        self.root = root
        self.game_info = game_info
        self.my_pokemons = my_pokemons

        self.root.title("Trainer Selection")
        self.root.iconbitmap("images/pokeball.ico")

        # Create the entry widget
        self.entry = ttk.Entry(root, width=60)
        self.entry.pack(pady=10)
        self.entry.bind('<KeyRelease>', self.on_key_release)

        # Create the listbox widget
        self.lb = tk.Listbox(root, width=50, height=30)
        self.lb.pack(expand=True, side=tk.LEFT)

        # Add scrollbar to the Listbox
        scrollbar = tk.Scrollbar(root, orient="vertical", command=self.lb.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lb.config(yscrollcommand=scrollbar.set)

        # Bind the selection event to the Listbox
        self.lb.bind('<<ListboxSelect>>', self.on_select)

        # Load the trainers from JSON file
        with open(f'data/trainers.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.trainers = list(data.keys())

        # Add options to the Listbox
        for i, trainer in enumerate(self.trainers, start=1):
            self.lb.insert(tk.END, f'{i}: {trainer}')
        
        # Highlight last-selected trainer if it exists
        with open(f'data/save.txt', 'r') as f:
            save_line = f.readline()

            # If not a previously selected trainer, it's startup, attempt from save file
            if not selected_trainer and save_line and save_line != "":
                selected_trainer = save_line.strip()

        if selected_trainer:
            self.selected_trainer = selected_trainer
            selected_trainer_index = self.trainers.index(selected_trainer)
            self.lb.selection_set(selected_trainer_index)
            self.entry.insert(tk.END, selected_trainer)

            # Scroll listbox down to last selected trainer
            self.lb.yview_scroll(selected_trainer_index, 'units')
                    
        # Create a button to switch to the battle window
        self.battle_button = ttk.Button(root, text="Go to Battle", command=self.switch_to_battle)
        self.battle_button.pack(side=tk.TOP, pady=0)

        # Create a button to reload the save
        self.reload_save_button = ttk.Button(root, text="Reload Save", command=self.reload_save)
        self.reload_save_button.pack(side=tk.TOP, pady=10)

    def on_key_release(self, event):
        # Get the current text in the Entry widget
        value = event.widget.get()
        value = value.strip().lower()

        # Remove all the values in the listbox
        self.lb.delete(0, tk.END)

        # Add matching values to the listbox
        for i, trainer in enumerate(self.trainers, start=1):
            # Filter on number
            if value.isdigit() and i == int(value):
                self.lb.insert(tk.END, f'{i}: {trainer.encode("latin1").decode("utf-8")}')

            # Filter on text
            if value in trainer.lower():
                self.lb.insert(tk.END, f'{i}: {trainer.encode("latin1").decode("utf-8")}')
        
    def on_select(self, event):
        # Get the selected item from the listbox
        selected = self.lb.curselection()
        if selected:
            self.selected_index = selected[0]
            self.selected_trainer = ' '.join(self.lb.get(self.selected_index).split(' ')[1:])
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.selected_trainer)

    def switch_to_battle(self):
        # Don't switch if demarcated entry is selected that signifies location in map
        if self.selected_trainer.startswith('* '):
            return

        # Lazy import
        from pokemonbattleGUI import PokemonBattleGUI
        # Destroy the current window and switch to the battle window
        self.root.destroy()
        root = tk.Tk()
        app = PokemonBattleGUI(root, self.selected_trainer, self.game_info, self.my_pokemons)
        root.mainloop()

    def reload_save(self):
        self.my_pokemons = read_my_pokemon(self.game_info)
