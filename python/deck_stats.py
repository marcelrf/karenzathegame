# coding: utf-8

import ktg
from ktg.card import *
from ktg.hand import *
from ktg.deck import *
import sys
import collections
import copy

def main():
    deck_filename = sys.argv[1]
    deck_file = open(deck_filename, 'r')
    deck_json = deck_file.read()[:-1]
    deck = Deck(deck_json)
    print "power", get_deck_power(deck)
    print "cohesion", get_deck_cohesion(deck)
    combos = collections.defaultdict(list)
    get_combos([], deck.cards, combos)
    combos = combos.items()
    combos.sort(key=lambda x: len(x[0]))
    combo_count = 0
    print "combos"
    for combo in combos:
    	accum = zip(*combo[1])
    	combo_count += len(combo[1])
    	print combo[0], len(combo[1]), map(lambda x: sum(x)/float(len(x)), accum)
    print "total", combo_count

def get_combos(current, cards, combos):
    for card in list(cards):
    	if len(current) == 0 or follows(current[-1], card) and len(current) < 5:
    		cards.remove(card)
    		current.append(card)
    		key, value = get_combo_infos(current)
    		combos[key].append(value)
    		get_combos(current, cards, combos)
    		current.pop()
    		cards.append(card)

def follows(card1, card2):
	return (
		card1.sword_destiny == card2.sword_origin and
		(
			card1.left_foot == card2.left_foot or
			card1.right_foot == card2.right_foot
		)
	)

def get_combo_infos(combo):
	key, value = "", []
	for card in combo:
		if card.type == ATTACK: key += "A"
		elif card.type == DEFENSE: key += "D"
		value.append(card.power)
	return [key, value]

def get_deck_power(deck):
	power = 0
	for card in deck.cards:
		power += card.power
	return power / float(len(deck.cards))

def get_deck_cohesion(deck):
	following = 0
	for card1 in deck.cards:
		other_cards = copy.copy(deck)
		other_cards.remove(card1)
		for card2 in other_cards.cards:
			if follows(card1, card2):
				following += 1
	return following / float(len(deck.cards) - 1)

main()
