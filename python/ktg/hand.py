# coding: utf-8

import copy

class Hand(object):

    def __init__(self):
        self.cards = []

    def __copy__(self):
        other = Hand()
        for card in self.cards:
            card_copy = copy.copy(card)
            other.cards.append(card_copy)
        return other

    def __eq__(self, other):
        return self.cards == other.cards

    def __str__(self):
        text = ""
        if len(self.cards) > 0:
            card_texts = map(lambda x: str(x).split("\n"), self.cards)
            while len(card_texts[0]) > 0:
                for i in range(len(card_texts)):
                    text += card_texts[i].pop(0)
                text += '\n'
        return text

    def size(self):
        return len(self.cards)

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)
