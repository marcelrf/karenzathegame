# coding: utf-8

import sys
import player

CARDS_IN_HAND = 5

def main():
    filename1, filename2 = sys.argv[1:3]
    deck_json1, deck_json2 = open(filename1).read()[:-1], open(filename2).read()[:-1]
    game = Game(deck_json1, deck_json2)
    game.setup()
    print game

class Game(object):

    def __init__(self, deck_json1, deck_json2):
        self.player1 = player.Player(deck_json1)
        self.player2 = player.Player(deck_json2)
        self.last_played = None
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

    def setup(self):
        self.player1.draw_up_to(CARDS_IN_HAND)
        self.player2.draw_up_to(CARDS_IN_HAND)

if __name__ == '__main__':
    main()