class Field:
    def __init__(self, num_mons_side_a, num_mons_side_b):
        self.num_mons_side_a = num_mons_side_a
        self.num_mons_side_b = num_mons_side_b
        self.electric_terrain = False
        self.psychic_terrain = False
        self.misty_terrain = False
        self.grassy_terrain = False
        self.rain = False
        self.sun = False
        self.sand = False
        self.snow = False