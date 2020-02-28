# coding: utf-8

from card import *
from copy import copy


class Hand(object):

    def __init__(self):
        self.cards = []

    def __copy__(self):
        other = Hand()
        other.cards = [copy(c) for c in self.cards]
        return other

    def __len__(self):
        return len(self.cards)

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def techniques(self):
        return [c for c in self.cards if c.card_type == CardType.TECHNIQUE]

    def abilities(self):
        return [c for c in self.cards if c.card_type == CardType.ABILITY]

    def attacks(self):
        return [
            c for c in self.techniques()
            if c.technique_type == TechniqueType.ATTACK
        ]

    def defenses(self):
        return [
            c for c in self.techniques()
            if c.technique_type == TechniqueType.DEFENSE
        ]

    def equipments(self):
        return [
            c for c in self.abilities()
            if c.ability_type == AbilityType.EQUIPMENT
        ]

    def replacements(self):
        return [
            c for c in self.abilities()
            if c.ability_type == AbilityType.REPLACEMENT
        ]

    def __str__(self):
        text = ""
        zipped_lines = zip(*[str(c).split('\n') for c in self.cards])
        for zipped_line in zipped_lines:
            text += ' '.join(zipped_line) + '\n'
        return text.strip()
