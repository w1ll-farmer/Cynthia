import pandas as pd
import numpy as np
import json
import os
import requests

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

def get_pokemon_smogon_info(pokemon_name=None, format="gen9vgc2025regg-1760"):
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


def get_pokemon_base_info(pokemon_name):
    print(pokemon_name)
    if " " in pokemon_name:
        space_idx = pokemon_name.index(" ")
        pokemon_name = pokemon_name[:space_idx]+"-"+pokemon_name[space_idx+1:]
    if "Ogerpon" in pokemon_name and pokemon_name != "Ogerpon":
        pokemon_name += "-mask"
    if pokemon_name in ["Landorus","Tornadus","Thundurus","Enamorus"]:
        pokemon_name+= "-incarnate"
    if pokemon_name.endswith("-M"): pokemon_name += "ale"
    if pokemon_name.endswith("-F"): pokemon_name += "emale"
    if pokemon_name == "Urshifu": pokemon_name = "urshifu-single-strike"
    if pokemon_name == "Tatsugiri": pokemon_name = "tatsugiri-curly"
    if pokemon_name == "Maushold": pokemon_name = "maushold-family-of-three"
    if pokemon_name == "Basculegion": pokemon_name = "basculegion-male"
    if pokemon_name == "Meowstic": pokemon_name = "meowstic-male"
    if pokemon_name == "Indeedee": pokemon_name = "indeedee-male"
    if "Necrozma" in pokemon_name and pokemon_name.endswith("Wings"): pokemon_name = pokemon_name[:-6]
    if "Necrozma" in pokemon_name and pokemon_name.endswith("Mane"): pokemon_name = pokemon_name[:-5]
    if pokemon_name == "Giratina": pokemon_name = "giratina-altered"
    if pokemon_name == "Mimikyu": pokemon_name = "mimikyu-disguised"
    if pokemon_name == "Dudunsparce": pokemon_name = "dudunsparce-two-segment"
    if pokemon_name.startswith("Tauros-Paldea"): pokemon_name += "-Breed"
    if pokemon_name == "Lycanroc": pokemon_name = "lycanroc-midday"
    if pokemon_name == "Toxtricity": pokemon_name = "toxtricity-low-key"
    try:
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")
        data = response.json()
    except:
        print(pokemon_name)

    # Base stats
    stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
    # Types
    types = [t["type"]["name"] for t in data["types"]]
    weight = data["weight"]
    return stats, types, weight

def get_all_mons(format="gen9vgc2025regi-1760"):
    with open(os.path.join("data","raw","chaos",f"{format}.json"),"r") as file:
        data = json.load(file)

    # Get the full data dictionary
    pokemon_stats = data["data"]

    # Sort by 'usage' in descending order
    sorted_pokemon = sorted(
        pokemon_stats.items(),
        key=lambda item: item[1].get("usage", 0),
        reverse=True
    )
    # print(pokemon_stats)


    # Print them out nicely
    df = pd.DataFrame(columns=["name","types","weight","hp","atk","def","spatk","spdef","speed"])
    for rank, (name, stats) in enumerate(sorted_pokemon, 1):
        # print(f"{rank}. {name}: {stats['usage']:.2%}")
        if name == "Palafin":
            write_mon_data("palafin-zero", df)
            name = "palafin-hero"
        
        df = write_mon_data(name, df)
    # myFile = open(os.path.join("data","clean","info.txt"),"a")
    df.to_csv(os.path.join("data","dex",f"{format}.txt"))

def write_mon_data(name, df):
    # mon_dict = {"name","type1","type2","weight","hp","atk","def","spatk","spdef","speed"}
    stats, types, weight = get_pokemon_base_info(name)
    if len(types) > 1: types = [f"{types[0]}/{types[1]}"]
    mon_data = [name, types.pop(), weight]
    for stat in stats:
        # print(f"{stat}:{stats[stat]}")
        mon_data.append(stats[stat])
    df.loc[len(df)] = mon_data
    return df

def reverse_damage_calc(field, attacker, target, num_targets):
    # Objects storing field info, attacker stats, weight, etc and same for target
    # Try to find out defence of opponent
    possible_rand_vals = [i/100 for i in range (85,101)]
    multiplier = 1
    multiplier *= 0.75 if num_targets > 1 else 1
    
get_all_mons()