# coding: utf-8

import deck
import hand
import board
import copy
import random

class Player(object):

    def __init__(self, deck_json):
        self.deck = deck.Deck(deck_json)
        self.hand = hand.Hand()
        self.board = board.Board()
        self.score = 0

    def __copy__(self):
        other = Player()
        other.deck = copy.copy(self.deck)
        other.hand = copy.copy(self.hand)
        other.board = copy.copy(self.board)
        other.score = self.score
        return other

    def __eq__(self, other):
        return (
            self.deck == other.deck and
            self.hand == other.hand and
            self.board == other.board and
            self.score == other.score
        )

    def __str__(self):
        return str(self.hand) + "\n" + str(self.board)

    def draw_up_to(self, card_number):
        while self.hand.size() < card_number:
            self.hand.add(self.deck.draw())
