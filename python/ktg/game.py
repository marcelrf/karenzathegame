# coding: utf-8

import player
import card

CARDS_IN_HAND = 5

class Game(object):

    def __init__(self):
        self.player1 = player.Player()
        self.player2 = player.Player()
        self.last_played = None
        self.last_moved = 0
        self.turn = 1
        self.time_up = False

    def __str__(self):
        text  = "############################## Player1:\n"
        text += str(self.player1) + "\n"
        text += "############################## Player2:\n"
        text += str(self.player2) + "\n"
        text += "##############################\n"
        return text

    def setup(self, deck_json1, deck_json2):
        self.player1.setup(deck_json1, CARDS_IN_HAND)
        self.player2.setup(deck_json2, CARDS_IN_HAND)

    def current_player(self):
        if self.turn == 1: return self.player1
        elif self.turn == 2: return self.player2
        else: return None

    def player_is_threatened(self):
        return self.last_played and self.last_played.type == card.ATTACK

    def has_ended(self):
        return (
            self.player1.score >= 10 or
            self.player2.score >= 10 or
            self.time_up
        )

    def change_turn(self):
        self.turn = 1 if self.turn == 2 else 2

    def hand_is_full(self):
        player = self.current_player()
        return len(player.hand.cards) == CARDS_IN_HAND

    def draw_event(self):
        print 'BOTH PLAYERS DRAW UP TO ' + str(CARDS_IN_HAND) + ' CARDS'
        try:
            self.player1.draw_up_to(CARDS_IN_HAND)
            self.player2.draw_up_to(CARDS_IN_HAND)
        except:
            self.time_up = True

    def apply_moves(self, moves):
        player = self.current_player()
        for move in moves:
            print "PLAYER MOVES %s TO POSITION %d" % (move[0], move[1])
            setattr(player.board, move[0], move[1])
        self.last_moved = len(moves)

    def play_card(self, card):
        player = self.current_player()
        player.hand.remove(card)
        move = ['sword', card.sword_destiny]
        self.apply_moves([move])
        if self.player_is_threatened():
            if card.power < self.last_played.power:
                self.change_turn()
        else: self.change_turn()
        self.last_played = card

    def score(self):
        scorer = 1 if self.turn == 2 else 2
        print 'AND PLAYER ' + str(scorer) + ' SCORES ' + str(self.last_played.power) + ' POINTS'
        if scorer == 1: self.player1.score += self.last_played.power
        elif scorer == 2: self.player2.score += self.last_played.power
        self.last_played = None
