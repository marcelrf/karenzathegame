# coding: utf-8

import copy

class Hand(object):

    def __init__(self, cards=None):
        if cards is None: cards = []
        self.cards = cards

    def __copy__(self):
        other = Hand()
        for card in self.cards:
            card_copy = copy.copy(card)
            other.cards.append(card_copy)
        return other

    def __eq__(self, other):
        return self.cards == other.cards

    def __str__(self):
        lines = []
        if len(self.cards) > 0:
            card_texts = map(lambda x: (str(x) if x.is_legal() else x.reverse_str()).split("\n"), self.cards)
            while len(card_texts[0]) > 0:
                line = ""
                for i in range(len(card_texts)):
                    line += card_texts[i].pop(0)
                lines.append(line)
        return "\n".join(lines)

    def __len__(self):
        return len(self.cards)

    def card_at(self, index):
        if index > len(self.cards):
            raise Exception('Bad index')
        return self.cards[index - 1]

    def add(self, card):
        self.cards.append(card)

    def remove(self, index):
        if index > len(self.cards):
            raise Exception('Bad index')
        del self.cards[index - 1]

    def contains(self, card):
        return card in self.cards
