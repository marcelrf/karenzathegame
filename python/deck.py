# coding: utf-8

from card import *
from copy import copy
import random

class Deck(object):

    def __init__(self, json_text=None):
        if json_text is None:
            self.cards = []
        else:
            card_jsons = json_text[2:-2].split('}, {')
            self.cards = map(lambda x: Card('{' + x + '}'), card_jsons)

    def __copy__(self):
        other = Deck()
        other.cards = []
        for card in self.cards:
            other.cards.append(copy(card))
        return other

    def __eq__(self, other):
        for card in self.cards:
            if card not in other.cards:
                return False
        for card in other.cards:
            if card not in self.cards:
                return False
        return True

    def __str__(self):
        text  = "===============\n"
        for card in self.cards:
            text += str(card) + "\n"
        text += "==============="
        return text

    def to_json(self):
        card_jsons = map(lambda x: x.to_json(), self.cards)
        return "[%s]" % ', '.join(card_jsons)

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

    def feet_balance(self):
        feet_count = [[0, 0] for i in range(5)]
        for card in self.cards:
            feet_count[card.left_foot][0] += 1
            feet_count[card.right_foot][1] += 1
        feet_sum = sum(map(lambda x: pow(x[0] - x[1], 2), feet_count))
        return feet_sum / (2.0 * pow(len(self.cards), 2))

    def sword_balance(self):
        sword_count = [[0, 0] for i in range(5)]
        for card in self.cards:
            sword_count[card.sword_origin][0] += 1
            sword_count[card.sword_destiny][0] += 1
        sword_sum = sum(map(lambda x: pow(x[0] - x[1], 2), sword_count))
        return 1 - sword_sum / (2.0 * pow(len(self.cards), 2))
