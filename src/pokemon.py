import pandas as pd
import numpy as np
import os
import math

from utils import *
from backend import *

# Raw count (int): Number of teams that used this mon
# Viability ceiling [count, max_gxe, gxe_1%, gxe_20%]: Recommended use gxe_1%
# Abilities ({ability: usage %})
# Items ({item: usage %})
# Spreads {"nature:hp/atk/def/spatk/spdef/spd":count}
# Moves {move:count}
# Teammates {teammate:count}
# Checks and Counters {check/counter:[count appeared on opposite teams, ko/force switch out %, std]}
class OpponentTeam:
    def __init__(self, mon1, mon2, mon3, mon4, mon5, mon6, format = "gen9vgc2025regi-1760"):
        # Define team members
        self.mon1 = OpponentMon(mon1, format)
        self.mon2 = OpponentMon(mon2, format)
        self.mon3 = OpponentMon(mon3, format)
        self.mon4 = OpponentMon(mon4, format)
        self.mon5 = OpponentMon(mon5, format)
        self.mon6 = OpponentMon(mon6, format)
        
        # Set all team members to inactive initially
        self.isMon1Active = False
        self.isMon2Active = False
        self.isMon3Active = False
        self.isMon4Active = False
        self.isMon5Active = False
        self.isMon6Active = False
        
        # Which pokemon were chosen by opponent
        self.isMon1Chosen = False
        self.isMon2Chosen = False
        self.isMon3Chosen = False
        self.isMon4Chosen = False
        self.isMon5Chosen = False
        self.isMon6Chosen = False
        
        self.numUnfainted = 0
        self.usedTera = False
        
