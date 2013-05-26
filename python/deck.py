# coding: utf-8

from card import *
from copy import copy

class Deck(object):

    def __init__(self):
        self.name = ''
        self.cards = []

    def __copy__(self):
        other = Deck()
        other.name = self.name
        other.cards = []
        for card in self.cards:
            other.cards.append(copy(card))
        return other

    def __eq__(self, other):
        if self.name != other.name:
            return False
        for card in self.cards:
            if card not in other.cards:
                return False
        for card in other.cards:
            if card not in self.cards:
                return False
        return True

    def __str__(self):
        if self.name == '':
            name_text = 'No name'
        else: name_text = self.name
        text  = "===============\n"
        text += " " + name_text + "\n"
        for card in self.cards:
            text += str(card) + "\n"
        text += "==============="
        return text

    def add(self, card):
        if card not in self.cards:
            self.cards.append(card)

    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)

    def random(self, size):
        self.name = ''
        self.cards = []
        while len(self.cards) < size:
            card = Card()
            card.random()
            self.add(card)

    def is_legal(self):
        for card in self.cards:
            if not card.is_legal():
                return False
        return True

    def mean_power(self):
        total = 0
        for card in self.cards:
            total += card.power
        return float(total) / len(self.cards)

    def power_deviation(self):
        mean = self.mean_power()
        total = 0
        for card in self.cards:
            total += abs(card.power - mean)
        return float(total) / len(self.cards)

    def mean_distance(self):
        total = 0
        for card_1 in self.cards:
            for card_2 in self.cards:
                if card_1 != card_2:
                    total += card_1.distance_to(card_2)
        deck_size = len(self.cards)
        return float(total) / (deck_size * (deck_size - 1))

    def distance_deviation(self):
        mean = self.mean_distance()
        total = 0
        for card_1 in self.cards:
            for card_2 in self.cards:
                if card_1 != card_2:
                    total += abs(card_1.distance_to(card_2) - mean)
        deck_size = len(self.cards)
        return float(total) / (deck_size * (deck_size - 1))
