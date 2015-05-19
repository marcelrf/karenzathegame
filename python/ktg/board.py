# coding: utf-8

import random

# board indexes
# numbers for sword positions
#   1     2
#
#   3     4
S1, S2, S3, S4 = range(4)

# other enumerations
NO_SWORD, SWORD = range(2)

class Board(object):

    def __init__(self):
        self.sword_squares = [NO_SWORD for i in range(4)]

    def __copy__(self):
        other = Board()
        other.sword_squares = list(self.sword_squares)
        return other

    def __eq__(self, other):
        return self.sword_squares == other.sword_squares

    def __str__(self):
        sword_codes = {
            SWORD:    's',
            NO_SWORD: '·',
        }
        text  = ' ,-----------, \n'
        text += '/             \\\n'
        text += '|   %s     %s   |\n'
        text += '|             |\n'
        text += '|   %s     %s   |\n'
        text += '\             /\n'
        text += ' \'-----------\''
        instantiation = (
            sword_codes[self.sword_squares[S1]],
            sword_codes[self.sword_squares[S2]],
            sword_codes[self.sword_squares[S3]],
            sword_codes[self.sword_squares[S4]],
        )
        return (text % instantiation)

    def random(self):
        sword_choices = range(4)
        self.sword = random.choice(sword_choices)

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

    def leads_to(self, card):
        return self.sword == card.sword_origin

    def move_sword_as_in(self, card):
        if self.sword != card.sword_origin:
            raise Exception("Card not playable")
        self.sword = card.sword_destiny
