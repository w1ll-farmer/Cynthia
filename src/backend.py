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

def get_pokemon_info():
    with open(os.path.join("data","raw","chaos","gen9vgc2025regg-1760.json"), "r") as file:
        data = json.load(file)
    
    pokemon_name = "Urshifu-Rapid-Strike"
    pokemon_data = data['data'].get(pokemon_name)

    if pokemon_data:
        print(f"data for {pokemon_name}:\n")
        for key, val in pokemon_data.items():
            print(f"{key}: {val}")
    else:
        print("No data")

def sort_by_usage(format="gen9vgc2025regg-1760"):
    # Load the Chaos JSON file
    with open(os.path.join("data","raw","chaos",f"{format}.json"), "r") as file:
        data = json.load(file)

    # Get the full data dictionary
    pokemon_stats = data["data"]

    # Sort by 'usage' in descending order
    sorted_pokemon = sorted(
        pokemon_stats.items(),
        key=lambda item: item[1].get("usage", 0),
        reverse=True
    )

    # Extract the top 100
    top_100 = sorted_pokemon[:100]

    # Print them out nicely
    for (name, stats) in top_100:
        pass
sort_by_usage()