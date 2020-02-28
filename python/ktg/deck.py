# coding: utf-8

from copy import copy
import random


class Deck(object):

    def __init__(self, character, cards):
        self.character = character
        self.cards = cards

    def __copy__(self):
        return Deck(
            self.character,
            [copy(c) for c in self.cards]
        )

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        card_groups = [[]]
        for card in self.cards:
            card_groups[-1].append(card)
            if len(card_groups[-1]) == 10:
                card_groups.append([])
        text = ""
        for card_group in card_groups:
            zipped_lines = zip(*[str(c).split('\n') for c in card_group])
            for zipped_line in zipped_lines:
                text += ' '.join(zipped_line) + '\n'
        return text.strip()

    def draw(self):
        if len(self.cards) > 0:
            chosen = random.choice(self.cards)
            self.cards.remove(chosen)
            return chosen
        else: return None
