# coding: UTF-8

import random

# card indexes
# letters for feet positions
# numbers for sword positions
#      A
#   1     2
# B         C
#  3       4
#   D  5  E
FA, FB, FC, FD, FE = range(5)
S1, S2, S3, S4, S5 = range(5)

# other enumerations
NO_TYPE, ATTACK, DEFENSE = range(3)
NO_FOOT, LEFT_FOOT, RIGHT_FOOT = range(3)
NO_SWORD, SWORD_ORIGIN, SWORD_DESTINY = range(3)
FRONT, FRONT_MID, MID, MID_BACK, BACK = range(5)
STRAIGHT, REVERSE = range(2)
SHORT, LONG = range(2)
ASCENDANT, HORIZONTAL, DESCENDANT = range(3)
ALIGNED, SEMI_ALIGNED, NOT_ALIGNED = range(3)

# feet angles respect horizontal (in degrees)
FEET_ANGLES = {
    FA: {FB: 36, FC: 144, FD: 72, FE: 108},
    FB: {FA: 36, FC: 0, FD: 108, FE: 144},
    FC: {FA: 144, FB: 0, FD: 36, FE: 72},
    FD: {FA: 72, FB: 108, FC: 36, FE: 0},
    FE: {FA: 108, FB: 144, FC: 72, FD: 0},
}
# trajectory angles respect horizontal (in degrees)
TRAJECTORY_ANGLES = {
    S1: {S2: 0, S3: 72, S4: 144, S5: 108},
    S2: {S1: 0, S3: 36, S4: 108, S5: 72},
    S3: {S1: 72, S2: 36, S4: 0, S5: 144},
    S4: {S1: 144, S2: 108, S3: 0, S5: 36},
    S5: {S1: 108, S2: 72, S3: 144, S4: 36},
}

class Card(object):

    def __init__(self):
        self.name = ''
        self.image = None
        self.type = NO_TYPE
        self.power = 0
        self.feet = [NO_FOOT for i in range(5)]
        self.sword = [NO_SWORD for i in range(5)]

    def __copy__(self):
        other = Card()
        other.name = self.name
        other.image = self.image
        other.type = self.type
        other.power = self.power
        other.feet = list(self.feet)
        other.sword = list(self.sword)
        return other

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.image == other.image and
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
        text += "| %s |\n"
        text += "| %s (%d) |\n"
        text += "|      %s      |\n"
        text += "|   %s     %s   |\n"
        text += "| %s         %s |\n"
        text += "|  %s       %s  |\n"
        text += "|   %s  %s  %s   |\n"
        text += "'-------------'"
        if self.name == '':
            name_text = 'No name    '
        else: name_text = self.name[:11].ljust(11)
        instantiation = (
            name_text,
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
            sword_codes[self.sword[S5]],
            foot_codes[self.feet[FE]],
        )
        return (text % instantiation)

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
        for i in range(5):
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
        for i in range(5):
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
        for i in range(5):
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
        for i in range(5):
            if self.sword[i] == SWORD_DESTINY:
                self.sword[i] = NO_SWORD

    def random(self):
        self.name = ''
        self.image = None
        self.type = random.randint(1, 2)
        self.power = random.randint(1, 9)
        feet_choices = range(5)
        self.left_foot = random.choice(feet_choices)
        feet_choices.pop(self.left_foot)
        self.right_foot = random.choice(feet_choices)
        sword_choices = range(5)
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
        if self.feet[FA] != NO_FOOT:
            if self.feet[FB] + self.feet[FC] != NO_FOOT:
                return FRONT
            else: return MID
        elif self.feet[FB] + self.feet[FC] != NO_FOOT:
            if self.feet[FD] + self.feet[FE] != NO_FOOT:
                return MID_BACK
            else: return FRONT_MID
        else: return BACK

    def feet_orientation(self):
        # assumes the card is legal
        if LEFT_FOOT == self.feet[FA]:
            if RIGHT_FOOT in [self.feet[FC], self.feet[FE]]:
                return STRAIGHT
            else: return REVERSE
        elif LEFT_FOOT == self.feet[FD]:
            if RIGHT_FOOT != self.feet[FB]: return STRAIGHT
            else: return REVERSE
        elif LEFT_FOOT == self.feet[FE]:
            if RIGHT_FOOT == self.feet[FC]: return STRAIGHT
            else: return REVERSE
        elif LEFT_FOOT == self.feet[FC]: return REVERSE
        else: return STRAIGHT

    def trajectory_length(self):
        # assumes the card is legal
        if SWORD_ORIGIN == self.sword[S1]:
            if SWORD_DESTINY in [self.sword[S2], self.sword[S3]]:
                return SHORT
            else: return LONG
        elif SWORD_ORIGIN == self.sword[S2]:
            if SWORD_DESTINY in [self.sword[S1], self.sword[S4]]:
                return SHORT
            else: return LONG
        elif SWORD_ORIGIN == self.sword[S3]:
            if SWORD_DESTINY in [self.sword[S1], self.sword[S5]]:
                return SHORT
            else: return LONG
        elif SWORD_ORIGIN == self.sword[S4]:
            if SWORD_DESTINY in [self.sword[S2], self.sword[S5]]:
                return SHORT
            else: return LONG
        else:
            if SWORD_DESTINY in [self.sword[S3], self.sword[S4]]:
                return SHORT
            else: return LONG

    def trajectory_direction(self):
        # assumes the card is legal
        if SWORD_ORIGIN in [self.sword[S1], self.sword[S2]]:
            if SWORD_DESTINY in [self.sword[S1], self.sword[S2]]:
                return HORIZONTAL
            else: return DESCENDANT
        elif SWORD_ORIGIN in [self.sword[S3], self.sword[S4]]:
            if SWORD_DESTINY == self.sword[S5]: return DESCENDANT
            elif SWORD_DESTINY in [self.sword[S1], self.sword[S2]]:
                return ASCENDANT
            else: return HORIZONTAL
        else: return ASCENDANT

    def feet_angle(self):
        # assumes the card is legal
        return FEET_ANGLES[self.left_foot][self.right_foot]

    def trajectory_angle(self):
        # assumes the card is legal
        return TRAJECTORY_ANGLES[self.sword_origin][self.sword_destiny]

    def alignment(self):
        alignment = abs(self.feet_angle() - self.trajectory_angle())
        if alignment == 0: return ALIGNED
        elif alignment in [36, 144]: return SEMI_ALIGNED
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
