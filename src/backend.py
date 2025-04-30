import pandas as pd
import numpy as np
import json
import os

global COLS
COLS = ["Raw count","Abilities","Items","Spreads","Moves","Teammates","Checks and Counters", "usage"]
# Raw count (int): Number of teams that used this mon
# Viability ceiling [count, max_gxe, gxe_1%, gxe_20%]: Recommended use gxe_1%
# Abilities ({ability: usage %})
# Items ({item: usage %})
# Spreads {"nature:hp/atk/def/spatk/spdef/spd":count}
# Moves {move:count}
# Teammates {teammate:count}
# Checks and Counters {check/counter:[count appeared on opposite teams, ko/force switch out %, std]}

def get_pokemon_info(pokemon_name=None, format="gen9vgc2025regg-1760"):
    if pokemon_name is None:
        print("Must enter a pokemon name")
        return None
    
    with open(os.path.join("data","raw","chaos",f"{format}.json"), "r") as file:
        data = json.load(file)
    
    pokemon_data = data['data'].get(pokemon_name)

    if pokemon_data:
        return pokemon_data
    print("Either there's no data about this pokemon or you have entered their name in the wrong format")
    return None

info = get_pokemon_info("Infernape")