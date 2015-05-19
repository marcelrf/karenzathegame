# coding: utf-8

import sys
import random
import collections
from card import *
from deck import *
from hand import *

ITERATIONS = 10
EXCLUDED_PER_ITERATION = 20
DECK_SAMPLES = 1000
CHOSEN_SAMPLES = 500

def generate():
    defenses = get_base_cards(DEFENSE, 6)
    attacks = get_base_cards(ATTACK, 6)
    generated_deck = Deck()
    generated_deck.cards = defenses + attacks
    combos = get_combos(generated_deck.cards)
    print generated_deck
    for combo in combos:
        print combo
    print len(combos)

def get_base_cards(card_type, size):
    base_cards = []
    trajectories = list(get_all_trajectories())
    while len(base_cards) < size:
        trajectory = random.choice(trajectories)
        base_card = Card()
        base_card.type = card_type
        base_card.sword_origin = trajectory[0]
        base_card.sword_destiny = trajectory[1]
        base_cards.append(base_card)
        trajectories.remove(trajectory)
    return base_cards

def get_all_trajectories():
    for sword_origin in [S1, S2, S3, S4]:
        for sword_destiny in [S1, S2, S3, S4]:
            if sword_origin != sword_destiny:
                yield [sword_origin, sword_destiny]

def get_combos(cards):
    combos = []
    for card1 in cards:
        for card2 in cards:
            if card1 != card2 and card1.leads_to(card2):
                combos.append(Hand([card1, card2]))
    return combos
