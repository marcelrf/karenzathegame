# coding: utf-8

import sys
import random
import copy
import ktg
from ktg import game
from ktg import player
from ktg import card

def main():
    log("setting up game...")
    filename1, filename2 = sys.argv[1:3]
    deck_json1, deck_json2 = open(filename1).read()[:-1], open(filename2).read()[:-1]
    g = game.Game()
    g.setup(deck_json1, deck_json2)
    log("starting game...")
    while not g.has_ended():
        print g
        log("turn for player %d" % g.turn)
        player = g.current_player()
        if g.player_is_threatened():
            log("(player is threatened)")
            defense = choose_card(card.DEFENSE, player.hand, player.board, g.last_moved)
            if defense:
                # log("can play a defense!")
                moves = choose_moves(player.board, defense[0], g.last_moved)
                if moves:
                    # log("will move some pieces...")
                    g.apply_moves(moves)
                # log("and plays the defense")
                print 'PLAYER PLAYS THE CARD'
                print defense[0]
                g.play_card(defense[0])
            else:
                # log("can NOT play defense!")
                defense = choose_card(card.DEFENSE, player.hand, player.board)
                if defense:
                    moves = choose_moves(player.board, defense[0])
                    # log("at least will move some pieces...")
                    g.apply_moves(moves)
                g.score()
        else:
            log("(player has the initiative)")
            attack = choose_card(card.ATTACK, player.hand, player.board)
            defense = choose_card(card.DEFENSE, player.hand, player.board)
            if attack:
                if defense:
                    if attack[1] > defense[1] and attack[1] > 100:
                        # log("chooses to attack!")
                        moves = choose_moves(player.board, attack[0])
                        if moves:
                            # log("will move some pieces...")
                            g.apply_moves(moves)
                        # log("and plays the attack")
                        print 'PLAYER PLAYS THE CARD'
                        print attack[0]
                        g.play_card(attack[0])
                    else:
                        # log("chooses NOT to attack!")
                        moves = choose_moves(player.board, defense[0])
                        if moves:
                            # log("at least will move some pieces...")
                            g.apply_moves(moves)
                        if g.hand_is_full():
                            discard(player.hand, player.board, [attack[0], defense[0]])
                        g.change_turn()
                        g.draw_event()
                else:
                    # log("chooses to attack!")
                    moves = choose_moves(player.board, attack[0])
                    if moves:
                        # log("will move some pieces...")
                        g.apply_moves(moves)
                    # log("and plays the attack")
                    print 'PLAYER PLAYS THE CARD'
                    print attack[0]
                    g.play_card(attack[0])
            elif defense:
                # log("can NOT play attack!")
                moves = choose_moves(player.board, defense[0])
                if moves:
                    # log("at least will move some pieces...")
                    g.apply_moves(moves)
                if g.hand_is_full():
                    discard(player.hand, player.board, [defense[0]])
                g.change_turn()
                g.draw_event()
            else:
                # log("WOW player can not play any card!")
                if len(player.hand.cards) > 0:
                    moves = choose_moves(player.board, player.hand.cards[0])
                    # log("at least will move some pieces...")
                    g.apply_moves(moves)
                if g.hand_is_full():
                    discard(player.hand, player.board, [])
                g.change_turn()
                g.draw_event()
        # sys.stdin.readline()
    print '##################################'
    print 'GAME ENDED!'
    print 'SCORE: ' + str(g.player1.score) + '/' + str(g.player2.score)

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
    print 'PLAYER DISCARDS'
    print to_discard
    hand.remove(to_discard)

def log(message):
    print '###', message

if __name__ == '__main__':
    main()