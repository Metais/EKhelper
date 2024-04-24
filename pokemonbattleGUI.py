import tkinter as tk
from PIL import Image, ImageTk
from math import floor
from read_files import read_trainer_pokemon_from_json, get_trainer_index
from damage_calc import get_move_details

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

def remove_tooltip(widget):
    widget.unbind("<Enter>")
    widget.unbind("<Leave>")


class PokemonBattleGUI:
    def __init__(self, root, enemy_trainer, game_info, my_pokemons):
        self.root = root
        self.root.title(enemy_trainer)
        self.root.iconbitmap("images/pokeball.ico")
        
        self.enemy_trainer = enemy_trainer
        self.game_info = game_info
        self.my_pokemons = my_pokemons

        # Establish self.enemy_team_info, self.his_moves and self.his_variable_moves
        self.get_battle_info()

        self.current_index = 0
        self.box_size = len(my_pokemons)

        # Enemy pokemon image
        self.enemy_pokemon_label = tk.Label(root)

        # Enemy pokemon info label
        self.enemy_pokemon_info_label = tk.Label(root)

        # Enemy pokemon held item label
        self.enemy_pokemon_held_item_text_label = tk.Label(root)
        self.enemy_pokemon_held_item_image_label = tk.Label(root)

        # Enemey pokemon ability label
        self.enemy_pokemon_ability_label = tk.Label(root)

        # Enemy pokemon move labels
        self.enemy_pokemon_move_labels = [tk.Label(root) for _ in range(4)]

        # Up to 4 variable move labels
        self.enemy_pokemon_variable_move_labels = tk.Label(root, wraplength=500)

        # My pokemon Image labels
        self.my_pokemon_vs_him_image_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.my_pokemon_vs_him_first_second_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.him_vs_my_pokemon_image_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.him_vs_my_pokemon_first_second_labels = [tk.Label(root) for _ in range(self.box_size)]

        # My pokemon Text labels
        self.my_pokemon_move_vs_him_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.my_pokemon_move_vs_him_texts = [[] for _ in range(self.box_size)]

        self.enemy_pokemon_move_vs_me_labels = [tk.Label(root) for _ in range(self.box_size)]
        self.enemy_pokemon_move_vs_me_texts = [[] for _ in range(self.box_size)]
        
        self.my_pokemon_info_top = [tk.Label(root) for _ in range(self.box_size)]
        self.my_pokemon_info_bot = [tk.Label(root) for _ in range(self.box_size)]

        # Bind click events for my pokemon move vs him labels
        for i in range(self.box_size):
            self.my_pokemon_move_vs_him_labels[i].bind("<Button-1>", lambda event, 
                                                       index=i: self.swap_text(self.my_pokemon_move_vs_him_labels[index], 
                                                                               self.my_pokemon_move_vs_him_texts[index]))

        # Bind click events for enemy pokemon move vs me labels
        for i in range(self.box_size):
            self.enemy_pokemon_move_vs_me_labels[i].bind("<Button-1>", lambda event, 
                                                         index=i: self.swap_text(self.enemy_pokemon_move_vs_me_labels[index], 
                                                                                 self.enemy_pokemon_move_vs_me_texts[index]))

        self.top_row_page = 0
        self.bot_row_page = 0
        
        self.create_navigation_buttons()
        self.load_content()
        self.display_current_pokemon_info()

    def swap_text(self, label, texts):
        # Get the current text of the label
        current_text = label.cget("text")
        # Find the index of the current text in the list of texts
        current_index = texts.index(current_text)
        # Determine the next index (wrapping around if necessary)
        next_index = (current_index + 1) % len(texts)
        # Update the label's text to the next text in the list
        label.config(text=texts[next_index])

    def get_battle_info(self):
        trainer_pokemon = read_trainer_pokemon_from_json(self.enemy_trainer, self.game_info)

        trainer_index = get_trainer_index(self.enemy_trainer)
        if trainer_index > get_trainer_index("Leaders Tate&Liza"):
            self.badge_boosts = { "Stone": True, "Dynamo": True, "Balance": True, "Mind": True}
        elif trainer_index > get_trainer_index("Leader Norman"):
            self.badge_boosts = { "Stone": True, "Dynamo": True, "Balance": True, "Mind": False}
        elif trainer_index > get_trainer_index("Leader Wattson"):
            self.badge_boosts = { "Stone": True, "Dynamo": True, "Balance": False, "Mind": False}
        elif trainer_index > get_trainer_index("Leader Roxanne"):
            self.badge_boosts = { "Stone": True, "Dynamo": False, "Balance": False, "Mind": False}
        else:
            self.badge_boosts = { "Stone": False, "Dynamo": False, "Balance": False, "Mind": False}

        # Index in following lists corresponds to trainer's pokemon in order
        his_moves = []
        his_variable_moves = []
        enemy_team_info = []

        # For each enemy pokemon...
        for enemy_pokemon in trainer_pokemon:
            # Each enemy pokemon has a dictionary containing my pokemon's names as keys
            # except the key/value pair 'variable', which stores the pokemon's variables moves
            enemy_pokemon_analysis = {}

            his_moves.append([move for move in enemy_pokemon.cur_moves])
            his_variable_moves.append([move for move in enemy_pokemon.cur_moves if move.power != "N/A" and not isinstance(move.power, int)])

            # For each of my pokemon...
            for my_pokemon in self.my_pokemons:
                # Move infos
                move_info_vs_me = get_move_details(enemy_pokemon, my_pokemon, self.badge_boosts, attacking=False)
                move_info_vs_him = get_move_details(my_pokemon, enemy_pokemon, self.badge_boosts, attacking=True)

                # Who goes first (0 = me, 1 = him, 2 = tie)
                my_spe = my_pokemon.get_real_spe_stat(my_pokemon.spe_iv)
                his_spe = enemy_pokemon.get_real_spe_stat(enemy_pokemon.spe_iv)
                if self.badge_boosts["Dynamo"]:
                    my_spe = floor(my_spe*1.1)

                if my_spe > his_spe:
                    goes_first = 0
                elif my_spe < his_spe:
                    goes_first = 1
                else:
                    goes_first = 2
                
                # Store above 3 values per box pokemon for each enemy pokemon
                enemy_pokemon_analysis[my_pokemon.name] = (move_info_vs_me, move_info_vs_him, goes_first)
                
            enemy_team_info.append((enemy_pokemon, enemy_pokemon_analysis))

        self.enemy_team_info = enemy_team_info
        self.his_moves = his_moves
        self.his_variable_moves = his_variable_moves

    def load_content(self):
        cur_enemy_pokemon = self.enemy_team_info[self.current_index][0]

        # Load enemy Pokemon image
        enemy_pokemon_image = cur_enemy_pokemon.get_gif()
        enemy_pokemon_image = enemy_pokemon_image.resize((200, 200))
        self.enemy_pokemon_label.image = ImageTk.PhotoImage(enemy_pokemon_image)
        self.enemy_pokemon_label.config(image=self.enemy_pokemon_label.image)
        create_tooltip(self.enemy_pokemon_label, cur_enemy_pokemon.print_current_stats(), 200, 200)

        # Load enemy pokemon info
        self.enemy_pokemon_info_label.config(text=cur_enemy_pokemon.print_current_stats(), wraplength=200)
        # Load enemy pokemon held item
        if cur_enemy_pokemon.held_item is not None:
            held_item_image = Image.open(cur_enemy_pokemon.held_item.image_path)
            self.enemy_pokemon_held_item_image_label.image = ImageTk.PhotoImage(held_item_image.resize((40, 40)))
            self.enemy_pokemon_held_item_image_label.config(image=self.enemy_pokemon_held_item_image_label.image)
            self.enemy_pokemon_held_item_text_label.config(text=str(cur_enemy_pokemon.held_item), wraplength=100)
        else:
            self.enemy_pokemon_held_item_image_label.config(image="")
            self.enemy_pokemon_held_item_text_label.config(text="")

        # Load enemy ability info
        self.enemy_pokemon_ability_label.config(text=str(cur_enemy_pokemon.ability), wraplength=200)

        # Load enemy pokemon moves and tooltips
        for i in range(4):
            self.enemy_pokemon_move_labels[i].config(text="")
            if len(self.his_moves[self.current_index]) > i:
                self.enemy_pokemon_move_labels[i].config(text=self.his_moves[self.current_index][i].name)
                create_tooltip(self.enemy_pokemon_move_labels[i], self.his_moves[self.current_index][i].detailed_string())

        # Load enemy pokemon variable moves (on the right)
        variable_move_text = ""
        for variable_move in self.his_variable_moves[self.current_index]:
            variable_move_text += variable_move.detailed_string() + "\n\n"
        self.enemy_pokemon_variable_move_labels.config(text=variable_move_text)

        # Load my Pokemon images and move info (me vs him)
        # Start by creating a list [ ("my_mon1": [("move1", 49), ("move2", 38)]), ("my_mon2": [("move1", 54), ("move2", 25)]) ]
        my_mons_move_vs_him = [(my_mon, move_info[1]) for my_mon, move_info in self.enemy_team_info[self.current_index][1].items()]
        # Then order it desc by strongest move [ ("my_mon2": [("move1", 54), ("move2", 25)]), ("my_mon1": [("move1", 49), ("move2", 38)]) ]
        in_order = sorted(my_mons_move_vs_him, key=lambda x: x[1][0][1], reverse=True)

        # Decide on how many pokemon to list in the row
        if self.box_size <= 13:
            start = 0
            amount = self.box_size
        else:
            start = self.top_row_page * 11
            amount = min(11, self.box_size - start)

        for i, (pokemon_name, move_info) in enumerate(in_order[start:start+amount]):
            # Pokemon level and name
            pokemon_i = [x for x in self.my_pokemons if x.name == pokemon_name][0]
            self.my_pokemon_info_top[i].config(text=f"Lv. {pokemon_i.lvl} {pokemon_i.name}")

            # Pokemon image
            pokemon_image = pokemon_i.get_gif()
            pokemon_image = pokemon_image.resize((100, 100))
            self.my_pokemon_vs_him_image_labels[i].image = ImageTk.PhotoImage(pokemon_image)
            self.my_pokemon_vs_him_image_labels[i].config(image=self.my_pokemon_vs_him_image_labels[i].image)
            create_tooltip(self.my_pokemon_vs_him_image_labels[i], pokemon_i.print_current_stats(with_ability=True), 100, 100)

            # Move info (reset texts from previous load_content call)
            self.my_pokemon_move_vs_him_texts[i].clear()
            for move, move_power in move_info:
                if move.name in ["Sonicboom", "Night Shade", "Dragon Rage", "Seismic Toss", "Psywave"]:
                    move_text = f"{move}\nPower: {int(move_power)}"
                elif move.name == "Magnitude":
                    move_text = f"{move}\nPower: {int(0.85*move_power/15)}-{int(move_power)}"
                else:
                    move_text = f"{move}\nPower: {int(0.85*move_power)}-{int(move_power)}"
                self.my_pokemon_move_vs_him_texts[i].append(move_text)

            self.my_pokemon_move_vs_him_labels[i].config(text=self.my_pokemon_move_vs_him_texts[i][0])

            # First or second info
            speed_info = self.enemy_team_info[self.current_index][1][pokemon_name][2]
            if speed_info == 0:
                first_second_image = Image.open("images/1st.png")
            elif speed_info == 1:
                first_second_image = Image.open("images/2nd.png")
            else:
                first_second_image = Image.open("images/tie.png")
            first_second_image = first_second_image.resize((20, 20))
            self.my_pokemon_vs_him_first_second_labels[i].image = ImageTk.PhotoImage(first_second_image)
            self.my_pokemon_vs_him_first_second_labels[i].config(image=self.my_pokemon_vs_him_first_second_labels[i].image)

        # Empty the squares if on the last page and row not fully filled
        if start + amount == self.box_size > 13 and (start + amount) % 11 != 0:
            for i in range(amount, 11):
                self.my_pokemon_info_top[i].config(text="")
                self.my_pokemon_vs_him_image_labels[i].image = None
                self.my_pokemon_move_vs_him_labels[i].config(text="")
                self.my_pokemon_vs_him_first_second_labels[i].image = None
                remove_tooltip(self.my_pokemon_vs_him_image_labels[i])

        # Load my Pokemon images and move info (him vs me)
        # Start by creating a list [ ("his_mon1": [("move1", 49), ("move2", 38)]), ("his_mon2": [("move1", 54), ("move2", 25)]) ]
        his_mons_move_vs_me = [(my_mon, move_info[0]) for my_mon, move_info in self.enemy_team_info[self.current_index][1].items()]
        # Then order it asc by strongest move [ ("his_mon1": [("move1", 49), ("move2", 38)]), ("his_mon2": [("move1", 54), ("move2", 25)]) ]
        in_order = sorted(his_mons_move_vs_me, key=lambda x: x[1][0][1])

        # Decide on how many pokemon to list in the row
        if self.box_size <= 13:
            start = 0
            amount = self.box_size
        else:
            start = self.bot_row_page * 11
            amount = min(11, self.box_size - start)

        for i, (pokemon_name, move_info) in enumerate(in_order[start:start+amount]):
            # Pokemon level and name
            pokemon_i = [x for x in self.my_pokemons if x.name == pokemon_name][0]
            self.my_pokemon_info_bot[i].config(text=f"Lv. {pokemon_i.lvl} {pokemon_i.name}")

            # Pokemon image
            pokemon_image = pokemon_i.get_gif()
            pokemon_image = pokemon_image.resize((100, 100))
            self.him_vs_my_pokemon_image_labels[i].image = ImageTk.PhotoImage(pokemon_image)
            self.him_vs_my_pokemon_image_labels[i].config(image=self.him_vs_my_pokemon_image_labels[i].image)
            create_tooltip(self.him_vs_my_pokemon_image_labels[i], pokemon_i.print_current_stats(with_ability=True), 100, 100)

            # Move info (reset texts from previous load_content call)
            self.enemy_pokemon_move_vs_me_texts[i].clear()
            for move, move_power in move_info:
                if move.name in ["Sonicboom", "Night Shade", "Dragon Rage", "Seismic Toss", "Psywave"]:
                    move_text = f"{move}\nPower: {int(move_power)}"
                elif move.name == "Magnitude":
                    move_text = f"{move}\nPower: {int(0.85*move_power/15)}-{int(move_power)}"
                else:
                    move_text = f"{move}\nPower: {int(0.85*move_power)}-{int(move_power)}"
                self.enemy_pokemon_move_vs_me_texts[i].append(move_text)

            self.enemy_pokemon_move_vs_me_labels[i].config(text=self.enemy_pokemon_move_vs_me_texts[i][0])

            # First or second info
            speed_info = self.enemy_team_info[self.current_index][1][pokemon_name][2]
            if speed_info == 0:
                first_second_image = Image.open("images/1st.png")
            elif speed_info == 1:
                first_second_image = Image.open("images/2nd.png")
            else:
                first_second_image = Image.open("images/tie.png")
            first_second_image = first_second_image.resize((20, 20))
            self.him_vs_my_pokemon_first_second_labels[i].image = ImageTk.PhotoImage(first_second_image)
            self.him_vs_my_pokemon_first_second_labels[i].config(image=self.him_vs_my_pokemon_first_second_labels[i].image)

        # Empty the squares if on the last page and row not fully filled
        if start + amount == self.box_size > 13 and (start + amount) % 11 != 0:
            for i in range(amount, 11):
                self.my_pokemon_info_bot[i].config(text="")
                self.him_vs_my_pokemon_image_labels[i].image = None
                self.enemy_pokemon_move_vs_me_labels[i].config(text="")
                self.him_vs_my_pokemon_first_second_labels[i].image = None
                remove_tooltip(self.him_vs_my_pokemon_image_labels[i])
           
    def display_current_pokemon_info(self):
        # Display enemy pokemon image
        self.enemy_pokemon_label.grid(row=4, column=5, columnspan=2, rowspan=2)

        # Display enemy pokemon info
        self.enemy_pokemon_info_label.grid(row=4, column=2, columnspan=2, rowspan=2, sticky="ew")

        # Display enemy pokemon moves labels
        self.enemy_pokemon_move_labels[0].grid(row=4, column=4)
        self.enemy_pokemon_move_labels[1].grid(row=5, column=4)
        self.enemy_pokemon_move_labels[2].grid(row=4, column=7)
        self.enemy_pokemon_move_labels[3].grid(row=5, column=7)

        # Display enemy pokemon held item
        self.enemy_pokemon_held_item_image_label.grid(row=4, column=8, sticky='s')
        self.enemy_pokemon_held_item_text_label.grid(row=5, column=8, stick='n')

        # Display enemy pokemon ability
        self.enemy_pokemon_ability_label.grid(row=4, column=9, rowspan=2, columnspan=2)

        # Display enemy pokemon variable moves label
        self.enemy_pokemon_variable_move_labels.grid(row=0, rowspan=10, column=13)

        # If <= 13 usable pokemons, static display. If > 13 pokemon, use buttons to click right/left so the window stays fixed size
        if self.box_size <= 13:
            start_column = 6 - floor(self.box_size / 2)
            box_range = self.box_size
        else:
            start_column = 1
            box_range = 11

        # Display my Pokemon images and move info (top)
        for i in range(box_range):
            self.my_pokemon_info_top[i].grid(row=0, column=start_column + i)
            self.my_pokemon_vs_him_image_labels[i].grid(row=1, column=start_column + i)
            self.my_pokemon_move_vs_him_labels[i].grid(row=2, column=start_column + i)
            self.my_pokemon_vs_him_first_second_labels[i].grid(row=3, column=start_column + i)
            
        # Display my Pokemon images and move info (bottom)
        for i in range(box_range):
            self.my_pokemon_info_bot[i].grid(row=6, column=start_column + i)
            self.him_vs_my_pokemon_image_labels[i].grid(row=7, column=start_column + i)
            self.enemy_pokemon_move_vs_me_labels[i].grid(row=8, column=start_column + i)
            self.him_vs_my_pokemon_first_second_labels[i].grid(row=9, column=start_column + i)

    def create_navigation_buttons(self):
        prev_button = tk.Button(self.root, text="Previous", command=self.show_previous_pokemon)
        prev_button.grid(row=4, rowspan=2, column=0)

        next_button = tk.Button(self.root, text="Next", command=self.show_next_pokemon)
        next_button.grid(row=4, rowspan=2, column=12)

        trainer_selection_button = tk.Button(self.root, text="Back to trainer select", command=self.back_to_trainer_select)
        trainer_selection_button.grid(row=10, column=5, columnspan=2)

        if self.box_size > 13:
            prev_top_row_button = tk.Button(self.root, text="Previous", command=self.show_previous_top_row)
            prev_top_row_button.grid(row=1, column=0)

            next_top_row_button = tk.Button(self.root, text="Next", command=self.show_next_top_row)
            next_top_row_button.grid(row=1, column=12)

            prev_bot_row_button = tk.Button(self.root, text="Previous", command=self.show_previous_bot_row)
            prev_bot_row_button.grid(row=7, column=0)

            next_bot_row_button = tk.Button(self.root, text="Next", command=self.show_next_bot_row)
            next_bot_row_button.grid(row=7, column=12)


    def show_previous_top_row(self):
        if self.top_row_page > 0:
            self.top_row_page -= 1
            self.load_content()

    def show_next_top_row(self):
        # 11 pokemon per page
        if self.top_row_page < floor((self.box_size - 1) / 11):
            self.top_row_page += 1
            self.load_content()

    def show_previous_bot_row(self):
        if self.bot_row_page > 0:
            self.bot_row_page -= 1
            self.load_content()

    def show_next_bot_row(self):
        # 11 pokemon per page
        if self.bot_row_page < floor((self.box_size - 1) / 11):
            self.bot_row_page += 1
            self.load_content()

    def show_next_pokemon(self):
        if self.current_index < len(self.enemy_team_info) - 1:
            self.current_index += 1
            
            # Reset top/bot row pages
            self.top_row_page = 0
            self.bot_row_page = 0

            self.load_content()

    def show_previous_pokemon(self):
        if self.current_index > 0:
            self.current_index -= 1

            # Reset top/bot row pages
            self.top_row_page = 0
            self.bot_row_page = 0

            self.load_content()

    def back_to_trainer_select(self):
        # Lazy import
        from trainerselectionGUI import TrainerSelectionGUI
        # Record last-watched trainer in save file
        with open(f'data/save.txt', 'w') as f:
            f.write(self.enemy_trainer)
        # Destroy the current window and switch to the battle window
        self.root.destroy()
        root = tk.Tk()
        app = TrainerSelectionGUI(root, self.game_info, self.my_pokemons, selected_trainer=self.enemy_trainer)
        root.mainloop()
