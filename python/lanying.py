# coding: utf-8

# not very powerful moves
# long and short moves
# aligned or not
# not so attached to position
# fast
# 1 or two reverse techniques

import sys
from card import *
from deck import *
from generator import *
from renderer import *

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
		2 * feet_level +
		2 * trajectory_length + 
		2 * alignment
	) / 6.0)
	
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
	orientation = 1 - reverse_count / 20.0

	# balance
	feet_balance = deck.feet_balance()
	sword_balance = deck.sword_balance()
	balance = (feet_balance + sword_balance) / 2.0

	# total value
	# return ((
	# 	4 * power +
	# 	2 * cohesion +
	# 	4 * balance +
	# 	1 * orientation
	# ) / 11.0)
	return (
		pow(power, 2) *
		pow(balance, 7) *
		pow(cohesion, 2) *
		pow(orientation, 1)
	)

deck = generate(20, card_heuristic, deck_heuristic)
deck.combo_analysis()

# print to_html(deck, 'lanying')
# sys.stderr.write("power: %f\n" % deck.mean_power())
# sys.stderr.write("distance: %f\n" % deck.mean_distance())
