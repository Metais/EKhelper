import tkinter as tk
from PIL import Image, ImageTk
from math import floor

class ToolTip:
    def __init__(self, widget, text, offsetx, offsety):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.offsetx = offsetx
        self.offsety = offsety
        
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + self.offsetx
        y += self.widget.winfo_rooty() + self.offsety

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry("+%d+%d" % (x, y))
        
        label = tk.Label(self.tooltip_window, text=self.text, bg="lightyellow", relief="solid", borderwidth=1, wraplength=400)
        label.pack(padx=5, pady=5)
        
    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

def create_tooltip(widget, text, offsetx=25, offsety=25):
    tooltip = ToolTip(widget, text, offsetx, offsety)
    widget.bind("<Enter>", tooltip.show_tooltip)
    widget.bind("<Leave>", tooltip.hide_tooltip)


class PokemonBattleGUI:
    def __init__(self, root, enemy_team_info, my_pokemons, his_moves, his_variable_moves, my_variable_moves):
        self.root = root
        self.enemy_team_info = enemy_team_info
        self.my_pokemons = my_pokemons
        self.his_moves = his_moves
        self.his_variable_moves = his_variable_moves
        self.my_variable_moves = my_variable_moves
        self.current_index = 0
        self.box_size = len(enemy_team_info[0][1].keys())

        # Enemy pokemon image
        self.enemy_pokemon_label = tk.Label(root)

        # Enemy pokemon info label
        self.enemy_pokemon_info_label = tk.Label(root)

        # Enemy pokemon held item label
        self.enemy_pokemon_held_item_text_label = tk.Label(root)
        self.enemy_pokemon_held_item_image_label = tk.Label(root)

        # Enemy pokemon move labels
        self.enemy_pokemon_move_labels = [tk.Label(root) for _ in range(4)]

        # Up to 4 variable move labels
        self.enemy_pokemon_variable_move_labels = [tk.Label(root, wraplength=500) for _ in range(4)]

        # My pokemon Image labels
        self.my_pokemon_vs_him_image_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.my_pokemon_vs_him_first_second_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.him_vs_my_pokemon_image_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.him_vs_my_pokemon_first_second_labels = [tk.Label(root) for _ in range(self.box_size)]

        # My pokemon Text labels
        self.my_pokemon_move_vs_him_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.enemy_pokemon_move_vs_me_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.my_pokemon_info_top = [tk.Label(root) for _ in range(self.box_size)]
        self.my_pokemon_info_bot = [tk.Label(root) for _ in range(self.box_size)]

        self.load_content()
        self.display_current_pokemon_info()
        self.create_navigation_buttons()

    def load_content(self):
        cur_enemy_pokemon = self.enemy_team_info[self.current_index][0]

        # Load enemy Pokemon image
        enemy_pokemon_image = Image.open(f"animations/{cur_enemy_pokemon.name}.gif")
        enemy_pokemon_image = enemy_pokemon_image.resize((200, 200))
        self.enemy_pokemon_label.image = ImageTk.PhotoImage(enemy_pokemon_image)
        self.enemy_pokemon_label.config(image=self.enemy_pokemon_label.image)
        create_tooltip(self.enemy_pokemon_label, cur_enemy_pokemon.print_estimated_stats(), 200, 200)

        # Load enemy pokemon info
        self.enemy_pokemon_info_label.config(text=cur_enemy_pokemon.print_estimated_stats())
        # Load enemy pokemon held item
        if cur_enemy_pokemon.held_item is not None:
            held_item_image = Image.open(cur_enemy_pokemon.held_item.image_path)
            self.enemy_pokemon_held_item_image_label.image = ImageTk.PhotoImage(held_item_image.resize((40, 40)))
            self.enemy_pokemon_held_item_image_label.config(image=self.enemy_pokemon_held_item_image_label.image)
            self.enemy_pokemon_held_item_text_label.config(text=str(cur_enemy_pokemon.held_item), wraplength=100)
        else:
            self.enemy_pokemon_held_item_image_label.config(image="")
            self.enemy_pokemon_held_item_text_label.config(text="")

        # Load enemy pokemon moves and tooltips
        for i in range(4):
            self.enemy_pokemon_move_labels[i].config(text="")
            if len(self.his_moves[self.current_index]) > i:
                self.enemy_pokemon_move_labels[i].config(text=self.his_moves[self.current_index][i].name)
                create_tooltip(self.enemy_pokemon_move_labels[i], self.his_moves[self.current_index][i].detailed_string())

        # Load enemy pokemon variable moves (on the right)
        for i in range(4):
            self.enemy_pokemon_variable_move_labels[i].config(text="")
            if len(self.his_variable_moves[self.current_index]) > i:
                self.enemy_pokemon_variable_move_labels[i].config(text=self.his_variable_moves[self.current_index][i].detailed_string())

        # Load my Pokemon images and move info (me vs him)
        in_order = sorted(self.enemy_team_info[self.current_index][1].items(), key=lambda x: x[1][3], reverse=True)
        for i, (pokemon_name, move_info) in enumerate(in_order):
            # Pokemon level and name
            pokemon_i = [x for x in self.my_pokemons if x.name == pokemon_name][0]
            self.my_pokemon_info_top[i].config(text=f"Lv. {pokemon_i.lvl} {pokemon_i.name}")

            # Pokemon image
            pokemon_image = Image.open(f"animations/{pokemon_name}.gif")
            pokemon_image = pokemon_image.resize((100, 100))
            self.my_pokemon_vs_him_image_labels[i].image = ImageTk.PhotoImage(pokemon_image)
            self.my_pokemon_vs_him_image_labels[i].config(image=self.my_pokemon_vs_him_image_labels[i].image)
            create_tooltip(self.my_pokemon_vs_him_image_labels[i], pokemon_i.print_current_stats(), 100, 100)

            # Move info
            move_name, move_power = move_info[2], move_info[3]
            move_text = f"{move_name}\nPower: {move_power}"
            self.my_pokemon_move_vs_him_labels[i].config(text=move_text)

            # First or second info
            first_second_image = Image.open("images/1st.png") if move_info[4] == 0 else Image.open("images/2nd.png")
            first_second_image = first_second_image.resize((20, 20))
            self.my_pokemon_vs_him_first_second_labels[i].image = ImageTk.PhotoImage(first_second_image)
            self.my_pokemon_vs_him_first_second_labels[i].config(image=self.my_pokemon_vs_him_first_second_labels[i].image)

        
        # Load my Pokemon images and move info (him vs me)
        in_order = sorted(self.enemy_team_info[self.current_index][1].items(), key=lambda x: x[1][1])
        for i, (pokemon_name, move_info) in enumerate(in_order):
            # Pokemon level and name
            pokemon_i = [x for x in self.my_pokemons if x.name == pokemon_name][0]
            self.my_pokemon_info_bot[i].config(text=f"Lv. {pokemon_i.lvl} {pokemon_i.name}")

            # Pokemon image
            pokemon_image = Image.open(f"animations/{pokemon_name}.gif")
            pokemon_image = pokemon_image.resize((100, 100))
            self.him_vs_my_pokemon_image_labels[i].image = ImageTk.PhotoImage(pokemon_image)
            self.him_vs_my_pokemon_image_labels[i].config(image=self.him_vs_my_pokemon_image_labels[i].image)
            create_tooltip(self.him_vs_my_pokemon_image_labels[i], pokemon_i.print_current_stats(), 100, 100)

            # Move info
            move_name, move_power = move_info[0], move_info[1]
            move_text = f"{move_name}\nPower: {move_power}"
            self.enemy_pokemon_move_vs_me_labels[i].config(text=move_text)

            # First or second info
            first_second_image = Image.open("images/1st.png") if move_info[4] == 0 else Image.open("images/2nd.png")
            first_second_image = first_second_image.resize((20, 20))
            self.him_vs_my_pokemon_first_second_labels[i].image = ImageTk.PhotoImage(first_second_image)
            self.him_vs_my_pokemon_first_second_labels[i].config(image=self.him_vs_my_pokemon_first_second_labels[i].image)
           
    def display_current_pokemon_info(self):
        label_column = floor(self.box_size / 2) - 1
        label_column = label_column if label_column >= 3 else 3

        # Display enemy pokemon image
        self.enemy_pokemon_label.grid(row=4, column=label_column, columnspan=2, rowspan=2)

        # Display enemy pokemon info
        self.enemy_pokemon_info_label.grid(row=4, column=label_column-3, columnspan=2, rowspan=2, sticky="ew")

        # Display enemy pokemon moves labels
        left_move_column = label_column - 1
        right_move_column = label_column + 2
        self.enemy_pokemon_move_labels[0].grid(row=4, column=left_move_column)
        self.enemy_pokemon_move_labels[1].grid(row=5, column=left_move_column)
        self.enemy_pokemon_move_labels[2].grid(row=4, column=right_move_column)
        self.enemy_pokemon_move_labels[3].grid(row=5, column=right_move_column)

        # Display enemy pokemon held item
        self.enemy_pokemon_held_item_image_label.grid(row=4, column=label_column + 3, sticky='s')
        self.enemy_pokemon_held_item_text_label.grid(row=5, column=label_column + 3, stick='n')

        # Display enemy pokemon variable moves label
        self.enemy_pokemon_variable_move_labels[0].grid(row=0, rowspan=2, column=self.box_size, columnspan=1)
        self.enemy_pokemon_variable_move_labels[1].grid(row=2, rowspan=2, column=self.box_size, columnspan=1)
        self.enemy_pokemon_variable_move_labels[2].grid(row=4, rowspan=2, column=self.box_size, columnspan=1)
        self.enemy_pokemon_variable_move_labels[3].grid(row=6, rowspan=2, column=self.box_size, columnspan=1)

        # Display my Pokemon images and move info (top)
        for i in range(self.box_size):
            self.my_pokemon_info_top[i].grid(row=0, column=i)
            self.my_pokemon_vs_him_image_labels[i].grid(row=1, column=i)
            self.my_pokemon_move_vs_him_labels[i].grid(row=2, column=i)
            self.my_pokemon_vs_him_first_second_labels[i].grid(row=3, column=i)
            
        # Display my Pokemon images and move info (bottom)
        for i in range(self.box_size):
            self.my_pokemon_info_bot[i].grid(row=6, column=i)
            self.him_vs_my_pokemon_image_labels[i].grid(row=7, column=i)
            self.enemy_pokemon_move_vs_me_labels[i].grid(row=8, column=i)
            self.him_vs_my_pokemon_first_second_labels[i].grid(row=9, column=i)

    def create_navigation_buttons(self):
        prev_button = tk.Button(self.root, text="Previous", command=self.show_previous_pokemon)
        prev_button.grid(row=10, column=0)
        next_button = tk.Button(self.root, text="Next", command=self.show_next_pokemon)
        next_button.grid(row=10, column=self.box_size - 1)

    def show_next_pokemon(self):
        if self.current_index < len(self.enemy_team_info) - 1:
            self.current_index += 1
            self.load_content()

    def show_previous_pokemon(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_content()

def pokemon_battle_gui(enemy_team_info, my_pokemons, his_moves, his_variable_moves, my_variable_moves):
    root = tk.Tk()
    app = PokemonBattleGUI(root, enemy_team_info, my_pokemons, his_moves, his_variable_moves, my_variable_moves)
    root.mainloop()
