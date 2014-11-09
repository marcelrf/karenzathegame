# coding: utf-8

import player
import card

TURN_1, TURN_2, PRE_TURN_1, PRE_TURN_2 = range(4)
CARDS_IN_HAND = 5

class Game(object):

    def __init__(self, deck_json_1, deck_json_2):
        self.player1 = player.Player(deck_json_1)
        self.player2 = player.Player(deck_json_2)
        for i in range(CARDS_IN_HAND):
            self.player1.draw()
            self.player2.draw()
        self.turn = PRE_TURN_1

    def __str__(self):
        text  = "############################## Player1:\n"
        text += str(self.player1) + "\n"
        text += "############################## Player2:\n"
        text += str(self.player2) + "\n"
        text += "##############################\n"
        return text

    def get_current_player(self):
        if self.turn in [TURN_1, PRE_TURN_1]:
            return self.player1
        else:
            return self.player2

    def get_last_player(self):
        if self.turn in [TURN_1, PRE_TURN_1]:
            return self.player2
        else:
            return self.player1

    def player_is_threatened(self):
        last_player = self.get_last_player()
        return (
            last_player.played is not None and
            last_player.played.type == card.ATTACK
        )

    def has_ended(self):
        return (
            self.player1.score >= 10 or
            self.player2.score >= 10 or
            len(self.player1.deck) == 0
        )

    def is_pre_turn(self):
        return self.turn in [PRE_TURN_1, PRE_TURN_2]

    def turn_number(self):
        if self.turn in [PRE_TURN_1, TURN_1]:
            return 1
        else:
            return 2

    def draw_card(self):
        current_player = self.get_current_player()
        current_player.draw()

    def change_turn(self):
        if self.turn == PRE_TURN_1: self.turn = PRE_TURN_2
        elif self.turn == PRE_TURN_2: self.turn = TURN_1
        else: self.turn = TURN_2 if self.turn == TURN_1 else TURN_1

    def apply_move(self, token, position):
        current_player = self.get_current_player()
        current_player.move(token, position)

    def get_playable(self):
        current_player = self.get_current_player()
        playable = []
        for index in range(len(current_player.hand)):
            if self.is_playable(index):
                playable.append(index)
        return playable

    def is_playable(self, index):
        current_player = self.get_current_player()
        card_at = current_player.hand.card_at(index)
        threatened = self.player_is_threatened()
        return (
            (threatened and card_at.type == card.DEFENSE or
            not threatened and card_at.type == card.ATTACK) and
            current_player.board.distance_to(card_at) == 0
        )

    def play_card(self, index):
        current_player = self.get_current_player()
        last_player = self.get_last_player()
        current_player.play(index)
        if (not self.player_is_threatened() or
            current_player.played.power < last_player.played.power):
            self.change_turn()
        else:
            last_player.played = None

    def discard_card(self, index):
        current_player = self.get_current_player()
        last_player = self.get_last_player()
        current_player.discard(index)
        if self.player_is_threatened():
            last_player.score += last_player.played.power
        self.change_turn()
