# coding: utf-8

import random
import collections
from card import *
from deck import *

def main():
    all_cards = get_all_cards()
    

def get_all_cards():
    all_cards = {TYPE_ATTACK: [], TYPE_DEFENSE: []}
    for type in [TYPE_ATTACK, TYPE_DEFENSE]:
        for left_foot in range(5):
            for right_foot in range(5):
                if left_foot != right_foot:
                    for sword_org in range(5):
                        for sword_dst in range(5):
                            if sword_org != sword_dst:
                                c = Card()
                                c.type = type
                                c.feet[left_foot] = LEFT_FOOT
                                c.feet[right_foot] = RIGHT_FOOT
                                c.sword[sword_org] = SWORD_ORG
                                c.sword[sword_dst] = SWORD_DST
                                c.set_auto_values()
                                all_cards[type].append(c)
    return all_cards

def get_power_mean(deck):
    total = 0
    for card in deck:
        total += card.power
    return float(total) / len(deck)

def get_cohesion(deck):
    feet_count = [0, 0, 0, 0, 0]
    for card in deck:
        for i in range(5):
            if card.feet[i] == RIGHT_FOOT:
                feet_count[i] += 1
            elif card.feet[i] == LEFT_FOOT:
                feet_count[i] -= 1
    feet_count = map(lambda x: x*x, feet_count)
    feet_cohesion = sum(feet_count) / 800.0
    sword_count = [0, 0, 0, 0, 0]
    for card in deck:
        for i in range(5):
            if card.sword[i] == SWORD_ORG:
                sword_count[i] += 1
            elif card.sword[i] == SWORD_DST:
                sword_count[i] -= 1
    sword_count = map(lambda x: abs(x), sword_count)
    sword_cohesion = 1 - sum(sword_count) / 80.0
    return feet_cohesion * sword_cohesion
    # distance = 0
    # for card1 in deck:
    #     for card2 in deck:
    #         distance += card1.distance_to(card2)
    # return 1 - (distance / 400.0)

def get_inverse_cohesion(deck):
    inverted_count = 0
    for card in deck:
        if card.guard_orientation == INVERSE:
            inverted_count += 1
    inverted_cohesion = pow(1 - inverted_count / 20.0, 5)
    return inverted_cohesion

def get_deck_factor(deck):
    global MAX_DECK_POWER, MAX_DECK_COHESION, MAX_DECK_FACTOR
    power = get_power_mean(deck)
    cohesion = get_cohesion(deck)
    inverse = get_inverse_cohesion(deck)
    factor = power * cohesion * inverse
    if power > MAX_DECK_POWER: MAX_DECK_POWER = power
    if cohesion > MAX_DECK_COHESION: MAX_DECK_COHESION = cohesion
    if factor > MAX_DECK_FACTOR: MAX_DECK_FACTOR = factor
    return factor

def get_power_histogram(decks):
    freqs = {
        TYPE_ATTACK: collections.defaultdict(lambda: 0),
        TYPE_DEFENSE: collections.defaultdict(lambda: 0)
    }
    for deck in decks:
        for card in deck[0]:
            freqs[card.type][card] += 1
    freqs[TYPE_ATTACK] = list(freqs[TYPE_ATTACK].iteritems())
    freqs[TYPE_DEFENSE] = list(freqs[TYPE_DEFENSE].iteritems())
    freqs[TYPE_ATTACK].sort(key=lambda x: x[1], reverse=True)
    freqs[TYPE_DEFENSE].sort(key=lambda x: x[1], reverse=True)
    return {
        TYPE_ATTACK: map(lambda x: x[0], freqs[TYPE_ATTACK]),
        TYPE_DEFENSE: map(lambda x: x[0], freqs[TYPE_DEFENSE])
    }

def sort_by_heuristic(cards, make_histogram=True):
    decks = []
    for i in range(100000):
        deck = []
        selected_attacks, selected_defenses = [None], [None]
        attack_index, defense_index = None, None
        for j in range(10):
            while attack_index in selected_attacks:
                attack_index = int(random.random() * len(cards[TYPE_ATTACK]))
            selected_attacks.append(attack_index)
            deck.append(cards[TYPE_ATTACK][attack_index])
            while defense_index in selected_defenses:
                defense_index = int(random.random() * len(cards[TYPE_DEFENSE]))
            selected_defenses.append(defense_index)
            deck.append(cards[TYPE_DEFENSE][defense_index])
        factor = get_deck_factor(deck)
        decks.append((deck, factor))
    decks.sort(key=lambda x: x[1], reverse=True)
    if make_histogram:
        hist = get_power_histogram(decks[:50000])
        return hist
    else: return decks

def crop_card_set(cards, threshold):
    return {
        TYPE_ATTACK: cards[TYPE_ATTACK][:threshold],
        TYPE_DEFENSE: cards[TYPE_DEFENSE][:threshold]
    }

if __name__ == '__main__':
    all_cards = get_all_cards()
    cards1 = sort_by_heuristic(all_cards)
    cards2 = sort_by_heuristic(crop_card_set(cards1, 350))
    cards3 = sort_by_heuristic(crop_card_set(cards2, 300))
    cards4 = sort_by_heuristic(crop_card_set(cards3, 250))
    cards5 = sort_by_heuristic(crop_card_set(cards4, 200))
    cards6 = sort_by_heuristic(crop_card_set(cards5, 150))
    deck = sort_by_heuristic(crop_card_set(cards6, 100), False)[0][0]

    print get_power_mean(deck), MAX_DECK_POWER
    print get_cohesion(deck), MAX_DECK_COHESION
    print get_power_mean(deck) * get_cohesion(deck), MAX_DECK_FACTOR
    for card in deck: print card
    
    # c = Card()
    # c.type = TYPE_ATTACK
    # c.feet[0] = RIGHT_FOOT
    # c.feet[3] = LEFT_FOOT
    # c.sword[1] = SWORD_ORG
    # c.sword[3] = SWORD_DST
    # c.set_auto_values()
    # print c

    # c2 = Card()
    # c2.type = TYPE_ATTACK
    # c2.feet[1] = RIGHT_FOOT
    # c2.feet[4] = LEFT_FOOT
    # c2.sword[1] = SWORD_ORG
    # c2.sword[3] = SWORD_DST
    # c2.set_auto_values()
    # print c2

    # print c.distance_to(c2)
