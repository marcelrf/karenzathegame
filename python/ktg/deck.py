# coding: utf-8

from card import *
from hand import Hand
from copy import copy
from collections import defaultdict
import random
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
        attacks = Hand(self.get_uniqe_cards(ATTACK))
        defenses = Hand(self.get_uniqe_cards(DEFENSE))
        text  = '===============\n'
        text += 'ATTACKS\n'
        text += str(attacks) + '\n'
        text += 'DEFENSES\n'
        text += str(defenses) + '\n'
        text += 'STATS\n'
        text += 'Power   - %.2f (A:%.2f D:%.2f)\n' % (self.power(None), self.power(ATTACK), self.power(DEFENSE))
        text += 'Connect - %.2f (AA:%.2f AD:%.2f DD:%.2f DA:%.2f)\n' % ((self.connectivity(DEFENSE, DEFENSE) + self.connectivity(DEFENSE, ATTACK) + self.connectivity(ATTACK, ATTACK) + self.connectivity(ATTACK, DEFENSE)) / 4.0, self.connectivity(ATTACK, ATTACK), self.connectivity(ATTACK, DEFENSE), self.connectivity(DEFENSE, DEFENSE), self.connectivity(DEFENSE, ATTACK))
        text += 'Predict - %.2f (1:%.2f 2:%.2f 3:%.2f 4:%.2f)\n' % ((self.predictability(S1) + self.predictability(S2) + self.predictability(S3) + self.predictability(S4)) / 4.0, self.predictability(S1), self.predictability(S2), self.predictability(S3), self.predictability(S4))
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

    def random(self):
        self.cards = []
        for card_type in [ATTACK, DEFENSE]:
            trajectories = get_all_trajectories()
            for freq in [4, 3, 3, 2, 2, 1]:
                trajectory = random.choice(trajectories)
                trajectories.remove(trajectory)
                base_card = Card()
                base_card.sword_origin = trajectory[0]
                base_card.sword_destiny = trajectory[1]
                base_card.type = card_type
                base_card.power = sorted([random.randint(1, 9) for _ in range(4)])[-freq]
                for _ in range(freq):
                    card = copy(base_card)
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
            for target_card in target_cards:
                if origin_card.leads_to(target_card):
                    total += 1
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
        attack_pred = math.pow(attack_total - 3.75, 2)
        defense_pred = math.pow(defense_total - 3.75, 2)
        return (attack_pred + defense_total) / 2


def get_all_trajectories():
    all_trajectories = []
    for sword_origin in [S1, S2, S3, S4]:
        for sword_destiny in [S1, S2, S3, S4]:
            if sword_origin != sword_destiny:
                all_trajectories.append((sword_origin, sword_destiny))
    return all_trajectories
