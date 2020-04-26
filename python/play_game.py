
import importlib
from ktg.player import Player, PlayerState
from ktg.game import Game, Turn, INITIAL_CARDS_IN_HAND
from ktg.action import Action, ActionType
from copy import copy
import sys
import random


LOWEST_SCORE = -999999999
MIN_MAX_DEPTH = 4
EN_GARDE_SCORE = 2
INITIATIVE_SCORE = 2
MIN_MAX_DRAW_SAMPLE = 3
PROB_MIN_MAX_RESHUFFLES = 5


def evaluate(game):
    current = game.current_player()
    current_score = (
        current.score +
        len(current.hand) +
        (0 if current.in_sequence() else EN_GARDE_SCORE) +
        (0 if game.current_player_state() == PlayerState.THREATENED else INITIATIVE_SCORE)
    )
    other = game.other_player()
    other_score = (
        other.score +
        len(other.hand) +
        (0 if other.in_sequence() else EN_GARDE_SCORE) +
        (0 if game.current_player_state() == PlayerState.INITIATIVE else INITIATIVE_SCORE)
    )
    max_score = 9 + INITIAL_CARDS_IN_HAND + EN_GARDE_SCORE + INITIATIVE_SCORE
    normalized_score = float(current_score - other_score) / max_score
    #print('evaluate(%s) = %d, %d, %d, %d, %d, %d, %f' % (game.current_player().deck.character, current.score, len(current.hand), other.score, len(other.hand), current_score, other_score, normalized_score))
    return normalized_score


def prob_min_max(game, depth):
    #print('=='*(3-depth) + 'prob_min_max(%s,%d)' % (game.current_player().deck.character, depth))
    if game.is_over():
        #print('==game_is_over')
        winner = game.winner()
        if winner == game.current_player():
            return 1
        elif winner == game.other_player():
            return -1
        else: return 0
    if depth == 0:
        return evaluate(game)
    total_score = 0
    total_action_count = 0
    for reshuffle in range(PROB_MIN_MAX_RESHUFFLES):
        gc = copy(game)
        gc.current_player().reshuffle_hand()
        valid_moves = gc.get_valid_moves()
        valid_actions = [Action(ActionType.MOVE, m) for m in valid_moves]
        if gc.can_draw(valid_moves):
            valid_actions.append(Action(ActionType.DRAW))
        if gc.can_reguard(valid_moves):
            valid_actions.append(Action(ActionType.REGUARD))
        if len(valid_actions) == 0:
            valid_actions = [Action(ActionType.TOUCHE)]
        for action in valid_actions:
            total_action_count += 1
            #print('=='*(3-depth) + 'trying action: %s' % str(action))
            if action.action_type == ActionType.DRAW:
                draw_score = 0
                for i in range(MIN_MAX_DRAW_SAMPLE):
                    gc2 = copy(gc)
                    gc2.play(action)
                    if len(gc2.other_player().hand) > INITIAL_CARDS_IN_HAND:
                        gc2.other_player().discard_random(1)
                    draw_score += -min_max(gc2, depth - 1)
                action_score = float(draw_score) / MIN_MAX_DRAW_SAMPLE
            else:
                gc3 = copy(gc)
                current_turn = Turn.PLAYER_1 if gc3.current_player() == gc3.player_1 else Turn.PLAYER_2
                gc3.play(action)
                next_turn = Turn.PLAYER_1 if gc3.current_player() == gc3.player_1 else Turn.PLAYER_2
                if next_turn == current_turn:
                    action_score = prob_min_max(gc3, depth - 1)
                else:
                    action_score = -min_max(gc3, depth - 1)
            total_score += action_score
    normalized_score = total_score / float(total_action_count)
    #print('=='*(3-depth) + 'prob_min_max(%s,%d) -----> %d' % (game.current_player().deck.character, depth, normalized_score))
    return normalized_score


def min_max(game, depth):
    #print('**'*(3-depth) + 'min_max(%s,%d)' % (game.current_player().deck.character, depth))
    if game.is_over():
        #print('==game_is_over')
        winner = game.winner()
        if winner == game.current_player():
            return 1
        elif winner == game.other_player():
            return -1
        else: return 0
    if depth == 0:
        return evaluate(game)
    valid_moves = game.get_valid_moves()
    valid_actions = [Action(ActionType.MOVE, move) for move in valid_moves]
    if game.can_draw(valid_moves):
        valid_actions.append(Action(ActionType.DRAW))
    if game.can_reguard(valid_moves):
        valid_actions.append(Action(ActionType.REGUARD))
    if len(valid_actions) == 0:
        valid_actions = [Action(ActionType.TOUCHE)]
    best_score = LOWEST_SCORE
    for action in valid_actions:
        #print('**'*(3-depth) + 'trying action: %s' % str(action))
        if action.action_type == ActionType.DRAW:
            draw_score = 0
            for i in range(MIN_MAX_DRAW_SAMPLE):
                gc = copy(game)
                gc.play(action)
                if len(gc.other_player().hand) > INITIAL_CARDS_IN_HAND:
                    gc.other_player().discard_random(1)
                draw_score += -prob_min_max(gc, depth - 1)
            action_score = float(draw_score) / MIN_MAX_DRAW_SAMPLE
        else:
            gc2 = copy(game)
            current_turn = Turn.PLAYER_1 if gc2.current_player() == gc2.player_1 else Turn.PLAYER_2
            gc2.play(action)
            next_turn = Turn.PLAYER_1 if gc2.current_player() == gc2.player_1 else Turn.PLAYER_2
            if next_turn == current_turn:
                action_score = min_max(gc2, depth - 1)
            else:
                action_score = -prob_min_max(gc2, depth - 1)
        if action_score > best_score:
            best_score = action_score
    #print('**'*(3-depth) + 'min_max(%s,%d) -------> %d' % (game.current_player().deck.character, depth, best_score))
    return best_score


