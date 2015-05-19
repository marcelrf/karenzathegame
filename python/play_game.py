# coding: utf-8

import sys
import os
import random
import copy
import ktg
from ktg import game
from ktg import player
from ktg import card as C
from collections import defaultdict

def main():
    deck_json_1, deck_json_2 = get_decks()
    g = game.Game(deck_json_1, deck_json_2)
    while not g.has_ended():
        print g
        log("Turn for: Player%d" % g.turn_number())
        if g.is_pre_turn():
            move_token_phase(g)
            g.change_turn()
        else:
            if g.player_is_threatened(): log("Player is threatened!")
            else: log("Player has the initiative!")
            draw_card_phase(g)
            played = play_card_phase(g)
            if not played:
                move_token_phase(g)
                discard_phase(g)
    log("Game ended. Player1: %s, Player2: %s" % (g.player1.score, g.player2.score))

def get_decks():
    filename_1 = sys.argv[1]
    filename_2 = sys.argv[2]
    deck_json_1 = open(filename_1).read()[:-1]
    deck_json_2 = open(filename_2).read()[:-1]
    return [deck_json_1, deck_json_2]

def move_token_phase(g):
    log("Place sword phase")
    while True:
        log("Select destiny (1, 2, 3, 4) or skip (s)")
        position = raw_input('Option:')
        if position in ['a', '1']: position = 0
        elif position in ['b', '2']: position = 1
        elif position in ['c', '3']: position = 2
        elif position in ['d', '4']: position = 3
        elif position == 's': continue
        else:
            log('Invalid option, retry!')
            continue
        g.apply_move('sword', position)
        break
    print g

def draw_card_phase(g):
    g.draw_card()
    print g
    log("You drawed a card")

def play_card_phase(g):
    playable = [str(x) for x in g.get_playable()]
    played = None
    if len(playable) > 0:
        log("Play card phase")
        while not played:
            log("Select card to play (" + " ,".join(playable) + ") or skip (s)")
            card = raw_input('Option:')
            if card == 's': break
            else:
                try:
                    card = int(card)
                    g.play_card(card)
                    played = True
                except:
                    log('Invalid option, retry!')
                    continue                
    print g
    return played

def discard_phase(g):
    log("Discard phase")
    while True:
        log("Select card to discard (1, 2, 3, 4, 5, 6)")
        card = raw_input('Option:')
        try:
            card = int(card)
            g.discard_card(card)
            break
        except:
            log('Invalid option, retry!')
            continue
    print g

def log(message):
    print '###', message

if __name__ == '__main__':
    main()