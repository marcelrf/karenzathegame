# coding: utf-8

import sys
import ktg
from ktg.card import *
from ktg.deck import *
from ktg.generator import *
import random

def card_heuristic(card):
	# must return int between 1 and 9 (both included)

	# feet level
	feet_level = card.feet_level()
	if card.type == ATTACK:
		feet_level = 2 - feet_level
	feet_level /= 2.0
	
	# trajectory length
	trajectory_length = card.trajectory_length()

	# trajectory direction
	trajectory_direction = (2 - card.trajectory_direction()) / 2.0

	# alignment
	alignment = (2 - card.alignment()) / 2.0

	# guard side (left)
	guard_side = (2 - card.guard_side()) / 2.0

	# total value
	factors = [random.randint(1, 8) for i in range(5)]
	value = ((
		factors[0] * feet_level +
		factors[1] * trajectory_length +
		factors[2] * trajectory_direction + 
		factors[3] * guard_side +
		factors[4] * alignment
	) / float(sum(factors)))
	
	# normalize total value
	return int(value * 8) + 1

def deck_heuristic(deck):
	# must return float between 0 and 1

	# power
	power = deck.mean_power() / 9.0
	power_deviation = deck.power_deviation() / 4.5

	# cohesion
	cohesion = 1 - deck.mean_distance() / 4.0
	cohesion_deviation = 1 - deck.distance_deviation() / 2.0

	# orientation
	reverse_count = 0
	for card in deck.cards:
		if card.feet_orientation() == REVERSE:
			reverse_count += 1
	orientation = 1 - reverse_count / float(len(deck.cards))

	# feet balance
	feet_balance = deck.feet_balance()
	
	# sword balance
	sword_balance = deck.sword_balance()

	# total value
	factors = [random.randint(1, 9) for i in range(7)]
	return (
		pow(power, factors[0]) *
		pow(power_deviation, factors[1]) *
		pow(feet_balance, factors[2]) *
		pow(sword_balance, factors[3]) *
		pow(cohesion, factors[4]) *
		pow(cohesion_deviation, factors[5]) *
		pow(orientation, factors[6])
	)

deck = generate(20, card_heuristic, deck_heuristic)
print deck.to_json()
