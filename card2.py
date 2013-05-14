# coding: utf-8

import random
import collections

NO_FOOT, LEFT_FOOT, RIGHT_FOOT = range(3)
NO_SWORD, SWORD_ORG, SWORD_DST = range(3)
NO_TYPE, TYPE_ATTACK, TYPE_DEFENSE = range(3)

DESCENDANT, HORIZONTAL, ASCENDANT = range(3)
FRONT, FRONT_MID, MID, MID_BACK, BACK = range(5)
SHORT, LONG = range(2)
REGULAR, INVERSE = range(2)
ALIGNED, SEMI_ALIGNED, NOT_ALIGNED = range(3)

class Card(object):

    def __init__(self):
        self.feet = [NO_FOOT for i in range(5)]
        self.sword = [NO_SWORD for i in range(5)]
        self.type = NO_TYPE

    def __eq__(self, other):
        return (self.feet == other.feet and
                self.sword == other.sword and
                self.type == other.type)

    def __str__(self):
        foot_texts = ['·', 'L', 'R']
        sword_texts = [' ', 'O', 'X']
        card_type_texts = ['Unknown', 'Attack', 'Defense']
        direction_texts = ['Descendant', 'Horizontal', 'Ascendant']
        position_texts = ['Front', 'Front-Mid', 'Mid', 'Mid-Back', 'Back']
        orientation_texts = ['Regular', 'Inverse']
        length_texts = ['Short', 'Long']
        alignment_texts = ['Total', 'Partial', 'None']
        text = "===============\n"
        text += "Type: %s\n" % card_type_texts[self.type]
        text += "Power: %s\n" % self.power
        text += "---------------\n"
        text += "       %s\n" % foot_texts[self.feet[4]]
        text += "   %s       %s\n" % (
            sword_texts[self.sword[4]],
            sword_texts[self.sword[0]],
        )
        text += " %s           %s\n" % (
            foot_texts[self.feet[3]],
            foot_texts[self.feet[0]],
        )
        text += "\n"
        text += "  %s         %s\n" % (
            sword_texts[self.sword[3]],
            sword_texts[self.sword[1]],
        )
        text += "   %s   %s   %s\n" % (
            foot_texts[self.feet[2]],
            sword_texts[self.sword[2]],
            foot_texts[self.feet[1]],
        )
        text += "---------------\n"
        text += "Sword Dir: %s\n" % direction_texts[self.sword_direction]
        text += "Guard Pos: %s\n" % position_texts[self.guard_position]
        text += "Guard Ori: %s\n" % orientation_texts[self.guard_orientation]
        text += "T. Length: %s\n" % length_texts[self.trajectory_length]
        text += "Alignment: %s\n" % alignment_texts[self.sword_guard_alignment]
        text += "===============\n"
        return text

    def set_auto_values(self):
        self.sword_direction = self._sword_direction()
        self.guard_position = self._guard_position()
        self.trajectory_length = self._trajectory_length()
        self.guard_orientation = self._guard_orientation()
        self.sword_guard_alignment = self._sword_guard_alignment()
        self.power = self._power()

    def _power(self):
        total = 0
        if self.type == TYPE_ATTACK:
            total += 5 - self.guard_position
            total += 1 if self.guard_orientation == INVERSE else 0
        else:
            total += self.guard_position + 1
            total += 1 if self.guard_orientation == REGULAR else 0
        total += 3 - self.sword_direction
        if self.trajectory_length == LONG: total += 2
        total += 4 - self.sword_guard_alignment * 2
        return total / 15.0

    def _sword_direction(self):
        if SWORD_ORG in [self.sword[0], self.sword[4]]:
            if SWORD_DST in [self.sword[0], self.sword[4]]: return HORIZONTAL
            else: return DESCENDANT
        elif SWORD_ORG in [self.sword[1], self.sword[3]]:
            if SWORD_DST == self.sword[2]: return DESCENDANT
            elif SWORD_DST in [self.sword[0], self.sword[4]]: return ASCENDANT
            else: return HORIZONTAL
        else: return ASCENDANT

    def _guard_position(self):
        if self.feet[4] != NO_FOOT:
            if self.feet[0] + self.feet[3] != NO_FOOT: return FRONT
            else: return MID
        elif self.feet[0] + self.feet[3] != NO_FOOT:
            if self.feet[1] + self.feet[2] != NO_FOOT: return MID_BACK
            else: return FRONT_MID
        else: return BACK

    def _trajectory_length(self):
        if SWORD_ORG == self.sword[0]:
            if SWORD_DST in [self.sword[1], self.sword[4]]: return SHORT
            else: return LONG
        elif SWORD_ORG == self.sword[1]:
            if SWORD_DST in [self.sword[2], self.sword[0]]: return SHORT
            else: return LONG
        elif SWORD_ORG == self.sword[2]:
            if SWORD_DST in [self.sword[3], self.sword[1]]: return SHORT
            else: return LONG
        elif SWORD_ORG == self.sword[3]:
            if SWORD_DST in [self.sword[4], self.sword[2]]: return SHORT
            else: return LONG
        else:
            if SWORD_DST in [self.sword[0], self.sword[3]]: return SHORT
            else: return LONG

    def _guard_orientation(self):
        if LEFT_FOOT == self.feet[4]:
            if RIGHT_FOOT in [self.feet[0], self.feet[1]]: return REGULAR
            else: return INVERSE
        elif LEFT_FOOT == self.feet[2]:
            if RIGHT_FOOT != self.feet[3]: return REGULAR
            else: return INVERSE
        elif LEFT_FOOT == self.feet[1]:
            if RIGHT_FOOT == self.feet[0]: return REGULAR
            else: return INVERSE
        elif LEFT_FOOT == self.feet[0]: return INVERSE
        else: return REGULAR

    def _sword_guard_alignment(self):
        guard_alignment = self._guard_alignment()
        sword_alignment = self._sword_alignment()
        compatibility = abs(guard_alignment - sword_alignment)
        if compatibility == 0: return ALIGNED
        elif compatibility in [1, 4]: return SEMI_ALIGNED
        else: return NOT_ALIGNED

    def _sword_alignment(self):
        table = [
            [None, 4, 0, 1, 2],
            [4, None, 1, 2, 3],
            [0, 1, None, 3, 4],
            [1, 2, 3, None, 0],
            [2, 3, 4, 0, None],
        ]
        sword_org_index = self.sword.index(SWORD_ORG)
        sword_dst_index = self.sword.index(SWORD_DST)
        return table[sword_org_index][sword_dst_index]

    def _guard_alignment(self):
        table = [
            [None, 0, 1, 2, 3],
            [0, None, 2, 3, 4],
            [1, 2, None, 4, 0],
            [2, 3, 4, None, 1],
            [3, 4, 0, 1, None],
        ]
        left_foot_index = self.feet.index(LEFT_FOOT)
        right_foot_index = self.feet.index(RIGHT_FOOT)
        return table[left_foot_index][right_foot_index]

    def distance_to(self, card):
        distance = 0
        a, b = self, card
        a_left_foot = a.feet.index(LEFT_FOOT)
        a_right_foot = a.feet.index(RIGHT_FOOT)
        a_sword_dst = a.sword.index(SWORD_DST)
        b_left_foot = b.feet.index(LEFT_FOOT)
        b_right_foot = b.feet.index(RIGHT_FOOT)
        b_sword_org = b.sword.index(SWORD_ORG)
        if a_left_foot != b_left_foot: distance += 1
        if a_right_foot != b_right_foot: distance += 1
        if a_sword_dst != b_sword_org: distance += 1
        return distance / 3.0

