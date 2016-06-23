# coding: utf-8

from card import *
from hand import Hand
from copy import copy
from collections import defaultdict
import math

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
        text += 'ATTACKS\n'
        text += str(Hand(self.get_uniqe_cards(ATTACK))) + '\n'
        text += 'DEFENSES\n'
        text += str(Hand(self.get_uniqe_cards(DEFENSE))) + '\n'
        text += 'SPECIALS\n'
        text += str(Hand(self.get_uniqe_cards(SPECIAL))) + '\n'
        text += 'STATS\n'
        text += 'Power   - %.2f (A:%.2f D:%.2f)\n' % (
            self.power(None), self.power(ATTACK), self.power(DEFENSE)
        )
        text += 'Connect - %.2f (AA:%.2f AD:%.2f DD:%.2f DA:%.2f)\n' % (
            self.connectivity(None, None),
            self.connectivity(ATTACK, ATTACK),
            self.connectivity(ATTACK, DEFENSE),
            self.connectivity(DEFENSE, DEFENSE),
            self.connectivity(DEFENSE, ATTACK),
        )
        text += 'Predict - %.2f (1:%.2f 2:%.2f 3:%.2f 4:%.2f)\n' % (
            (self.predictability(S1) + self.predictability(S2) + self.predictability(S3) + self.predictability(S4)) / 4.0,
            self.predictability(S1),
            self.predictability(S2),
            self.predictability(S3),
            self.predictability(S4)
        )
        text += '==============='
        return text

    def __len__(self):
        return len(self.cards)

    def to_json_object(self):
        return [x.to_json_object() for x in self.cards]

    def get_uniqe_cards(self, card_type):
        unique_cards = []
        freqs = defaultdict(lambda: 0)
        for card in self.cards:
            if card.type == card_type:
                card_str = str(card)
                if card_str not in freqs:
                    unique_cards.append(card)
                freqs[card_str] += 1
        unique_cards.sort(key=lambda x: -freqs[str(x)])
        return unique_cards

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

    def is_legal(self):
        for card in self.cards:
            if not card.is_legal():
                return False
        return True

    def power(self, card_type):
        # assumes deck is legal
        type_mask = [card_type] if card_type is not None else [ATTACK, DEFENSE]
        power_cards = [card for card in self.cards if card.type in type_mask]
        total = sum([card.power for card in power_cards])
        return float(total) / len(power_cards)

    def connectivity(self, origin_type, target_type):
        # assumes deck is legal
        origin_mask = [origin_type] if origin_type is not None else [ATTACK, DEFENSE]
        target_mask = [target_type] if target_type is not None else [ATTACK, DEFENSE]
        origin_cards = [card for card in self.cards if card.type in origin_mask]
        target_cards = [card for card in self.cards if card.type in target_mask]
        total = 0
        for origin_card in origin_cards:
            for target_card in target_cards:
                if origin_card.leads_to(target_card):
                    total += 1
        return float(total) / len(origin_cards)

    def predictability(self, position):
        # assumes deck is legal
        attack_total = 0
        defense_total = 0
        for card in self.cards:
            if card.sword_origin == position:
                if card.type == ATTACK:
                    attack_total += 1
                elif card.type == DEFENSE:
                    defense_total += 1
        if attack_total + defense_total == 0:
            return 1
        return abs(
            float(attack_total - defense_total) /
            (attack_total + defense_total)
        )
