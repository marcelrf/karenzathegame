# coding: utf-8

from ktg.hand import Hand
from ktg.card import Card
from copy import copy
from enum import Enum
from collections import defaultdict
import random


class PlayerState(Enum):
    INITIATIVE = 1
    THREATENED = 2


class Player(object):

    def __init__(self, deck):
        self.deck = deck
        self.discards = []
        self.hand = Hand()
        self.sequence = []
        self.score = 0
        self.touche = False
        self.played_cards = defaultdict(lambda: 0)
        self.discarded_cards = defaultdict(lambda: 0)

    def __copy__(self):
        other = Player(copy(self.deck))
        other.discards = [copy(c) for c in self.discards]
        other.hand = copy(self.hand)
        other.sequence = [copy(c) for c in self.sequence]
        other.score = self.score
        other.touche = self.touche
        other.played_cards = copy(self.played_cards)
        other.discarded_cards = copy(self.discarded_cards)
        return other

    def can_draw(self, cards=1):
        return len(self.deck) >= cards

    def draw(self, cards=1):
        for i in range(cards):
            if self.can_draw():
                card = self.deck.draw()
                self.hand.add(card)
            else:
                break

    def should_discard(self):
        return len(self.hand) > 7

    def discard(self, card):
        self.hand.remove(card)
        self.discards.append(card)
        self.discarded_cards[card.name] += 1

    def discard_at(self, index):
        card = self.hand.cards[index]
        self.discards.append(card)
        del self.hand.cards[index]
        self.discarded_cards[card.name] += 1

    def discard_random(self, number):
        for i in range(number):
            chosen_card = self.hand.cards[random.randint(0, len(self.hand.cards) - 1)]
            self.hand.remove(chosen_card)
            self.discards.append(chosen_card)

    def can_reguard(self):
        return len(self.sequence) > 0

    def reguard(self):
        for move in self.sequence:
            self.discards.extend(move.cards())
        self.sequence = []

    def in_sequence(self):
        return len(self.sequence) > 0

    def sequence_head(self):
        if len(self.sequence) > 0:
            return self.sequence[-1]
        else: return None

    def play(self, move):
        for card in move.cards():
            self.hand.remove(card)
            self.played_cards[card.name] += 1
        self.sequence.append(move)

    def play_instant(self, move):
        for card in move.cards():
            self.hand.remove(card)
            self.discards.append(card)
            self.played_cards[card.name] += 1

    def main_info_str(self, state):
        normalize = lambda s, l: s + ' ' * (l - len(s)) if len(s) < l else s[0:l]
        text  = '.-------------.\n'
        text += '|             |\n'
        text += '|             |\n'
        text += '| %s |\n' % normalize(self.deck.character, 11)
        text += '| ----------- |\n'
        text += '| Score: %s   |\n' % normalize(str(self.score), 2)
        text += '| State: %s   |\n' % ('--' if state is None else ('IN' if state == PlayerState.INITIATIVE else 'TH'))
        text += '|             |\n'
        text += '|             |\n'
        text += '\'-------------\''
        return text

    def block_str(self, state):
        components = [
            self.main_info_str(state),
            '\n'.join(['    '] * 11),
            str(self.hand),
            '\n'.join(['     '] * 11),
            Card.reverse_str(str(len(self.deck))),
            '\n'.join([' '] * 11),
            Card.reverse_str() if len(self.discards) == 0 else str(self.discards[-1])
        ]
        text = ""
        zipped_lines = zip(*[str(c).split('\n') for c in components])
        for zipped_line in zipped_lines:
            text += ' '.join(zipped_line) + '\n'
        return text.strip()

    def sequence_text(self):
        sequence_cards = Hand()
        for move in self.sequence:
            for card in move.cards():
                sequence_cards.add(card)
        return str(sequence_cards)

    def top_str(self, state):
        title_text = "== PLAYER =====      == HAND " + ("=" * (len(self.hand) * 16 - 9)) + "       == DECK =======   == DISCARDS ==="
        block_text = self.block_str(state)
        sequence_text = self.sequence_text()
        return '\n'.join(['', title_text, block_text, sequence_text, ''])

    def bottom_str(self, state):
        sequence_text = self.sequence_text()
        block_text = self.block_str(state)
        title_text = "== PLAYER =====      == HAND " + ("=" * (len(self.hand) * 16 - 9)) + "       == DECK =======   == DISCARDS ==="
        return '\n'.join(['', sequence_text, block_text, title_text, ''])

    def reshuffle_hand(self):
        hand_len = len(self.hand)
        for card in self.hand.cards:
            self.deck.reshuffle([card])
        self.hand.cards = []
        self.draw(hand_len)
