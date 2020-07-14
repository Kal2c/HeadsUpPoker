class Player:

    def __init__(self, name, starting_stack=100.00):
        self.name = name
        self.stack = starting_stack
        self.all_in = False
        self.put_in_pot_pre = 0
        self.put_in_pot_flop = 0
        self.put_in_pot_turn = 0
        self.put_in_pot_river = 0
