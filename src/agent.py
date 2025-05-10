import poke_env as env
from gymnasium.spaces import Space, Box
import poke_env as env


class VGCPlayer():
    def __init__(self):
        super().__init__()
        # Observation space format
        # base power move i pokemon 1a
        # base power move i pokemon 1b
        # damage multiplier of each move from pokemon 1a to pokemon 2a
        # damage multipler of each move from pokemon 1b to pokemon 2b
        # damage multiplier of each move from pokemon 1c to pokemon 2a
        # damage multipler of each move from pokemon 1d to pokemon 2b
        # Number of non-fainted mons in our team
        # Number of non-fainted mons in opponent team
        # Pokemon 1a stats
        # Pokemon 1b stats
        # Pokemon 1c stats
        # Pokemon 1d stats
        # Pokemon 2a base stats
        # Pokemon 2b base stats
        # Pokemon 2c base stats
        # Pokemon 2d base stats
        # Pokemon 2a predicted stats
        # Pokemon 2b predicted stats
        # Pokemon 2c predicted stats
        # Pokemon 2d predicted stats
        # Pokemon 2a possible stat range
        # Pokemon 2b possible stat range
        # Pokemon 2c possible stat range
        # Pokemon 2d possible stat range
        # Pokemon 2a predicted moves
        # Pokemon 2b predicted moves
        # Pokemon 2c predicted moves
        # Pokemon 2d predicted moves
        # Each pokemon's type
        # Can agent tera?
        # can opponent tera?
        # Pokemon 1a-d tera type
        # Pokemon 2a-d possible tera types
        # Prediction of what pokemon are in the back if not known
        # Every pokemon's temporary stats (stat boosts/changes)
        # Every pokemon's ability 
        # Status condition of every pokemon
        # What level each pokemon is
        # What item each pokemon is holding
        # What pokemon cant use which moves this turn
        # Field effects - incl. perish song, arena trap
        # Each pokemon's weight
        # Is commonly checked by opponent?
        # 