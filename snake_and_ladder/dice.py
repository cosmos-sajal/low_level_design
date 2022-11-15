import random


class Dice:
    MIN_DICE_VAL = 1
    MAX_DICE_VAL = 6

    def __init__(self):
        self.current_value = 0

    def roll_dice(self):
        return random.randint(
            self.MIN_DICE_VAL, self.MAX_DICE_VAL)
