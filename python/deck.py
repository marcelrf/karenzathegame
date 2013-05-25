# coding: UTF-8

from card import *

MIN_DECK_SIZE = 20
DEFAULT_DECK_SIZE = 40
MAX_DECK_SIZE = 60

class Deck(object):

    def __init__(self):
        self.name = ''
        self.cards = set([])

    def __str__(self):
        if self.name == '':
            name_text = 'No name'
        else: name_text = self.name
        text  = "===============\n"
        text += " " + name_text + "\n"
        text += "===============\n"
        for card in self.cards:
            text += str(card) + "\n"
        text += "==============="
        return text

    def random(self, size=DEFAULT_DECK_SIZE):
        self.name = ''
        self.cards = set([])
        while len(self.cards) < size:
            card = Card()
            card.random()
            self.cards.add(card)

    def is_legal(self):
        if (len(self.cards) < MIN_DECK_SIZE or
            len(self.cards) > MAX_DECK_SIZE):
            return False
        for card in self.cards:
            if not card.is_legal():
                return False
        return True
