# coding: utf-8

import random
import json

# card indexes
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
NO_POWER = None
NO_TYPE, ATTACK, DEFENSE = range(3)
NO_FOOT, LEFT_FOOT, RIGHT_FOOT = range(3)
NO_SWORD, SWORD_ORIGIN, SWORD_DESTINY = range(3)

class Card(object):

    def __init__(self, json_text=None):
        if json_text is None:
            self.type = NO_TYPE
            self.power = NO_POWER
            self.feet = [NO_FOOT for i in range(4)]
            self.sword = [NO_SWORD for i in range(4)]
        else:
            json_object = json.loads(json_text)
            self.type = json_object['type']
            self.power = json_object['power']
            self.feet = json_object['feet']
            self.sword = json_object['sword']

    def __copy__(self):
        other = Card()
        other.type = self.type
        other.power = self.power
        other.feet = list(self.feet)
        other.sword = list(self.sword)
        return other

    def __eq__(self, other):
        return (
            self.type == other.type and
            self.power == other.power and
            self.feet == other.feet and
            self.sword == other.sword
        )

    def __str__(self):
        type_codes = {
            ATTACK: 'Attack ',
            DEFENSE: 'Defense',
            NO_TYPE: 'Unknown',
        }
        foot_codes = {
            LEFT_FOOT: 'L',
            RIGHT_FOOT: 'R',
            NO_FOOT: '·',
        }
        sword_codes = {
            SWORD_ORIGIN: 'o',
            SWORD_DESTINY: 'x',
            NO_SWORD: ' ',
        }
        text  = ".-------------.\n"
        text += "| %s (%d) |\n"
        text += "|      %s      |\n"
        text += "|   %s     %s   |\n"
        text += "| %s         %s |\n"
        text += "|   %s     %s   |\n"
        text += "|      %s      |\n"
        text += "'-------------'"
        instantiation = (
            type_codes[self.type],
            self.power or 0,
            foot_codes[self.feet[FA]],
            sword_codes[self.sword[S1]],
            sword_codes[self.sword[S2]],
            foot_codes[self.feet[FB]],
            foot_codes[self.feet[FC]],
            sword_codes[self.sword[S3]],
            sword_codes[self.sword[S4]],
            foot_codes[self.feet[FD]],
        )
        return (text % instantiation)

    def to_json(self):
        return json.dumps({
            "type": self.type,
            "power": self.power,
            "feet": self.feet,
            "sword": self.sword,
        })

    @property
    def left_foot(self):
        if LEFT_FOOT in self.feet:
            return self.feet.index(LEFT_FOOT)
        else: return None
    @left_foot.setter
    def left_foot(self, value):
        del self.left_foot
        if value is not None:
            self.feet[value] = LEFT_FOOT
    @left_foot.deleter
    def left_foot(self):
        for i in range(4):
            if self.feet[i] == LEFT_FOOT:
                self.feet[i] = NO_FOOT

    @property
    def right_foot(self):
        if RIGHT_FOOT in self.feet:
            return self.feet.index(RIGHT_FOOT)
        else: return None
    @right_foot.setter
    def right_foot(self, value):
        del self.right_foot
        if value is not None:
            self.feet[value] = RIGHT_FOOT
    @right_foot.deleter
    def right_foot(self):
        for i in range(4):
            if self.feet[i] == RIGHT_FOOT:
                self.feet[i] = NO_FOOT

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
        feet_choices = range(4) + [None]
        self.left_foot = random.choice(feet_choices)
        feet_choices.pop(self.left_foot)
        if self.left_foot is None: feet_choices.append(None)
        self.right_foot = random.choice(feet_choices)
        sword_choices = range(4)
        self.sword_origin = random.choice(sword_choices)
        sword_choices.pop(self.sword_origin)
        self.sword_destiny = random.choice(sword_choices)

    def is_legal(self):
        return (
            self.type in [ATTACK, DEFENSE] and
            self.power in range(1, 10) and
            self.sword.count(SWORD_ORIGIN) == 1 and
            self.sword.count(SWORD_DESTINY) == 1
        )

    def leads_to(self, other):
        # assumes the cards are legal
        return self.sword_destiny == other.sword_origin

    def distance_to(self, other):
        # assumes the cards are legal and self leads to other
        conditions = [
            self.left_foot is not None and other.left_foot is not None and self.left_foot != other.left_foot,
            self.right_foot is not None and other.right_foot is not None and self.right_foot != other.right_foot,
            (
                self.left_foot is not None and self.right_foot is not None and
                self.left_foot == other.right_foot and self.right_foot == other.left_foot
            )
        ]
        distance = map(lambda x: 1 if x else 0, conditions)
        return reduce(lambda x, y: x + y, distance)
