# coding: utf-8

# long moves
# powerful moves
# aligned moves
# attached to position
# not very fast
# some combos in-place
# 1 or two reverse techniques

import sys
import ktg
from ktg.card import *
from ktg.deck import *
from ktg.generator import *

def card_heuristic(card):
	# must return int between 1 and 9 (both included)

	# feet level
	feet_level = card.feet_level()
	if card.type == ATTACK:
		feet_level = 2 - feet_level
	feet_level /= 2.0
	
	# trajectory length
	trajectory_length = card.trajectory_length()

	# alignment
	alignment = (2 - card.alignment()) / 2.0

	# total value
	value = ((
		5 * feet_level +
		1 * trajectory_length + 
		2 * alignment
	) / 8.0)
	
	# normalize total value
	return int(value * 8) + 1

def deck_heuristic(deck):
	# must return float between 0 and 1

	# power
	power = deck.mean_power() / 9.0

	# cohesion
	cohesion = 1 - deck.mean_distance() / 4.0

	# orientation
	reverse_count = 0
	for card in deck.cards:
		if card.feet_orientation() == REVERSE:
			reverse_count += 1
	orientation = 1 - reverse_count / float(len(deck.cards))

	# balance
	feet_balance = deck.feet_balance()
	sword_balance = deck.sword_balance()
	balance = feet_balance * sword_balance

	# total value
	return (
		pow(power, 6) *
		pow(balance, 4) *
		pow(cohesion, 2) *
		pow(orientation, 1)
	)

deck = generate(20, card_heuristic, deck_heuristic)
print deck.to_json()
