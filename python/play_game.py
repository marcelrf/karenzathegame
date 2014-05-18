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
    filename_1 = sys.argv[1]
    filename_2 = sys.argv[2]
    deck_json_1 = open(filename_1).read()[:-1]
    deck_json_2 = open(filename_2).read()[:-1]
    winner = play_game(deck_json_1, deck_json_2)
    
def play_game(deck_json_1, deck_json_2):
    g = game.Game()
    g.setup(deck_json_1, deck_json_2)
    while not g.has_ended():
        print g
        
        log("Turn for: Player%d" % g.turn)
        player = g.current_player()
        if g.player_is_threatened(): log("Player is threatened!")
        else: log("Player has the initiative!")
        
        move_feet_phase(g)
        play_card_phase(g)

def move_feet_phase(g):
    if not g.player_is_threatened() or g.last_moved > 0:
        log("Move feet phase")
        to_move = g.last_moved if g.player_is_threatened() else 2
        while to_move > 0:
            log("%d feet movements remaining" % to_move)
            log("Select left foot (l), right foot (r) or skip (s)")
            foot = raw_input("Option:")
            if foot == 's':
                break
            elif foot == 'l': foot = 'left_foot'
            elif foot == 'r': foot = 'right_foot'
            else:
                log('Invalid option, retry!')
                continue
            log("Select destiny (a, b, c, d) or skip (s)")
            destiny = raw_input('Option:')
            if destiny == 's':
                break
            elif destiny == 'a': destiny = 0
            elif destiny == 'b': destiny = 1
            elif destiny == 'c': destiny = 2
            elif destiny == 'd': destiny = 3
            else:
                log('Invalid option, retry!')
                continue
            g.apply_moves([[foot, destiny]])
            to_move -= 1
            print g

def play_card_phase(g):
    if g.player_is_threatened(): playable_type = C.DEFENSE
    else: playable_type = C.ATTACK
    player = g.current_player()
    playable = []
    for card in player.hand.cards:
        if card.type == playable_type and player.board.distance_to(card) == 0:
            playable.append(card)
    if len(playable) > 0:
        log("Play card phase")
        played = False
        while not played:
            log("Select card to play (1, 2, 3, 4, 5) or skip (s)")
            card = raw_input('Option:')
            if card == 's':
                break
            else:
                card = int(card) - 1
                if (card in range(len(player.hand.cards)) and
                    player.hand.cards[card].type == playable_type and
                    player.board.distance_to(player.hand.cards[card]) == 0):
                    card = player.hand.cards[card]
                    g.play_card(card)
                    played = True
                    print g
                else:
                    log('Invalid option, retry!')
                    continue




    #     player = g.current_player()
    #     if g.player_is_threatened():
    #         log("(player is threatened)")
    #         defense = choose_card(card.DEFENSE, player.hand, player.board, g.last_moved)
    #         if defense:
    #             moves = choose_moves(player.board, defense[0], g.last_moved)
    #             if moves:
    #                 g.apply_moves(moves)
    #             if LOGS:
    #                 print defense[0]
    #             if player_index == g.turn:
    #                 add_freq_to_list(played_cards, defense[0])
    #             g.play_card(defense[0])
    #         else:
    #             defense = choose_card(card.DEFENSE, player.hand, player.board)
    #             if defense:
    #                 moves = choose_moves(player.board, defense[0])
    #                 g.apply_moves(moves)
    #             log('AND PLAYER ' + str(2 if g.turn == 1 else 1) + ' SCORES ' + str(g.last_played.power) + ' POINTS')
    #             g.score()
    #             g.change_turn()
    #     else:
    #         log("(player has the initiative)")
    #         attack = choose_card(card.ATTACK, player.hand, player.board)
    #         defense = choose_card(card.DEFENSE, player.hand, player.board)
    #         if attack:
    #             if defense:
    #                 if attack[1] > defense[1] and attack[1] > 100:
    #                     moves = choose_moves(player.board, attack[0])
    #                     if moves:
    #                         g.apply_moves(moves)
    #                     if LOGS: print attack[0]
    #                     if player_index == g.turn:
    #                         add_freq_to_list(played_cards, attack[0])
    #                     g.play_card(attack[0])
    #                 else:
    #                     moves = choose_moves(player.board, defense[0])
    #                     if moves:
    #                         g.apply_moves(moves)
    #                     if g.hand_is_full():
    #                         discard(player.hand, player.board, [attack[0], defense[0]])
    #                     g.change_turn()
    #                     log('BOTH PLAYERS DRAW UP TO ' + str(game.CARDS_IN_HAND) + ' CARDS')
    #                     g.draw_event()
    #             else:
    #                 moves = choose_moves(player.board, attack[0])
    #                 if moves:
    #                     g.apply_moves(moves)
    #                 if LOGS: print attack[0]
    #                 if player_index == g.turn:
    #                     add_freq_to_list(played_cards, attack[0])
    #                 g.play_card(attack[0])
    #         elif defense:
    #             moves = choose_moves(player.board, defense[0])
    #             if moves:
    #                 g.apply_moves(moves)
    #             if g.hand_is_full():
    #                 discard(player.hand, player.board, [defense[0]])
    #             g.change_turn()
    #             log('BOTH PLAYERS DRAW UP TO ' + str(game.CARDS_IN_HAND) + ' CARDS')
    #             g.draw_event()
    #         else:
    #             if len(player.hand.cards) > 0:
    #                 moves = choose_moves(player.board, player.hand.cards[0])
    #                 g.apply_moves(moves)
    #             if g.hand_is_full():
    #                 discard(player.hand, player.board, [])
    #             g.change_turn()
    #             log('BOTH PLAYERS DRAW UP TO ' + str(game.CARDS_IN_HAND) + ' CARDS')
    #             g.draw_event()
    # log('################################')
    # log('GAME ENDED! SCORE: ' + str(g.player1.score) + '/' + str(g.player2.score))
    # log('################################')
    # if g.player1.score > g.player2.score: return '1'
    # elif g.player1.score == g.player2.score: return 'x'
    # else: return '2'

