# coding: utf-8

import sys
import random
import collections
from card import *
from deck import *
from copy import copy

ITERATIONS = 10000
CARD_AMOUNT = [1, 2, 2, 3, 3, 4]
SWORD_POSITIONS = [S1, S2, S3, S4]

def generate(power, speed, flow, shadow):
    deck = get_trajectory_deck(flow, shadow)
    set_power(deck, power)
    deck = set_feet(deck, speed)
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
        defenses = random.sample(trajectories, 6)
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

def set_feet(deck, speed):
    guards = get_all_guards()
    best_heuristic, best_deck = 1, None
    for it in range(ITERATIONS):
        deck_copy = copy(deck)
        for ref_card in set(deck.cards):
            guard = None
            while guard is None or not guard_is_compatible(guard, deck_copy.cards):
                guard = random.choice(guards)
            for card in deck_copy.cards:
                if card == ref_card:
                    if guard.left_foot is not None: card.left_foot = guard.left_foot
                    if guard.right_foot is not None: card.right_foot = guard.right_foot
        deck_speed = deck_copy.get_speed()
        heuristic = abs(deck_speed - speed)
        if heuristic < best_heuristic:
            best_heuristic = heuristic
            best_deck = deck_copy
    return best_deck

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

def get_all_guards():
    all_cards = []
    for left_foot in [FA, FB, FD, None]:
        for right_foot in [FA, FC, FD, None]:
            if left_foot != right_foot or left_foot is None:
                card = Card()
                card.left_foot = left_foot
                card.right_foot = right_foot
                all_cards.append(card)
    return all_cards

def guard_is_compatible(guard, cards):
    for card in cards:
        if guard.left_foot == card.right_foot and guard.right_foot == card.left_foot:
            return False
    return True
