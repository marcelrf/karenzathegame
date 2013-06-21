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
NO_TYPE, ATTACK, DEFENSE = range(3)
NO_FOOT, LEFT_FOOT, RIGHT_FOOT = range(3)
NO_SWORD, SWORD_ORIGIN, SWORD_DESTINY = range(3)
FRONT, MID, BACK = range(3)
STRAIGHT, LATERAL, REVERSE = range(3)
SHORT, LONG = range(2)
ASCENDANT, HORIZONTAL, DESCENDANT = range(3)
ALIGNED, SEMI_ALIGNED, NOT_ALIGNED = range(3)

# feet angles respect horizontal (in degrees)
FEET_ANGLES = {
    FA: {FB: 45, FC: 135, FD: 90},
    FB: {FA: 45, FC: 0, FD: 135},
    FC: {FA: 135, FB: 0, FD: 45},
    FD: {FA: 90, FB: 135, FC: 45},
}
# trajectory angles respect horizontal (in degrees)
TRAJECTORY_ANGLES = {
    S1: {S2: 0, S3: 90, S4: 135},
    S2: {S1: 0, S3: 45, S4: 90},
    S3: {S1: 90, S2: 45, S4: 0},
    S4: {S1: 135, S2: 90, S3: 0},
}

FEET_POSITIONS = [FA, FB, FC, FD]
SWORD_POSITIONS = [S1, S2, S3, S4]

class Card(object):

    def __init__(self, json_text=None):
        if json_text is None:
            self.type = NO_TYPE
            self.power = 0
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
            self.power,
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
        feet_choices = range(4)
        self.left_foot = random.choice(feet_choices)
        feet_choices.pop(self.left_foot)
        self.right_foot = random.choice(feet_choices)
        sword_choices = range(4)
        self.sword_origin = random.choice(sword_choices)
        sword_choices.pop(self.sword_origin)
        self.sword_destiny = random.choice(sword_choices)

    def is_legal(self):
        return (
            self.type in [ATTACK, DEFENSE] and
            self.power in range(1, 10) and
            self.feet.count(LEFT_FOOT) == 1 and
            self.feet.count(RIGHT_FOOT) == 1 and
            self.sword.count(SWORD_ORIGIN) == 1 and
            self.sword.count(SWORD_DESTINY) == 1
        )

    def feet_level(self):
        # assumes the card is legal
        if NO_FOOT not in [self.feet[FA], self.feet[FD]]: return MID
        elif self.feet[FA] != NO_FOOT: return FRONT
        elif self.feet[FD] != NO_FOOT: return BACK
        else: return MID

    def feet_orientation(self):
        # assumes the card is legal
        if LEFT_FOOT == self.feet[FB] or RIGHT_FOOT == self.feet[FC]:
            return STRAIGHT
        elif LEFT_FOOT == self.feet[FC] or RIGHT_FOOT == self.feet[FB]:
            return REVERSE
        else: return LATERAL

    def trajectory_length(self):
        # assumes the card is legal
        if (SWORD_ORIGIN == self.sword[S1] and SWORD_DESTINY == self.sword[S4] or
            SWORD_ORIGIN == self.sword[S4] and SWORD_DESTINY == self.sword[S1] or
            SWORD_ORIGIN == self.sword[S2] and SWORD_DESTINY == self.sword[S3] or
            SWORD_ORIGIN == self.sword[S3] and SWORD_DESTINY == self.sword[S2]):
            return LONG
        else: return SHORT

    def trajectory_direction(self):
        # assumes the card is legal
        if SWORD_ORIGIN in [self.sword[S1], self.sword[S2]]:
            if SWORD_DESTINY in [self.sword[S1], self.sword[S2]]:
                return HORIZONTAL
            else: return DESCENDANT
        elif SWORD_ORIGIN in [self.sword[S3], self.sword[S4]]:
            if SWORD_DESTINY in [self.sword[S1], self.sword[S2]]:
                return ASCENDANT
            else: return HORIZONTAL

    def feet_angle(self):
        # assumes the card is legal
        return FEET_ANGLES[self.left_foot][self.right_foot]

    def trajectory_angle(self):
        # assumes the card is legal
        return TRAJECTORY_ANGLES[self.sword_origin][self.sword_destiny]

    def alignment(self):
        alignment = abs(self.feet_angle() - self.trajectory_angle())
        if alignment == 0: return ALIGNED
        elif alignment in [45, 135]: return SEMI_ALIGNED
        else: return NOT_ALIGNED

    def distance_to(self, other):
        # assumes the card is legal
        conditions = [
            self.left_foot != other.left_foot,
            self.right_foot != other.right_foot,
            (self.left_foot == other.right_foot and
             self.right_foot == other.left_foot),
            self.sword_destiny != other.sword_origin,
        ]
        distance = map(lambda x: 1 if x else 0, conditions)
        return reduce(lambda x, y: x + y, distance)