# def choose_card(type, hand, board, max_moves=2):
#     weighted_cards = []
#     for card in hand.cards:
#         if card.type == type and board.distance_to(card) <= max_moves:
#             rest = list(hand.cards)
#             rest.remove(card)
#             combos = get_combos(card, rest)
#             score = get_combos_score(combos)
#             weighted_cards.append([card, score])
#     weighted_cards.sort(key=lambda x: x[1], reverse=True)
#     return weighted_cards[0] if len(weighted_cards) > 0 else None

# def choose_moves(board, card, max_moves=2):
#     needed_moves = []
#     if board.left_foot != card.left_foot:
#         needed_moves.append(['left_foot', card.left_foot, card.left_foot == board.right_foot])
#     if board.right_foot != card.right_foot:
#         needed_moves.append(['right_foot', card.right_foot, card.right_foot == board.left_foot])
#     if board.sword != card.sword_origin:
#         needed_moves.append(['sword', card.sword_origin, False])
#     random.shuffle(needed_moves)
#     needed_moves.sort(key=lambda x: x[2])
#     chosen_moves = needed_moves[:max_moves]
#     return chosen_moves

# def get_combos(base, cards):
#     combos = [[base]]
#     for card in cards:
#         if base.distance_to(card) <= 2:
#             rest = list(cards)
#             rest.remove(card)
#             card_combos = get_combos(card, rest)
#             for card_combo in card_combos:
#                 combos.append([base] + card_combo)
#     return combos

# def get_combos_score(combos):
#     score = 0
#     for combo in combos:
#         length = len(combo)
#         mean_power = reduce(lambda x, y: x + y.power, combo, 0) / float(length)
#         mean_distance = reduce(lambda x, y: x + y, [combo[i].distance_to(combo[i + 1]) for i in range(length - 1)], 0) / float(length)
#         score += length / 5.0 * mean_power * (4 - mean_distance) / 4.0
#     return score

# def discard(hand, board, blacklist):
#     hand_copy = copy.copy(hand)
#     for card in blacklist:
#         hand_copy.cards.remove(card)
#     to_discard = random.choice(hand_copy.cards)
#     if LOGS:
#         print 'PLAYER DISCARDS'
#         print to_discard
#     hand.remove(to_discard)

# def read_control_decks():
#     filenames = os.listdir('../decks/control')
#     deck_jsons = [open('../decks/control/' + filename).read()[:-1] for filename in filenames]
#     return deck_jsons

# def add_freq_to_list(card_list, card):
#     found = False
#     for i in range(len(card_list)):
#         if card_list[i][0] == card:
#             card_list[i][1] += 1
#             found = True
#     if not found:
#         card_list.append([card, 1])

def log(message):
    print '###', message

if __name__ == '__main__':
    main()