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
    print 'power', deck.get_power()
    print 'speed', deck.get_speed()
    print 'flow', deck.get_flow()
    print 'shadow', deck.get_shadow()

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

def get_combo_infos(combo):
	key, value = '', []
	for card in combo:
		if card.type == ATTACK: key += 'A'
		elif card.type == DEFENSE: key += 'D'
		value.append(card.power)
	return [key, value]

main()
