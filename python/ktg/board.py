# coding: utf-8

import random

# board indexes
# letters for feet positions
# numbers for sword positions
#      A
#   1     2
# B         C
#   3     4
#      D
FA, FB, FC, FD = range(4)
S1, S2, S3, S4 = range(4)

# other enumerations
NO_FOOT, LEFT_FOOT, RIGHT_FOOT = range(3)
NO_SWORD, SWORD = range(2)

FEET_POSITIONS = [FA, FB, FC, FD]
SWORD_POSITIONS = [S1, S2, S3, S4]

class Board(object):

    def __init__(self):
        self.foot_squares = [NO_FOOT for i in range(4)]
        self.sword_squares = [NO_SWORD for i in range(4)]

    def __copy__(self):
        other = Board()
        other.foot_squares = list(self.foot_squares)
        other.sword_squares = list(self.sword_squares)
        return other

    def __eq__(self, other):
        return (
            self.foot_squares == other.foot_squares and
            self.sword_squares == other.sword_squares
        )

    def __str__(self):
        foot_codes = {
            LEFT_FOOT: 'L',
            RIGHT_FOOT: 'R',
            NO_FOOT: '·',
        }
        sword_codes = {
            SWORD: 'o',
            NO_SWORD: ' ',
        }
        text  = "   .---------.   \n"
        text += "  /     %s     \\  \n"
        text += " /   %s     %s   \\ \n"
        text += "|  %s         %s  |\n"
        text += " \   %s     %s   / \n"
        text += "  \     %s     /  \n"
        text += "   '---------'   "
        instantiation = (
            foot_codes[self.foot_squares[FA]],
            sword_codes[self.sword_squares[S1]],
            sword_codes[self.sword_squares[S2]],
            foot_codes[self.foot_squares[FB]],
            foot_codes[self.foot_squares[FC]],
            sword_codes[self.sword_squares[S3]],
            sword_codes[self.sword_squares[S4]],
            foot_codes[self.foot_squares[FD]],
        )
        return (text % instantiation)

    def random(self):
        feet_choices = range(4)
        self.left_foot = random.choice(feet_choices)
        feet_choices.pop(self.left_foot)
        self.right_foot = random.choice(feet_choices)
        sword_choices = range(4)
        self.sword = random.choice(sword_choices)

    @property
    def left_foot(self):
        if LEFT_FOOT in self.foot_squares:
            return self.foot_squares.index(LEFT_FOOT)
        else: return None
    @left_foot.setter
    def left_foot(self, value):
        del self.left_foot
        self.foot_squares[value] = LEFT_FOOT
    @left_foot.deleter
    def left_foot(self):
        for i in range(4):
            if self.foot_squares[i] == LEFT_FOOT:
                self.foot_squares[i] = NO_FOOT

    @property
    def right_foot(self):
        if RIGHT_FOOT in self.foot_squares:
            return self.foot_squares.index(RIGHT_FOOT)
        else: return None
    @right_foot.setter
    def right_foot(self, value):
        del self.right_foot
        self.foot_squares[value] = RIGHT_FOOT
    @right_foot.deleter
    def right_foot(self):
        for i in range(4):
            if self.foot_squares[i] == RIGHT_FOOT:
                self.foot_squares[i] = NO_FOOT

    @property
    def sword(self):
        if SWORD in self.sword_squares:
            return self.sword_squares.index(SWORD)
        else: return None
    @sword.setter
    def sword(self, value):
        del self.sword
        self.sword_squares[value] = SWORD
    @sword.deleter
    def sword(self):
        for i in range(4):
            if self.sword_squares[i] == SWORD:
                self.sword_squares[i] = NO_SWORD

    def distance_to(self, card):
        conditions = [
            self.left_foot != card.left_foot,
            self.right_foot != card.right_foot,
            (self.left_foot == card.right_foot and
             self.right_foot == card.left_foot),
            self.sword != card.sword_origin,
        ]
        distance = map(lambda x: 1 if x else 0, conditions)
        return reduce(lambda x, y: x + y, distance)

