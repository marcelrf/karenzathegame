# coding: utf-8

import sys
import player
from card import *

CARDS_IN_HAND = 5

def main():
    filename1, filename2 = sys.argv[1:3]
    deck_json1, deck_json2 = open(filename1).read()[:-1], open(filename2).read()[:-1]
    game = Game()
    game.setup(deck_json1, deck_json2)
    # while not game.has_ended():
    player = game.current_player()
    if game.is_threatened():
        defense = choose_card(DEFENSE, player.hand, player.board, game.last_moved)
        if defense:
            moves = choose_moves(player.board, defense[0], game.last_moved)
            pass#moveit
            pass#playit
        else:
            defense = choose_card(DEFENSE, player.hand, player.board)
            if defense:
                moves = choose_moves(player.board, defense[0])
                if moves:
                    pass#moveit
    else:
        attack = choose_card(ATTACK, player.hand, player.board)
        defense = choose_card(DEFENSE, player.hand, player.board)
        if attack:
            if defense:
                if attack[1] > defense[1] and attack[1] > 100:
                    moves = choose_moves(player.board, attack[0])
                    pass#moveit
                    pass#playit
                else:
                    moves = choose_moves(player.board, defense[0])
                    pass#moveit
                    pass#discard?
            else:
                moves = choose_moves(player.board, attack[0])
                pass#moveit
                pass#playit
        elif defense:
            moves = choose_moves(player.board, defense[0])
            pass#moveit
            pass#discard?
        else:
            pass#discard?

class Game(object):

    def __init__(self):
        self.player1 = player.Player()
        self.player2 = player.Player()
        self.last_played = None
        self.last_moved = 0
        self.turn = 1

    def __str__(self):
        text  = "############################## Player1:\n"
        text += str(self.player1) + "\n"
        text += "############################## Player2:\n"
        text += str(self.player2) + "\n"
        text += "##############################\n"
        return text

    def current_player(self):
        if self.turn == 1: return self.player1
        elif self.turn == 2: return player2
        else: return None

    def setup(self, deck_json1, deck_json2):
        self.player1.setup(deck_json1, CARDS_IN_HAND)
        self.player2.setup(deck_json2, CARDS_IN_HAND)

    def is_threatened(self):
        return self.last_played and last_played.type == ATTACK

    def has_ended(self):
        return (
            self.player1.score >= 10 or
            self.player2.score >= 10
        )

def choose_card(type, hand, board, max_moves=2):
    weighted_cards = []
    for card in hand.cards:
        if card.type == type and board.distance_to(card) <= max_moves:
            rest = list(hand.cards)
            rest.remove(card)
            combos = get_combos(card, rest)
            score = get_combos_score(combos)
            weighted_cards.append([card, score])
    weighted_cards.sort(key=lambda x: x[1], reverse=True)
    return weighted_cards[0] if len(weighted_cards) > 0 else None

def choose_moves(board, card, max_moves=2):
    needed_moves = []
    if board.left_foot != card.left_foot:
        needed_moves.append(['left_foot', card.left_foot, card.left_foot == board.right_foot])
    if board.right_foot != card.right_foot:
        needed_moves.append(['right_foot', card.right_foot, card.right_foot == board.left_foot])
    if board.sword != card.sword_origin:
        needed_moves.append(['sword', card.sword_origin, False])
    random.shuffle(needed_moves)
    needed_moves.sort(key=lambda x: x[2])
    chosen_moves = needed_moves[:max_moves]
    return chosen_moves

def get_combos(base, cards):
    combos = [[base]]
    for card in cards:
        if base.distance_to(card) <= 2:
            rest = list(cards)
            rest.remove(card)
            card_combos = get_combos(card, rest)
            for card_combo in card_combos:
                combos.append([base] + card_combo)
    return combos

def get_combos_score(combos):
    score = 0
    for combo in combos:
        length = len(combo)
        mean_power = reduce(lambda x, y: x + y.power, combo, 0) / float(length)
        mean_distance = reduce(lambda x, y: x + y, [combo[i].distance_to(combo[i + 1]) for i in range(length - 1)], 0) / float(length)
        score += length / 5.0 * mean_power * (4 - mean_distance) / 4.0
    return score

if __name__ == '__main__':
    main()