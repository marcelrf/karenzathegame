# coding: utf-8

from card import *
from copy import copy
import random
import json

class Deck(object):

    def __init__(self, json_text=None):
        if json_text is None:
            self.cards = []
        else:
            card_infos = json.loads(json_text)
            self.cards = map(lambda x: Card(json.dumps(x)), card_infos)

    def __copy__(self):
        other = Deck()
        other.cards = []
        for card in self.cards:
            other.cards.append(copy(card))
        return other

    def __eq__(self, other):
        for card in self.cards:
            if self.cards.count(card) != other.cards.count(card):
                return False
        for card in other.cards:
            if self.cards.count(card) != other.cards.count(card):
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
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def draw(self):
        chosen_card = random.choice(self.cards)
        self.cards.remove(chosen_card)
        return chosen_card

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

    def get_power(self):
        total = 0
        for card in self.cards:
            total += card.power
        return (float(total) / len(self.cards) - 1) / 9

    def get_speed(self):
        total, count = 0, 0
        for card_1 in self.cards:
            for card_2 in self.cards:
                if card_1.leads_to(card_2):
                    total += card_1.distance_to(card_2)
                    count += 1
        return 1 - float(total) / count / 2

    def get_flow(self):
        total, count = 0, 0
        for card_1 in self.cards:
            for card_2 in self.cards:
                if card_1 != card_2:
                    if card_1.leads_to(card_2):
                        total += 1
                    count += 1
        return float(total) / count * 2

    def get_shadow(self):
        sword_count = [[0, 0] for i in range(4)]
        for card in self.cards:
            if card.type == ATTACK:
                sword_count[card.sword_origin][0] += 1
            elif card.type == DEFENSE:
                sword_count[card.sword_origin][1] += 1
        sword_sum = sum(map(lambda x: abs(x[0] - x[1]), sword_count))
        return 1 - float(sword_sum) / len(self.cards)
