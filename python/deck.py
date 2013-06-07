# coding: utf-8

from card import *
from copy import copy
import random

class Deck(object):

    def __init__(self):
        self.cards = []

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

    def combo_analysis(self):
        combos = []
        for i in range(100):
            hand = random.sample(self.cards, 6)
            combos.extend(self._get_combos(hand))
        if len(combos) > 0:
            print "combos per hand:", len(combos) / float(100)
            print "mean combo length:", sum(map(lambda x: len(x), combos)) / float(len(combos))
            print "mean combo card power:", sum(map(lambda x: sum(map(lambda y: y.power, x)), combos)) / float(sum(map(lambda x: len(x), combos)))
            combo_distance = 0
            for combo in combos:
                for i in range(len(combo) - 1):
                    combo_distance += combo[i].distance_to(combo[i + 1])
            print "mean combo card distance:", combo_distance / float(sum(map(lambda x: len(x) - 1, combos)))

        else:
            print "no combos found"

    def _get_combos(self, hand):
        if len(hand) == 1:
            return [hand]
        combos = []
        for card in hand:
            rest = list(hand)
            rest.remove(card)
            rest_combos = self._get_combos(rest)
            for combo in rest_combos:
                if card.distance_to(combo[0]) <= 2:
                    combos.append([card] + combo)
            combos.append([card])
        return combos