class OpponentMon:
    def __init__(self, name, format="gen9vgc2025regi-1760"):
        self.name = name
        self.format = format
        self.isActive = False
        self.isChosen = False
        self.isFainted = False
        self.status = None
        # Assign Base Stats
        self.baseHP = self.get_mon_base_stat("hp")
        self.baseAttack = self.get_mon_base_stat("atk")
        self.baseDefence = self.get_mon_base_stat("def")
        self.baseSpecialAttack = self.get_mon_base_stat("spa")
        self.baseSpecialDefence = self.get_mon_base_stat("spd")
        self.baseSpeed = self.get_mon_base_stat("spe")
        
        # Get most used item, ability and tera
        self.isItemKnown = self.check_if_required("Items")
        self.item = self.get_most_used('Items')
        self.ability = self.get_most_used('Abilities')
        self.isAbilityKnown = self.check_if_required("Abilities")
        self.tera = self.get_most_used("Tera Types")
        self.isTeraKnown = self.check_if_required("Tera Types")
        
        # Set moves to most common
        self.set_most_common_moves()
        self.ismove1known = False
        self.ismove2known = False
        self.ismove3known = False
        self.ismove4known = False
        
        # Conditions wrt choice items
        self.lastUsedMove = None
        self.isChoiceLocked = False
        
        # Initialise Attack and Speed IV ranges
        self.MaxAttackIV = 31
        self.minAttackIV = 0
        self.maxSpeedIV = 31
        self.minSpeedIV = 0
        
        # Set most likely IV spreads - almost always 31
        self.likelyAtkIV = 31 * (self.baseSpecialAttack < self.baseAttack)
        self.likelyDefIV = 31
        self.likelySpaIV = 31
        self.likelySpdIV = 31
        self.likelySpeIV = 31
        self.likelyHPIV = 31
        # Initialise possible EV ranges
        self.unknownEVs = 510
        
        self.minHPEV = 0
        self.maxHPEV = 252
        self.commonHPEV = 0
        
        self.minAtkEV = 0
        self.maxAtkEV = 252
        self.commonAtkEV = 0
        
        self.minDefEV = 0
        self.maxDefEV = 252
        self.commonDefEV = 0
        
        self.minSpaEV = 0
        self.maxSpaEV = 252
        self.commonSpaEV = 0
        
        self.minSpdEV = 0
        self.maxSpdEV = 252
        self.commonSpdEV = 0
        
        self.minSpeEV = 0
        self.maxSpeEV = 252
        self.commonSpeEV = 0
        
        # Initialise possible stat ranges
        self.maxHP = self.get_max_hp()
        self.minHP = self.get_min_hp()
        
        self.minAtkStat = 0
        self.maxAtkStat = 252
        
        self.minDefStat = 0
        self.maxDefStat = 252
        
        self.minSpaStat = 0
        self.maxSpaStat = 252
        
        self.minSpdStat = 0
        self.maxSpdStat = 252
        
        self.minSpeStat = 0
        self.maxSpeStat = 252
        
        self.nature = "Adamant"
        self.isNatureKnown = False
        
        #  Assume most common spreads are opponent's spreads
        self.get_most_used("Spreads")
        
        self.statDict = {
            "atk": {
                "base": self.baseAttack,
                "minIV": self.minAttackIV,
                "maxIV": self.MaxAttackIV,
                "minEV": self.minAtkEV,
                "maxEV": self.maxAtkEV,
                "commonEV": self.commonAtkEV,
                "likelyIV": self.likelyAtkIV
            },
            "def": {
                "base": self.baseDefence,
                "minIV": 31,
                "maxIV": 31,
                "minEV": self.minDefEV,
                "maxEV": self.maxDefEV,
                "commonEV": self.commonDefEV,
                "likelyIV": self.likelyDefIV
            },
            "spa": {
                "base": self.baseSpecialAttack,
                "minIV": 31,
                "maxIV": 31,
                "minEV": self.minSpaEV,
                "maxEV": self.maxSpaEV,
                "commonEV": self.commonSpaEV,
                "likelyIV": self.likelySpaIV
            },
            "spd": {
                "base": self.baseSpecialDefence,
                "minIV": 31,
                "maxIV": 31,
                "minEV": self.minSpdEV,
                "maxEV": self.maxSpdEV,
                "commonEV": self.commonSpdEV,
                "likelyIV": self.likelySpdIV
            },
            "spe": {
                "base": self.baseSpeed,
                "minIV": self.minSpeedIV,
                "maxIV": self.maxSpeedIV,
                "minEV": self.minSpeEV,
                "maxEV": self.maxSpeEV,
                "commonEV": self.commonSpeEV,
                "likelyIV": self.likelySpeIV
            },
        }
        
        self.currentHP = self.get_raw_hp_common()
        
        # Initialise most common stats
        self.maxRawAtk = self.get_raw_stat_max('atk')
        self.minRawAtk = self.get_raw_stat_min('atk')
        self.commonRawAtk = self.get_raw_stat_common('atk')
        
        self.maxRawDef = self.get_raw_stat_max('def')
        self.minRawDef = self.get_raw_stat_min('def')
        self.commonRawDef = self.get_raw_stat_common('def')
        
        self.maxRawSpa = self.get_raw_stat_max('spa')
        self.minRawSpa = self.get_raw_stat_min('spa')
        self.commonRawSpa = self.get_raw_stat_common('spa')
        
        self.maxRawSpd = self.get_raw_stat_max('spd')
        self.minRawSpd = self.get_raw_stat_min('spd')
        self.commonRawSpd = self.get_raw_stat_common('spd')
        
        self.maxRawSpe = self.get_raw_stat_max('spe')
        self.minRawSpe = self.get_raw_stat_min('spe')
        self.commonRawSpe = self.get_raw_stat_common('spe')
        
        self.atkBoosts = 0
        self.defBoosts = 0
        self.spaBoosts = 0
        self.spdBoosts = 0
        self.speBoosts = 0
        
    def get_mon_base_stat(self, stat):
        df = pd.read_csv(os.path.join("data","dex","gen9vgc2025regi-1760.txt"))
        opponent = df.loc[df['name'] == self.name, stat].values[0]
        return opponent

    def get_max_hp(self):
        return math.floor((2*self.baseHP+self.likelyHPIV+math.floor(self.maxHPEV/4)))+60
    
    def get_min_hp(self):
        return math.floor((2*self.baseHP+self.likelyHPIV+math.floor(self.minHPEV/4)))+60

    def calc_opponent_hp_ev(self):
        hp_ev = 4*((100*self.maxHP-6000)/50 - (2*self.baseHP + 31))
        return max(0,hp_ev)
    
    def get_raw_stat_min(self, stat):
        base = self.statDict[stat]["base"]
        # print(self.nature_multiplier(stat))
        return math.floor((math.floor((2*base+self.statDict[stat]["likelyIV"]+self.statDict[stat]["minEV"]//4)*50/100)+5)*self.nature_multiplier(stat))
    
    def get_raw_stat_max(self, stat):
        base = self.statDict[stat]["base"]
        return math.floor((math.floor((2*base+self.statDict[stat]["maxIV"]+self.statDict[stat]["maxEV"]//4)*50/100)+5)*self.nature_multiplier(stat))
    
    def get_raw_stat_common(self, stat):
        base = self.statDict[stat]["base"]
        return math.floor((math.floor((2*base+self.statDict[stat]["likelyIV"]+self.statDict[stat]["commonEV"]//4)*50/100)+5)*self.nature_multiplier(stat))
    
    def get_raw_hp_common(self):
        return math.floor((2*self.baseHP+self.likelyHPIV+math.floor(self.commonHPEV/4))*50/100)+60
    
    def get_most_used(self, col):
        pkmn_data = get_pokemon_smogon_info(self.name, self.format)
        info =  max(pkmn_data[col], key=pkmn_data[col].get)
        if col == "Spreads":
            self.nature, EVs = info.split(":")
            self.commonHPEV, self.commonAtkEV, self.commonDefEV, self.commonSpaEV, self.commonSpdEV, self.commonSpeEV = [int(EV) for EV in EVs.split("/")]
        else:
            return info
    
    def check_if_required(self, col):
        pkmn_data = get_pokemon_smogon_info(self.name, self.format)
        info =  pkmn_data[col]
        return len(info) == 1
    
    def nature_multiplier(self, stat):
        return nature_table[stat][self.nature] if self.nature in nature_table[stat] else 1
    
    def set_most_common_moves(self):
        pkmn_data = get_pokemon_smogon_info(self.name, self.format)
        sorted_moves =  sorted(pkmn_data["Moves"], key=pkmn_data["Moves"].get, reverse=True)
        self.move1, self.move2, self.move3, self.move4 = sorted_moves[:4]
    
    def reverse_damage_calc(self, damage):
        pass

mon = OpponentMon("Urshifu-Rapid-Strike")
print(mon.baseAttack)
print(mon.nature)
print(mon.commonAtkEV)
print(mon.likelyAtkIV)
print(mon.minRawAtk)
