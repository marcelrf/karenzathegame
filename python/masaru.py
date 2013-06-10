# coding: utf-8

# long moves
# powerful moves
# aligned moves
# attached to position
# not very fast
# some combos in-place
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

# def combo_analysis(self):
#     import sys
#     combos = []
#     for i in range(100):
#         hand = random.sample(self.cards, 5)
#         combos.extend(self._get_combos(hand))
#     if len(combos) > 0:
#         sys.stderr.write("combos per hand: %f\n" % (len(combos) / float(100)))
#         sys.stderr.write("mean combo length: %f\n" % (sum(map(lambda x: len(x), combos)) / float(len(combos))))
#         sys.stderr.write("mean combo card power: %f\n" % (sum(map(lambda x: sum(map(lambda y: y.power, x)), combos)) / float(sum(map(lambda x: len(x), combos)))))
#         combo_distance = 0
#         for combo in combos:
#             for i in range(len(combo) - 1):
#                 combo_distance += combo[i].distance_to(combo[i + 1])
#         sys.stderr.write("mean combo card distance: %f\n" % (combo_distance / float(sum(map(lambda x: len(x) - 1, combos)))))
#     else:
#         print "no combos found"

# def _get_combos(self, hand):
#     if len(hand) == 1:
#         return [hand]
#     combos = []
#     for card in hand:
#         rest = list(hand)
#         rest.remove(card)
#         rest_combos = self._get_combos(rest)
#         for combo in rest_combos:
#             if card.distance_to(combo[0]) <= 2:
#                 combos.append([card] + combo)
#         combos.append([card])
#     return combos


deck = generate(20, card_heuristic, deck_heuristic)
print deck

# deck.combo_analysis()
# print to_html(deck, 'masaru')
# sys.stderr.write("power: %f\n" % deck.mean_power())
# sys.stderr.write("distance: %f\n" % deck.mean_distance())