if __name__ == '__main__':
    player_1_deck = importlib.import_module("decks." + sys.argv[1]).deck
    player_2_deck = importlib.import_module("decks." + sys.argv[3]).deck
    player_1 = Player(player_1_deck)
    player_2 = Player(player_2_deck)
    g = Game(player_1, player_2)
    player_types = {}
    player_types[Turn.PLAYER_1] = sys.argv[2]
    player_types[Turn.PLAYER_2] = sys.argv[4]
    while not g.is_over():
        print(g)
        valid_moves = g.get_valid_moves()
        if player_types[g.turn] == "human":
            index = 0
            for move in valid_moves:
                print(str(index) + ') ' + ' + '.join([c.name for c in move.cards()]))
                index += 1
            while True:
                choice = raw_input("Choose: ")
                if choice == 'd' and g.can_draw(valid_moves): break
                elif choice == 'r' and g.can_reguard(valid_moves): break
                elif choice == 't' and g.current_player_state() == PlayerState.THREATENED and len(valid_moves) == 0: break
                elif choice.isdigit() and int(choice) >= 0 and int(choice) < len(valid_moves): break
            if choice == 'd':
                g.play(Action(ActionType.DRAW))
                if len(g.other_player().hand) > INITIAL_CARDS_IN_HAND:
                    choice = raw_input("Discard: ")
                    g.other_player().discard_at(index)
            elif choice == 'r': g.play(Action(ActionType.REGUARD))
            elif choice == 't': g.play(Action(ActionType.TOUCHE))
            else: g.play(Action(ActionType.MOVE, valid_moves[int(choice)]))
        elif player_types[g.turn] == "computer":

            # collect valid actions
            valid_actions = [Action(ActionType.MOVE, move) for move in valid_moves]
            if g.can_draw(valid_moves):
                valid_actions.append(Action(ActionType.DRAW))
            if g.can_reguard(valid_moves):
                valid_actions.append(Action(ActionType.REGUARD))
            if len(valid_actions) == 0:
                valid_actions = [Action(ActionType.TOUCHE)]
            # find best action
            if len(valid_actions) == 1:
                best_action = valid_actions[0]
            else:
                best_action, best_score = None, LOWEST_SCORE
                for action in valid_actions:
                    # treat draw actions probabilistically
                    if action.action_type == ActionType.DRAW:
                        draw_score = 0
                        for i in range(MIN_MAX_DRAW_SAMPLE):
                            gc = copy(g)
                            gc.play(action)
                            #print('&&&&&&&&& try drawing: ' + str(action))
                            if len(gc.other_player().hand) > INITIAL_CARDS_IN_HAND:
                                gc.other_player().discard_random(1)
                            draw_score += -prob_min_max(gc, MIN_MAX_DEPTH)
                        action_score = float(draw_score) / MIN_MAX_DRAW_SAMPLE
                    else:
                        gc2 = copy(g)
                        current_turn = Turn.PLAYER_1 if gc2.current_player() == gc2.player_1 else Turn.PLAYER_2
                        #print('@@@@@@@@@@@@@@@@@@@@@@@ try action: ' + str(action))
                        gc2.play(action)
                        next_turn = Turn.PLAYER_1 if gc2.current_player() == gc2.player_1 else Turn.PLAYER_2
                        if next_turn == current_turn:
                            action_score = min_max(gc2, MIN_MAX_DEPTH)
                        else:
                            action_score = -prob_min_max(gc2, MIN_MAX_DEPTH)
                    print(str(action) + " " + str(action_score))
                    if action_score > best_score:
                        best_score = action_score
                        best_action = action
            print(g.current_player().deck.character + " " + str(best_action))
            g.play(best_action)
            # if necessary choose what to discard
            if len(g.other_player().hand) > INITIAL_CARDS_IN_HAND:
                best_discard, best_score = None, LOWEST_SCORE
                for card in g.other_player().hand.cards:
                    gc3 = copy(g)
                    gc3.other_player().discard(card)
                    discard_score = -prob_min_max(gc3, MIN_MAX_DEPTH)
                    print("Discard " + card.name + " " + str(discard_score))
                    if discard_score > best_score:
                        best_score = discard_score
                        best_discard = card
                g.other_player().discard(best_discard)

    if g.winner() is None: print("THE GAME IS A DRAW!")
    else: print("THE WINNER IS: %s!" % g.winner().deck.character)
