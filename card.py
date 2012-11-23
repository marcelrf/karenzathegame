# coding: utf-8

import copy

class Card(object):

	LEFT_FOOT, RIGHT_FOOT, NO_FOOT = range(3)
	SWORD_ORG, SWORD_DST, NO_SWORD = range(3)
	TYPE_ATTACK, TYPE_DEFENSE, NO_TYPE = range(3)

	# Sword power table (type, origin, destiny)
	SWORD_POWER = [
		[ # Attack
			[0, 5, 8, 7, 4],
			[2, 0, 5, 6, 5],
			[3, 2, 0, 3, 4],
			[4, 5, 4, 0, 1],
			[3, 6, 7, 6, 0],
		],
		[ # Defense
			[0, 1, 4, 5, 4],
			[6, 0, 3, 6, 7],
			[7, 4, 0, 5, 8],
			[6, 5, 2, 0, 5],
			[3, 4, 3, 2, 0],
		],
	]

	GUARD_POWER = [
		[ # Attack
			[0, 2, 3, 5, 7],
			[4, 0, 1, 4, 5],
			[5, 2, 0, 3, 6],
			[6, 4, 3, 0, 8],
			[7, 5, 4, 6, 0],
		],
		[ # Defense
			[0, 5, 4, 2, 2],
			[7, 0, 6, 5, 4],
			[6, 7, 0, 6, 5],
			[3, 5, 6, 0, 3],
			[2, 4, 3, 1, 0],
		],
	]

	def __init__(self):
		self.feet = [self.NO_FOOT for i in range(5)]
		self.sword = [self.NO_SWORD for i in range(5)]
		self.type = self.NO_TYPE

	def __str__(self):
		foot_texts = ['L', 'R', '·']
		sword_texts = ['O', 'X', ' ']
		card_type_texts = ['Attack', 'Defense', 'Unknown']
		text = "===============\n"
		text += "Type: %s\n" % card_type_texts[self.type]
		# text += "Sword power: %f\n" % self.sword_power()
		# text += "Guard power: %f\n" % self.guard_power()
		text += "Power: %d\n" % self.power()
		text += "---------------\n"
		text += "       %s\n" % foot_texts[self.feet[4]]
		text += "   %s       %s\n" % (
			sword_texts[self.sword[0]],
			sword_texts[self.sword[4]],
		)
		text += " %s           %s\n" % (
			foot_texts[self.feet[3]],
			foot_texts[self.feet[0]],
		)
		text += "\n"
		text += "  %s         %s\n" % (
			sword_texts[self.sword[1]],
			sword_texts[self.sword[3]],
		)
		text += "   %s   %s   %s\n" % (
			foot_texts[self.feet[2]],
			sword_texts[self.sword[2]],
			foot_texts[self.feet[1]],
		)
		text += "===============\n"
		return text

	def sword_power(self):
		assert(self.type != self.NO_TYPE)
		assert(self.sword.count(self.SWORD_ORG) == 1)
		assert(self.sword.count(self.SWORD_DST) > 0)
		power = 0
		origin = self.sword.index(self.SWORD_ORG)
		destiny_count = 0
		for destiny in range(5):
			if self.sword[destiny] == self.SWORD_DST:
				destiny_count += 1
				power += self.SWORD_POWER[self.type][origin][destiny]
		return power / 8.0 / destiny_count * (1 - (destiny_count - 1) * 0.25)

	def guard_power(self):
		assert(self.type != self.NO_TYPE)
		power = 0
		left_foot_count = self.feet.count(self.LEFT_FOOT)
		right_foot_count = self.feet.count(self.RIGHT_FOOT)
		for left_foot in range(5):
			if left_foot_count == 0 or self.feet[left_foot] == self.LEFT_FOOT:
				for right_foot in range(5):
					if (left_foot != right_foot and
						    (right_foot_count == 0 or
						    self.feet[right_foot] == self.RIGHT_FOOT)):
						power += self.GUARD_POWER[self.type][left_foot][right_foot]
		guards = None
		if left_foot_count == 0 and right_foot_count == 0: guards = 20
		elif left_foot_count == 0: guards = 4 * right_foot_count
		elif right_foot_count == 0: guards = 4 * left_foot_count
		else: guards = left_foot_count * right_foot_count
		return power / 8.0 / guards * (1 - pow((guards - 1) / 19, 0.6))

	def power(self):
		return min(round(1 + (0.5 * self.sword_power() + 0.5 * self.guard_power()) * 8.5), 9)

	def variations(self, variation_type, context, no_type, max_adjacents):
		for i in range(5):
			new_variation = copy.deepcopy(self)
			valid, adjacents = True, 0
			while valid and adjacents < max_adjacents:
				new_adjacent = (i + adjacents) % 5
				if getattr(self, context)[new_adjacent] == no_type:
					getattr(new_variation, context)[new_adjacent] = variation_type
					yield copy.deepcopy(new_variation)
					adjacents += 1
				else:
					valid = False

	def foot_variations(self, foot, max_adjacents):
		assert(foot not in self.feet)
		yield copy.deepcopy(self)
		for x in self.variations(foot, 'feet', self.NO_FOOT, max_adjacents):
			yield x

	def sword_variations(self):
		assert(self.SWORD_ORG not in self.sword)
		assert(self.SWORD_DST not in self.sword)
		for x in self.variations(self.SWORD_ORG, 'sword', self.NO_SWORD, 1):
			for y in x.variations(self.SWORD_DST, 'sword', self.NO_SWORD, 4):
				yield y

	def type_variations(self):
		assert(self.type == self.NO_TYPE)
		attack = copy.deepcopy(self)
		attack.type = self.TYPE_ATTACK
		yield attack
		defense = copy.deepcopy(self)
		defense.type = self.TYPE_DEFENSE
		yield defense

	def accepts_reversed_guard(self):
		return (
			self.LEFT_FOOT in [self.feet[0], self.feet[1]] or
			self.RIGHT_FOOT in [self.feet[2], self.feet[3]]
		)


def get_all_cards():
	c = Card()
	all_cards = []
	for i in c.foot_variations(Card.LEFT_FOOT, 4):
		max_adjacents = 4 - i.feet.count(Card.LEFT_FOOT)
		for j in i.foot_variations(Card.RIGHT_FOOT, max_adjacents):
			for k in j.sword_variations():
				for l in k.type_variations():
					all_cards.append(l)
	return all_cards

if __name__ == '__main__':
	all_cards = get_all_cards()
	# all_cards = filter(lambda x: x.power() > 7, all_cards)
	# all_cards = filter(lambda x: x.feet.count(Card.LEFT_FOOT) == x.feet.count(Card.RIGHT_FOOT) == 1, all_cards)
	all_cards = filter(lambda x: not x.accepts_reversed_guard(), all_cards)
	all_cards.sort(key=lambda x: 10 - x.power())
	for card in all_cards: print card
	print "Number of cards: %d" % len(all_cards)
	print "Number of attacks: %d" % len(filter(lambda x: x.type == Card.TYPE_ATTACK, all_cards))
	print "Number of defenses: %d" % len(filter(lambda x: x.type == Card.TYPE_DEFENSE, all_cards))
