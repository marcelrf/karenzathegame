# coding: utf-8

from card import *
from deck import *
from generator import *

def card_heuristic(card):
	# must return int between 1 and 9 (both included)
	if card.type == ATTACK:
		value = 5 - card.feet_level()
	elif card.type == DEFENSE:
		value = card.feet_level() + 1
	if card.feet_orientation() == REVERSE:
		value *= 0.5
	return int(value / 5.0 * 8) + 1

def deck_heuristic(deck):
	# must return float between 0 and 1
	power = deck.mean_power() / 9.0
	distance = 1 - deck.mean_distance() / 4.0
	return power * distance

deck = generate(card_heuristic, deck_heuristic)
print_deck(deck)
