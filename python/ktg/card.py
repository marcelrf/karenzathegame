# coding: utf-8

# card indexes
# numbers for sword positions
#   1     2
#
#   3     4
S1, S2, S3, S4 = range(4)

# other enumerations
NO_POWER = None
NO_TYPE, ATTACK, DEFENSE, SPECIAL = [None, 'attack', 'defense', 'special']
NO_SWORD, SWORD_ORIGIN, SWORD_DESTINY = range(3)

class Card(object):

    def __init__(self, json_object=None):
        if json_object is None:
            self.fighter = ''
            self.name = ''
            self.type = NO_TYPE
            self.power = NO_POWER
            self.image = ''
            self.sword = [NO_SWORD for i in range(4)]
            self.text = ''
        else:
            self.fighter = json_object['fighter']
            self.name = json_object['name']
            self.type = json_object['type']
            self.power = json_object['power']
            self.image = json_object['image']
            self.sword = [NO_SWORD for i in range(4)]
            self.sword_origin = json_object.get('sword_origin', NO_SWORD)
            self.sword_destiny = json_object.get('sword_destiny', NO_SWORD)
            self.text = json_object.get('text', None)

    def __copy__(self):
        other = Card()
        other.fighter = self.fighter
        other.name = self.name
        other.type = self.type
        other.power = self.power
        other.image = self.image
        other.sword = list(self.sword)
        other.text = self.text
        return other

    def __eq__(self, other):
        return (
            self.fighter == other.fighter and
            self.name == other.name and
            self.type == other.type and
            self.power == other.power and
            self.image == other.image and
            self.sword == other.sword and
            self.text == other.text
        )

    def is_equivalent(self, other):
        return (
            self.type == other.type and
            self.power == other.power and
            self.sword == other.sword and
            self.text == other.text
        )

    def __str__(self):
        normalize = lambda s, l: s + ' ' * (l - len(s)) if len(s) < l else s[0:l]
        types = {NO_TYPE: '', ATTACK: 'Attack', DEFENSE: 'Defense', SPECIAL: 'Special'}
        powers = lambda p: str(p) if p is not None else ' '
        text  = '.-------------.\n'
        text += '| ' + normalize(self.fighter, 11) + ' |\n'
        text += '| ' + normalize(self.name, 11) + ' |\n'
        text += '|-------------|\n'
        text += '| ' + normalize(types[self.type], 7) + ' (' + powers(self.power) + ') |\n'
        text += '|             |\n'
        if self.type == NO_TYPE:
            for i in range(3):
                text += '|             |\n'
        elif self.type in [ATTACK, DEFENSE]:
            swords = {SWORD_ORIGIN: 'o', SWORD_DESTINY: 'x', NO_SWORD: '·'}
            text += '|   %s     %s   |\n' % (swords[self.sword[S1]], swords[self.sword[S2]])
            text += '|             |\n'
            text += '|   %s     %s   |\n' % (swords[self.sword[S3]], swords[self.sword[S4]])
        elif self.type == SPECIAL:
            card_text = normalize(self.text, 33)
            text += '| %s |\n' % card_text[0:11]
            text += '| %s |\n' % card_text[11:22]
            text += '| %s |\n' % card_text[22:33]
        text += '|             |\n'
        text += '\'-------------\''
        return text

    def reverse_str(self):
        text  = '.-------------.\n'
        for i in range(9):
            text += '|             |\n'
        text += '\'-------------\''
        return text

    def to_json_object(self):
        json_object = {
            'fighter': self.fighter,
            'name': self.name,
            'type': self.type,
            'power': self.power,
            'image': self.image,
        }
        if self.type == 'special':
            json_object['text'] = self.text
        else:
            json_object['sword_origin'] = self.sword_origin
            json_object['sword_destiny'] = self.sword_destiny

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

    def is_legal(self):
        return (
            self.type in range(1, 4) and
            self.power in range(0 if self.type == SPECIAL else 1, 6) and
            (
                self.type == SPECIAL or
                self.sword.count(SWORD_ORIGIN) == 1 and
                self.sword.count(SWORD_DESTINY) == 1
            )
        )

    def leads_to(self, other):
        # assumes the cards are legal
        return (
            self.type in [ATTACK, DEFENSE] and
            other.type in [ATTACK, DEFENSE] and
            self.sword_destiny == other.sword_origin
        )
