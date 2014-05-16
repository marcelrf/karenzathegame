# coding: utf-8

import sys
import random
import collections
from card import *
from deck import *
from copy import copy

ITERATIONS = 10000
CARD_AMOUNT = [1, 2, 2, 3, 3, 4]

def generate(power, speed, flow, shadow):
    deck = get_trajectory_deck(flow, shadow)
    set_power(deck, power)
    return deck

def get_trajectory_deck(flow, shadow):
    trajectories = get_all_trajectories()
    best_heuristic, best_deck = 1, None
    for it in range(ITERATIONS):
        deck = Deck()
        attacks = random.sample(trajectories, 6)
        for i in range(len(attacks)):
            attack = copy(attacks[i])
            attack.type = ATTACK
            for j in range(CARD_AMOUNT[i]):
                deck.add(attack)
        defenses = random.sample(trajectories, 5)
        for i in range(len(defenses)):
            defense = copy(defenses[i])
            defense.type = DEFENSE
            for j in range(CARD_AMOUNT[i]):
                deck.add(defense)
        deck_flow = deck.get_flow()
        deck_shadow = deck.get_shadow()
        heuristic = abs(deck_flow - flow) + abs(deck_shadow - shadow) / 2
        if heuristic < best_heuristic:
            best_heuristic = heuristic
            best_deck = deck
    return best_deck

def set_power(deck, power):
    remaining_power = int(power * 10 * len(deck.cards))
    remaining_cards = len(deck.cards)
    for card in set(deck.cards):
        count = deck.cards.count(card)
        factor = None
        if count == 1: factor = 2
        elif count == 2: factor = 1.5
        elif count == 3: factor = 1.2
        elif count == 4: factor = 1
        card_power = get_card_power(remaining_power, remaining_cards, factor)
        for deck_card in deck.cards:
            if deck_card == card:
                deck_card.power = card_power
        remaining_power -= card_power * count
        remaining_cards -= count

def get_card_power(remaining_power, remaining_cards, factor):
    randomized_factor = factor + random.uniform(-0.25 * factor, 0.25 * factor)
    return int(max(min(float(remaining_power) / remaining_cards * randomized_factor, 9), 1))

def get_all_trajectories():
    all_cards = []
    for sword_origin in SWORD_POSITIONS:
        for sword_destiny in SWORD_POSITIONS:
            if sword_origin != sword_destiny:
                card = Card()
                card.sword_origin = sword_origin
                card.sword_destiny = sword_destiny
                all_cards.append(card)
    return all_cards