def get_all_cards():
    all_cards = []
    for type in [TYPE_ATTACK, TYPE_DEFENSE]:
        for left_foot in range(5):
            for right_foot in range(5):
                if left_foot != right_foot:
                    for sword_org in range(5):
                        for sword_dst in range(5):
                            if sword_org != sword_dst:
                                c = Card()
                                c.type = type
                                c.feet[left_foot] = LEFT_FOOT
                                c.feet[right_foot] = RIGHT_FOOT
                                c.sword[sword_org] = SWORD_ORG
                                c.sword[sword_dst] = SWORD_DST
                                c.set_auto_values()
                                all_cards.append(c)
    return all_cards

def get_power_mean(cards):
    total = 0
    for card in cards:
        total += card.power
    return float(total) / len(cards)

def get_power_histogram(decks):
    freqs = collections.defaultdict(lambda: 0)
    for deck in decks:
        for card in deck[0]:
            freqs[card] += 1
    return list(freqs.iteritems())

def get_distance(deck):
    distance = 0
    for card1 in deck:
        for card2 in deck:
            distance += card1.distance_to(card2)
    return distance / 400.0

def get_proportion(deck):
    attacks = 0
    defenses = 0
    for card in deck:
        if card.type == TYPE_ATTACK: attacks += 1
        if card.type == TYPE_DEFENSE: defenses += 1
    return 1 - abs(attacks - defenses) / 20.0

def sort_by_heuristic(cards):
    decks = []
    for i in range(10000):
        deck = []
        for j in range(20):
            card_index = int(random.random() * len(cards))
            deck.append(cards[card_index])
        power = get_power_mean(deck)
        distance = get_distance(deck)
        proportion = get_proportion(deck)
        decks.append((deck, power * (1 - distance) * proportion))
    decks.sort(key=lambda x: x[1], reverse=True)
    hist = get_power_histogram(decks[:5000])
    hist.sort(key=lambda x: x[1], reverse=True)
    return map(lambda x: x[0], hist)

if __name__ == '__main__':
    all_cards = get_all_cards()
    cards1 = sort_by_heuristic(all_cards)
    print '.'
    cards2 = sort_by_heuristic(cards1[:700])
    print '.'
    cards3 = sort_by_heuristic(cards2[:600])
    print '.'
    cards4 = sort_by_heuristic(cards3[:500])
    print '.'
    cards5 = sort_by_heuristic(cards4[:400])
    print '.'
    cards6 = sort_by_heuristic(cards5[:300])
    print '.'
    cards7 = sort_by_heuristic(cards6[:200])
    print '.'
    cards8 = sort_by_heuristic(cards7[:100])
    print '.'
    cards9 = sort_by_heuristic(cards8[:50])
    print '.'
    cards10 = sort_by_heuristic(cards9[:20])

    print get_power_mean(cards10)
    print get_distance(cards10)
    print get_proportion(cards10)
    for card in cards10: print card
    
    # c = Card()
    # c.type = TYPE_ATTACK
    # c.feet[0] = RIGHT_FOOT
    # c.feet[3] = LEFT_FOOT
    # c.sword[1] = SWORD_ORG
    # c.sword[3] = SWORD_DST
    # c.set_auto_values()
    # print c

    # c2 = Card()
    # c2.type = TYPE_ATTACK
    # c2.feet[1] = RIGHT_FOOT
    # c2.feet[4] = LEFT_FOOT
    # c2.sword[1] = SWORD_ORG
    # c2.sword[3] = SWORD_DST
    # c2.set_auto_values()
    # print c2

    # print c.distance_to(c2)
