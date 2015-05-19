# coding: utf-8

import deck
import hand
import card
import board
import copy

class Player(object):

    def __init__(self, deck_json):
        self.deck = deck.Deck(deck_json)
        self.hand = hand.Hand([])
        self.board = board.Board()
        self.board.random()
        self.played = None
        self.score = 0

    def __copy__(self):
        other = Player()
        other.deck = copy.copy(self.deck)
        other.hand = copy.copy(self.hand)
        other.board = copy.copy(self.board)
        other.played = self.played
        other.score = self.score
        return other

    def __eq__(self, other):
        return (
            self.deck == other.deck and
            self.hand == other.hand and
            self.board == other.board and
            self.played == other.played and
            self.score == other.score
        )

    def __str__(self):
        if self.played is not None:
            played = str(self.played)
        else:
            played = card.Card().reverse_str()
        text  = played + '\n'
        text += str(self.board) + '\n'
        text += str(self.hand) + '\n'
        text += 'Cards in deck: ' + str(len(self.deck.cards)) + ', '
        text += 'Score: ' + str(self.score)
        return text

    def draw(self):
        if len(self.deck.cards) == 0:
            raise Exception('No more cards left')
        self.hand.add(self.deck.draw())

    def move(self, token, position):
        setattr(self.board, token, position)

    def play(self, index):
        if index > len(self.hand):
            raise Exception('Bad index')
        card = self.hand.card_at(index)
        if not self.board.leads_to(card):
            raise Exception('Card not playable')
        self.hand.remove(index)
        self.played = card
        self.board.move_sword_as_in(card)

    def discard(self, index):
        if index > len(self.hand):
            raise Exception('Bad index')
        self.hand.remove(index)
        self.played = None
