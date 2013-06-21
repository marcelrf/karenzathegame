# coding: utf-8

import deck
import hand
import board
import copy
import random

class Player(object):

    def __init__(self):
        self.deck = None
        self.hand = None
        self.board = None
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
        text  = str(self.hand)
        text += str(self.board) + "\n"
        text += 'Cards in deck: ' + str(len(self.deck.cards)) + ', '
        text += 'Score: ' + str(self.score)
        return text

    def setup(self, deck_json, card_number):
        self.deck = deck.Deck(deck_json)
        self.hand = hand.Hand()
        self.board = board.Board()
        self.board.random()
        self.score = 0
        self.draw_up_to(card_number)

    def draw_up_to(self, card_number):
        while self.hand.size() < card_number:
            if len(self.deck.cards) == 0:
                raise Exception('No more cards left')
            self.hand.add(self.deck.draw())
