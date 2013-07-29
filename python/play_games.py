# coding: utf-8

import sys
import os
import random
import copy
import ktg
from ktg import game
from ktg import player
from ktg import card
from collections import defaultdict

GAMES = 5
LOGS = False

played_cards = []

def main():
    control_decks = read_control_decks()
    filename = sys.argv[1]
    deck_json = open(filename).read()[:-1]
    wins, ties, losses = 0, 0, 0
    for control_json in control_decks:
        for i in range(GAMES):
            winner = play_game(deck_json, control_json, 1)
            if winner == '1': wins += 1
            elif winner == 'x': ties += 1
            elif winner == '2': losses += 1
            winner = play_game(control_json, deck_json, 2)
            if winner == '2': wins += 1
            elif winner == 'x': ties += 1
            elif winner == '1': losses += 1
    print "%d/%d/%d" % (wins, ties, losses)
    played_cards.sort(key=lambda x: x[1], reverse=True)
    print "most played card:"
    print played_cards[0][0]
    print "least played card:"
    print played_cards[-1][0]
    
def play_game(deck_json1, deck_json2, player_index):
    g = game.Game()
    g.setup(deck_json1, deck_json2)
    while not g.has_ended():
        if LOGS: print g
        log("turn for player %d" % g.turn)
        player = g.current_player()
        if g.player_is_threatened():
            log("(player is threatened)")
            defense = choose_card(card.DEFENSE, player.hand, player.board, g.last_moved)
            if defense:
                moves = choose_moves(player.board, defense[0], g.last_moved)
                if moves:
                    g.apply_moves(moves)
                if LOGS:
                    print defense[0]
                if player_index == g.turn:
                    add_freq_to_list(played_cards, defense[0])
                g.play_card(defense[0])
            else:
                defense = choose_card(card.DEFENSE, player.hand, player.board)
                if defense:
                    moves = choose_moves(player.board, defense[0])
                    g.apply_moves(moves)
                log('AND PLAYER ' + str(2 if g.turn == 1 else 1) + ' SCORES ' + str(g.last_played.power) + ' POINTS')
                g.score()
                g.change_turn()
        else:
            log("(player has the initiative)")
            attack = choose_card(card.ATTACK, player.hand, player.board)
            defense = choose_card(card.DEFENSE, player.hand, player.board)
            if attack:
                if defense:
                    if attack[1] > defense[1] and attack[1] > 100:
                        moves = choose_moves(player.board, attack[0])
                        if moves:
                            g.apply_moves(moves)
                        if LOGS: print attack[0]
                        if player_index == g.turn:
                            add_freq_to_list(played_cards, attack[0])
                        g.play_card(attack[0])
                    else:
                        moves = choose_moves(player.board, defense[0])
                        if moves:
                            g.apply_moves(moves)
                        if g.hand_is_full():
                            discard(player.hand, player.board, [attack[0], defense[0]])
                        g.change_turn()
                        log('BOTH PLAYERS DRAW UP TO ' + str(game.CARDS_IN_HAND) + ' CARDS')
                        g.draw_event()
                else:
                    moves = choose_moves(player.board, attack[0])
                    if moves:
                        g.apply_moves(moves)
                    if LOGS: print attack[0]
                    if player_index == g.turn:
                        add_freq_to_list(played_cards, attack[0])
                    g.play_card(attack[0])
            elif defense:
                moves = choose_moves(player.board, defense[0])
                if moves:
                    g.apply_moves(moves)
                if g.hand_is_full():
                    discard(player.hand, player.board, [defense[0]])
                g.change_turn()
                log('BOTH PLAYERS DRAW UP TO ' + str(game.CARDS_IN_HAND) + ' CARDS')
                g.draw_event()
            else:
                if len(player.hand.cards) > 0:
                    moves = choose_moves(player.board, player.hand.cards[0])
                    g.apply_moves(moves)
                if g.hand_is_full():
                    discard(player.hand, player.board, [])
                g.change_turn()
                log('BOTH PLAYERS DRAW UP TO ' + str(game.CARDS_IN_HAND) + ' CARDS')
                g.draw_event()
    log('################################')
    log('GAME ENDED! SCORE: ' + str(g.player1.score) + '/' + str(g.player2.score))
    log('################################')
    if g.player1.score > g.player2.score: return '1'
    elif g.player1.score == g.player2.score: return 'x'
    else: return '2'

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

def discard(hand, board, blacklist):
    hand_copy = copy.copy(hand)
    for card in blacklist:
        hand_copy.cards.remove(card)
    to_discard = random.choice(hand_copy.cards)
    if LOGS:
        print 'PLAYER DISCARDS'
        print to_discard
    hand.remove(to_discard)

def read_control_decks():
    filenames = os.listdir('../decks/control')
    deck_jsons = [open('../decks/control/' + filename).read()[:-1] for filename in filenames]
    return deck_jsons

def add_freq_to_list(card_list, card):
    found = False
    for i in range(len(card_list)):
        if card_list[i][0] == card:
            card_list[i][1] += 1
            found = True
    if not found:
        card_list.append([card, 1])

def log(message):
    if LOGS: print '###', message

if __name__ == '__main__':
    main()