import tkinter as tk
from PIL import Image, ImageTk
from math import floor

class PokemonBattleGUI:
    def __init__(self, root, enemy_team_info, my_pokemons, his_variable_moves, my_variable_moves):
        self.root = root
        self.enemy_team_info = enemy_team_info
        self.my_pokemons = my_pokemons
        self.his_variable_moves = his_variable_moves
        self.my_variable_moves = my_variable_moves
        self.current_index = 0
        self.box_size = len(enemy_team_info[0][1].keys())

        self.enemy_pokemon_label = tk.Label(root)
        # Up to 4 variable move labels
        self.enemy_pokemon_variable_move_labels = [tk.Label(root, wraplength=500) for _ in range(4)]

        # My pokemon Image labels
        self.my_pokemon_vs_him_image_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.him_vs_my_pokemon_image_labels = [tk.Label(root) for _ in range(self.box_size)]

        # My pokemon Text labels
        self.my_pokemon_move_vs_him_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.enemy_pokemon_move_vs_me_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.my_pokemon_info_top = [tk.Label(root) for _ in range(self.box_size)]
        self.my_pokemon_info_bot = [tk.Label(root) for _ in range(self.box_size)]

        self.load_pokemon_images()
        self.display_current_pokemon_info()
        self.create_navigation_buttons()

    def load_pokemon_images(self):
        # Load enemy Pokemon image
        enemy_pokemon_image = Image.open(f"animations/{self.enemy_team_info[self.current_index][0]}.gif")
        enemy_pokemon_image = enemy_pokemon_image.resize((200, 200))
        self.enemy_pokemon_image = ImageTk.PhotoImage(enemy_pokemon_image)

        # Load enemy pokemon variable moves
        for i in range(4):
            self.enemy_pokemon_variable_move_labels[i].config(text="")
            if len(self.his_variable_moves[self.current_index]) > i:
                self.enemy_pokemon_variable_move_labels[i].config(text=self.his_variable_moves[self.current_index][i].detailed_string())

        # Load my Pokemon images and move info (me vs him)
        in_order = sorted(self.enemy_team_info[self.current_index][1].items(), key=lambda x: x[1][3], reverse=True)
        for i, (pokemon_name, move_info) in enumerate(in_order):
            pokemon_image = Image.open(f"animations/{pokemon_name}.gif")
            pokemon_image = pokemon_image.resize((100, 100))
            self.my_pokemon_vs_him_image_labels[i].image = ImageTk.PhotoImage(pokemon_image)

            move_name, move_power = move_info[2], move_info[3]
            move_text = f"{move_name}\nPower: {move_power}"
            self.my_pokemon_move_vs_him_labels[i].config(text=move_text)

            # Pokemon level and name
            pokemon_i = [x for x in self.my_pokemons if x.name == pokemon_name][0]
            self.my_pokemon_info_top[i].config(text=f"Lv. {pokemon_i.lvl} {pokemon_i.name}")
        
        # Load my Pokemon images and move info (him vs me)
        in_order = sorted(self.enemy_team_info[self.current_index][1].items(), key=lambda x: x[1][1])
        for i, (pokemon_name, move_info) in enumerate(in_order):
            pokemon_image = Image.open(f"animations/{pokemon_name}.gif")
            pokemon_image = pokemon_image.resize((100, 100))
            self.him_vs_my_pokemon_image_labels[i].image = ImageTk.PhotoImage(pokemon_image)

            move_name, move_power = move_info[0], move_info[1]
            move_text = f"{move_name}\nPower: {move_power}"
            self.enemy_pokemon_move_vs_me_labels[i].config(text=move_text)

            # Pokemon level and name
            pokemon_i = [x for x in self.my_pokemons if x.name == pokemon_name][0]
            self.my_pokemon_info_bot[i].config(text=f"Lv. {pokemon_i.lvl} {pokemon_i.name}")

    def display_current_pokemon_info(self):
        # Display enemy Pokemon image
        self.enemy_pokemon_label.config(image=self.enemy_pokemon_image)
        label_column = floor(self.box_size / 2) - 1
        label_column = label_column if label_column >= 0 else 0
        self.enemy_pokemon_label.grid(row=3, column=label_column, columnspan=2, rowspan=2)

        # Display enemy pokemon variable moves label
        self.enemy_pokemon_variable_move_labels[0].grid(row=0, rowspan=2, column=self.box_size, columnspan=1)
        self.enemy_pokemon_variable_move_labels[1].grid(row=2, rowspan=2, column=self.box_size, columnspan=1)
        self.enemy_pokemon_variable_move_labels[2].grid(row=4, rowspan=2, column=self.box_size, columnspan=1)
        self.enemy_pokemon_variable_move_labels[3].grid(row=6, rowspan=2, column=self.box_size, columnspan=1)

        # Display my Pokemon images and move info (top)
        for i in range(self.box_size):
            self.my_pokemon_vs_him_image_labels[i].config(image=self.my_pokemon_vs_him_image_labels[i].image)
            self.my_pokemon_vs_him_image_labels[i].grid(row=1, column=i)
            
            self.my_pokemon_move_vs_him_labels[i].grid(row=2, column=i)
            self.my_pokemon_info_top[i].grid(row=0, column=i)
            
        # Display my Pokemon images and move info (bottom)
        for i in range(self.box_size):
            self.him_vs_my_pokemon_image_labels[i].config(image=self.him_vs_my_pokemon_image_labels[i].image)
            self.him_vs_my_pokemon_image_labels[i].grid(row=6, column=i)

            self.enemy_pokemon_move_vs_me_labels[i].grid(row=7, column=i)
            self.my_pokemon_info_bot[i].grid(row=5, column=i)

    def create_navigation_buttons(self):
        prev_button = tk.Button(self.root, text="Previous", command=self.show_previous_pokemon)
        prev_button.grid(row=8, column=0)
        next_button = tk.Button(self.root, text="Next", command=self.show_next_pokemon)
        next_button.grid(row=8, column=self.box_size - 1)

    def show_next_pokemon(self):
        if self.current_index < len(self.enemy_team_info) - 1:
            self.current_index += 1
            self.load_pokemon_images()
            self.display_current_pokemon_info()

    def show_previous_pokemon(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_pokemon_images()
            self.display_current_pokemon_info()

def pokemon_battle_gui(enemy_team_info, my_pokemons, his_variable_moves, my_variable_moves):
    root = tk.Tk()
    app = PokemonBattleGUI(root, enemy_team_info, my_pokemons, his_variable_moves, my_variable_moves)
    root.mainloop()
