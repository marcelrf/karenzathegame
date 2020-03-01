# coding: utf-8

from ktg.hand import Hand
from copy import copy
from enum import Enum
import random


class PlayerState(Enum):
    INITIATIVE = 1
    THREATENED = 2


class Player(object):

    def __init__(self, deck):
        self.deck = deck
        self.discards = []
        self.hand = Hand()
        self.sequence = []
        self.last_move = None
        self.score = 0
        self.touche = False

    def __copy__(self):
        other = Player(copy(self.deck))
        other.discards = [copy(c) for c in self.discards]
        other.hand = copy(self.hand)
        other.sequence = [copy(c) for c in self.sequence]
        other.last_move = copy(self.last_move)
        other.score = self.score
        other.touche = self.touche
        return other

    def can_draw(self, cards=1):
        return len(self.deck) >= cards

    def draw(self, cards=1):
        for i in range(cards):
            card = self.deck.draw()
            self.hand.add(card)

    def should_discard(self):
        return len(self.hand) > 7

    def discard(self, card):
        self.hand.remove(card)
        self.discards.append(card)

    def can_reguard(self):
        return len(self.sequence) > 0

    def reguard(self):
        for move in self.sequence:
            self.discards.extend(move.cards)
        self.sequence = []

    def in_sequence(self):
        return len(self.sequence) > 0

    def sequence_head(self):
        if len(self.sequence) > 0:
            return self.sequence[-1]
        else: return None

    def play(self, move):
        for card in move.cards:
            self.hand.remove(card)
        self.sequence.append(move)

    def __str__(self):
        pass
