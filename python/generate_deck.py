# coding: utf-8

import json
import math
from ktg.deck import Deck
from ktg.card import ATTACK, DEFENSE, S1, S2, S3, S4

print 'Welcome!'

desired_attack_power = float(raw_input('Desired attack power: '))
desired_defense_power = float(raw_input('Desired defense power: '))

desired_aa_connect = float(raw_input('Desired aa connect: '))
desired_ad_connect = float(raw_input('Desired ad connect: '))
desired_da_connect = float(raw_input('Desired da connect: '))
desired_dd_connect = float(raw_input('Desired dd connect: '))

desired_predict = float(raw_input('Desired predict: '))
print 'Generating...'

ITERATIONS = 10000


while True:
	min_delta, best_deck = None, None
	for _ in range(ITERATIONS):
		deck = Deck()
		deck.random()

		# power
		actual_attack_power = deck.power(ATTACK)
		actual_defense_power = deck.power(DEFENSE)
		attack_delta = math.pow(actual_attack_power - desired_attack_power, 2)
		defense_delta = math.pow(actual_defense_power - desired_defense_power, 2)
		power_delta = (attack_delta + defense_delta) / 2.

		# connect
		actual_aa_connect = deck.connectivity(ATTACK, ATTACK)
		actual_ad_connect = deck.connectivity(ATTACK, DEFENSE)
		actual_da_connect = deck.connectivity(DEFENSE, ATTACK)
		actual_dd_connect = deck.connectivity(DEFENSE, DEFENSE)
		aa_delta = math.pow(actual_aa_connect - desired_aa_connect, 2)
		ad_delta = math.pow(actual_ad_connect - desired_ad_connect, 2)
		da_delta = math.pow(actual_da_connect - desired_da_connect, 2)
		dd_delta = math.pow(actual_dd_connect - desired_dd_connect, 2)
		connect_delta = (aa_delta + ad_delta + da_delta + dd_delta) / 4.

		# predict
		actual_predict = (deck.predictability(S1) + deck.predictability(S2) + deck.predictability(S3) + deck.predictability(S4)) / 4.0
		predict_delta = abs(desired_predict - actual_predict)

		# total
		delta = (power_delta + connect_delta + predict_delta) / 3.

		if min_delta is None or delta < min_delta:
			best_deck = deck
			min_delta = delta

	print best_deck

	option = None
	while option not in ['n', 's']:
		option = raw_input('Next or Save? [n,s]: ')
	if option == 'n':
		continue
	elif option == 's':
		filename = raw_input('Filename: ')
		with open(filename, 'w') as output_file:
			output_file.write(json.dumps(best_deck.to_json_object()))
		break

print 'Bye!'
