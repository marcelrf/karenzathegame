# coding: utf-8

import random

# card indexes
# numbers for sword positions
#   1     2
#
#   3     4
S1, S2, S3, S4 = range(4)

# other enumerations
NO_POWER = None
NO_TYPE, ATTACK, DEFENSE = range(3)
NO_SWORD, SWORD_ORIGIN, SWORD_DESTINY = range(3)

class Card(object):

    def __init__(self, json_object=None):
        if json_object is None:
            self.type = NO_TYPE
            self.power = NO_POWER
            self.sword = [NO_SWORD for i in range(4)]
        else:
            self.type = json_object['type']
            self.power = json_object['power']
            self.sword = json_object['sword']

    def __copy__(self):
        other = Card()
        other.type = self.type
        other.power = self.power
        other.sword = list(self.sword)
        return other

    def __eq__(self, other):
        return (
            self.type == other.type and
            self.power == other.power and
            self.sword == other.sword
        )

    def __str__(self):
        type_codes = {
            ATTACK:   'Attack ',
            DEFENSE:  'Defense',
            NO_TYPE:  '       ',
        }
        sword_codes = {
            SWORD_ORIGIN:   'o',
            SWORD_DESTINY:  'x',
            NO_SWORD: '·',
        }
        text  = '.-------------.\n'
        text += '| %s (%d) |\n'
        text += '|             |\n'
        text += '|   %s     %s   |\n'
        text += '|             |\n'
        text += '|   %s     %s   |\n'
        text += '|             |\n'
        text += '\'-------------\''
        instantiation = (
            type_codes[self.type],
            self.power or 0,
            sword_codes[self.sword[S1]],
            sword_codes[self.sword[S2]],
            sword_codes[self.sword[S3]],
            sword_codes[self.sword[S4]],
        )
        return (text % instantiation)

    def reverse_str(self):
        text  = '.-------------.\n'
        text += '|             |\n'
        text += '|             |\n'
        text += '|             |\n'
        text += '|             |\n'
        text += '|             |\n'
        text += '|             |\n'
        text += '\'-------------\''
        return text

    def to_json_object(self):
        return {
            'type': self.type,
            'power': self.power,
            'sword': self.sword,
        }

    @property
    def sword_origin(self):
        if SWORD_ORIGIN in self.sword:
            return self.sword.index(SWORD_ORIGIN)
        else: return None
    @sword_origin.setter
    def sword_origin(self, value):
        del self.sword_origin
        self.sword[value] = SWORD_ORIGIN
    @sword_origin.deleter
    def sword_origin(self):
        for i in range(4):
            if self.sword[i] == SWORD_ORIGIN:
                self.sword[i] = NO_SWORD

    @property
    def sword_destiny(self):
        if SWORD_DESTINY in self.sword:
            return self.sword.index(SWORD_DESTINY)
        else: return None
    @sword_destiny.setter
    def sword_destiny(self, value):
        del self.sword_destiny
        self.sword[value] = SWORD_DESTINY
    @sword_destiny.deleter
    def sword_destiny(self):
        for i in range(4):
            if self.sword[i] == SWORD_DESTINY:
                self.sword[i] = NO_SWORD

    def random(self):
        self.type = random.randint(1, 2)
        self.power = random.randint(1, 9)
        sword_choices = range(4)
        self.sword_origin = random.choice(sword_choices)
        sword_choices.pop(self.sword_origin)
        self.sword_destiny = random.choice(sword_choices)

    def is_legal(self):
        return (
            self.type in range(1, 3) and
            self.power in range(1, 10) and
            self.sword.count(SWORD_ORIGIN) == 1 and
            self.sword.count(SWORD_DESTINY) == 1
        )

    def leads_to(self, other):
        # assumes the cards are legal
        return self.sword_destiny == other.sword_origin
