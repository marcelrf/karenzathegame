# coding: utf-8

import sys
import random
import collections
from card import *
from deck import *

ITERATIONS = 10
EXCLUDED_PER_ITERATION = 50
DECK_SAMPLES = 10000
CHOSEN_SAMPLES = 500

def generate(deck_size, card_heuristic, deck_heuristic):
    cards = get_all_cards(card_heuristic)
    for i in range(ITERATIONS):
        log_iteration(i, cards)
        decks = get_random_decks(cards, DECK_SAMPLES, deck_size / 2)
        sorted_decks = get_sorted_decks(decks, deck_heuristic)
        sorted_cards = get_sorted_cards(sorted_decks[:CHOSEN_SAMPLES])
        cards = exclude_worse_cards(sorted_cards, EXCLUDED_PER_ITERATION / 2)
    decks = get_random_decks(cards, DECK_SAMPLES, deck_size / 2)
    sorted_decks = get_sorted_decks(decks, deck_heuristic)
    return sorted_decks[0]

def get_all_cards(heuristic):
    all_cards = {ATTACK: [], DEFENSE: []}
    for card_type in [ATTACK, DEFENSE]:
        for left_foot in FEET_POSITIONS:
            for right_foot in FEET_POSITIONS:
                if left_foot != right_foot:
                    for sword_origin in SWORD_POSITIONS:
                        for sword_destiny in SWORD_POSITIONS:
                            if sword_origin != sword_destiny:
                                card = Card()
                                card.type = card_type
                                card.left_foot = left_foot
                                card.right_foot = right_foot
                                card.sword_origin = sword_origin
                                card.sword_destiny = sword_destiny
                                card.power = heuristic(card)
                                all_cards[card_type].append(card)
    return all_cards

def get_random_decks(cards, quantity, size):
    decks = []
    for i in range(quantity):
        deck = Deck()
        deck_attacks = random.sample(cards[ATTACK], size)
        deck_defenses = random.sample(cards[DEFENSE], size)
        for card in deck_attacks: deck.add(card)
        for card in deck_defenses: deck.add(card)
        decks.append(deck)
    return decks

def get_sorted_decks(decks, heuristic):
    decks_with_score = map(lambda x: [x, heuristic(x)], decks)
    decks_with_score.sort(key=lambda x: x[1], reverse=True)
    sorted_decks = map(lambda x: x[0], decks_with_score)
    return sorted_decks

def get_sorted_cards(decks):
    freqs = {
        ATTACK: collections.defaultdict(lambda: 0),
        DEFENSE: collections.defaultdict(lambda: 0)
    }
    for deck in decks:
        for card in deck.cards:
            freqs[card.type][card] += 1
    freqs[ATTACK] = list(freqs[ATTACK].iteritems())
    freqs[DEFENSE] = list(freqs[DEFENSE].iteritems())
    freqs[ATTACK].sort(key=lambda x: x[1], reverse=True)
    freqs[DEFENSE].sort(key=lambda x: x[1], reverse=True)
    return {
        ATTACK: map(lambda x: x[0], freqs[ATTACK]),
        DEFENSE: map(lambda x: x[0], freqs[DEFENSE])
    }

def exclude_worse_cards(cards, quantity):
    return {
        ATTACK: cards[ATTACK][:-quantity],
        DEFENSE: cards[DEFENSE][:-quantity],
    }

def log_iteration(i, cards):
    sys.stderr.write(
        "iteration %d: %d cards\n" %
        (i + 1, len(cards[ATTACK]) + len(cards[DEFENSE]))
    )
