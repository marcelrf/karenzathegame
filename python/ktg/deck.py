# coding: utf-8

from card import *
from copy import copy
import random

class Deck(object):

    def __init__(self, json_object=None):
        if json_object is None:
            self.cards = []
        else:
            self.cards = [Card(x) for x in json_object]

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
        text  = '===============\n'
        for card in self.cards:
            text += str(card) + '\n'
        text += '==============='
        return text

    def __len__(self):
        return len(self.cards)

    def to_json_object(self):
        return [x.to_json_object() for x in self.cards]

    def add(self, card):
        self.cards.append(card)

    def remove(self, card):
        self.cards.remove(card)

    def remove_all(self, card):
        self.cards = [x for x in self.cards if x != card]

    def draw(self):
        chosen_card = random.choice(self.cards)
        self.cards.remove(chosen_card)
        return chosen_card

    def random(self, size):
        type_size = int(size / 2)
        self.cards = []
        for card_type in [ATTACK, DEFENSE]:
            for _ in range(type_size):
                card = Card()
                card.random()
                card.type = card_type
                self.add(card)

    def is_legal(self):
        for card in self.cards:
            if not card.is_legal():
                return False
        return True

    def power(self, card_type):
        # assumes deck is legal
        total = 0
        power_cards = [
            card for card in self.cards
            if card_type is None or card.type == card_type
        ]
        for card in power_cards:
            total += card.power
        return float(total) / len(power_cards)

    def connectivity(self, origin_type, target_type):
        # assumes deck is legal
        total = 0
        origin_cards = [
            card for card in self.cards
            if origin_type is None or card.type == origin_type
        ]
        target_cards = [
            card for card in self.cards
            if target_type is None or card.type == target_type
        ]
        for origin_card in origin_cards:
            origin_in_targets = origin_card in target_cards
            if origin_in_targets:
                target_cards.remove(origin_card)
            for target_card in target_cards:
                if origin_card.leads_to(target_card):
                    total += 1
            if origin_in_targets:
                target_cards.append(origin_card)
        return float(total) / len(origin_cards)

    def predictability(self, position):
        # assumes deck is legal
        attack_total = 0
        defense_total = 0
        power_total = 0
        for card in self.cards:
            if card.sword_origin == position:
                if card.type == ATTACK:
                    attack_total += 1
                elif card.type == DEFENSE:
                    defense_total += 1
                power_total += card.power
        return (attack_total, defense_total, power_total)
