import openpyxl

from pokemon import Pokemon
from move import Move
from read_files import *


def get_trainer_pokemon(lines, line_number):
    trainer_pokemon = []

    # Trainer info exists until whiteline
    while lines[line_number - 1] != '\n':
        pokemon_line = lines[line_number - 1].strip()

        # Get pokemon name
        pokemon_name = "" 
        for char in pokemon_line:
            if char == '(' or char == ' ':
                break
            pokemon_name += char
        
        # Make an exception for nidoran(m)/nidoran(f)
        if pokemon_name == "Nidoran":
            pokemon_name = pokemon_line.split(' ')[0]

        pokemon = pokemons[pokemon_name]

        pokemon_moves = pokemon_line.split(': ')[1].split(', ')
        pokemon_moves[3] = pokemon_moves[3].split(' [')[0].split(' +')[0]  # Last move has extra fluff info to the right
        pokemon_moves = [x for x in pokemon_moves if x != '-----']
        pokemon_moves = [moves[x.lower()] for x in pokemon_moves]

        trainer_pokemon.append((pokemon, pokemon_moves))
        line_number += 1

    return trainer_pokemon


moves = read_moves_sheet("gen3moves.xlsx")
pokemons = read_pokemon_sheet("pokemon.xlsx", moves)
box = read_box()

with open('EK Mastersheet.txt', 'r') as f:
    lines = f.readlines()
    while True:
        line_number = int(input("Enter line number at which trainer starts: "))

        print(f"Helping you fight '{lines[line_number - 1].strip()}'!")
        line_number += 1
        trainer_pokemon = get_trainer_pokemon(lines, line_number)
        
        pass
