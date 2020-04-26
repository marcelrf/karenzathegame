
import importlib
from ktg.player import Player, PlayerState
from ktg.game import Game, Turn, INITIAL_CARDS_IN_HAND
from ktg.action import Action, ActionType
from copy import copy
import sys
import random


# LOWEST_SCORE = -999999999
# MIN_MAX_DEPTH = 4
# EN_GARDE_SCORE = 2
# INITIATIVE_SCORE = 2
# MIN_MAX_DRAW_SAMPLE = 3
#
#
# def evaluate(game):
#     current = game.current_player()
#     current_score = (
#         current.score +
#         len(current.hand) +
#         (0 if current.in_sequence() else EN_GARDE_SCORE) +
#         (0 if game.current_player_state() == PlayerState.THREATENED else INITIATIVE_SCORE)
#     )
#     other = game.other_player()
#     other_score = (
#         other.score +
#         len(other.hand) +
#         (0 if other.in_sequence() else EN_GARDE_SCORE) +
#         (0 if game.current_player_state() != PlayerState.THREATENED else INITIATIVE_SCORE)
#     )
#     max_score = float(9 + INITIAL_CARDS_IN_HAND + EN_GARDE_SCORE + INITIATIVE_SCORE)
#     normalized_score = (current_score - other_score) / max_score
#     return normalized_score
#
#
# def prob_min_max(game, depth):
#     return evaluate(game)


MONTE_CARLO_ITERATIONS = 1000
WINNING_SCORE = 1
LOOSING_SCORE = -1


def get_action_score(game, player, iterations):
    action_score = 0
    for i in range(iterations):
        game_copy = copy(game)
        game_copy.current_player().reshuffle_hand()
        winner = monte_carlo(game_copy)
        if winner == player: action_score += WINNING_SCORE
        elif winner is not None: action_score += LOOSING_SCORE
    return action_score


def monte_carlo(game):
    if game.is_over():
        winner = game.winner()
        if winner == game.player_1:
            return Turn.PLAYER_1
        elif winner == game.player_2:
            return Turn.PLAYER_2
        else:
            return None
    else:
        valid_moves = game.get_valid_moves()
        valid_actions = [Action(ActionType.MOVE, move) for move in valid_moves]
        if game.can_draw(valid_moves):
            valid_actions.append(Action(ActionType.DRAW))
        if game.can_reguard(valid_moves):
            valid_actions.append(Action(ActionType.REGUARD))
        if len(valid_actions) == 0:
            game.play(Action(ActionType.TOUCHE))
        else:
            action = random.choice(valid_actions)
            game.play(action)
            if (action.action_type == ActionType.DRAW and
                len(game.other_player().hand) > INITIAL_CARDS_IN_HAND):
                game.other_player().discard_random(1)
        return monte_carlo(game)


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
            # # collect valid actions
            # valid_actions = [Action(ActionType.MOVE, move) for move in valid_moves]
            # if g.can_draw(valid_moves):
            #     valid_actions.append(Action(ActionType.DRAW))
            # if g.can_reguard(valid_moves):
            #     valid_actions.append(Action(ActionType.REGUARD))
            # if len(valid_actions) == 0:
            #     valid_actions = [Action(ActionType.TOUCHE)]
            # # find best action
            # if len(valid_actions) == 1:
            #     best_action = valid_actions[0]
            # else:
            #     best_action, best_score = None, LOWEST_SCORE
            #     for action in valid_actions:
            #         # treat draw actions probabilistically
            #         if action.action_type == ActionType.DRAW:
            #             draw_score = 0
            #             for i in range(MIN_MAX_DRAW_SAMPLE):
            #                 gc = copy(g)
            #                 gc.play(action)
            #                 if len(g.other_player().hand) > INITIAL_CARDS_IN_HAND:
            #                     g.other_player().discard_random(1)
            #                 draw_score += -prob_min_max(gc, MIN_MAX_DEPTH)
            #             action_score = draw_score / MIN_MAX_DRAW_SAMPLE
            #         else:
            #             gc = copy(g)
            #             gc.play(action)
            #             action_score = -prob_min_max(gc, MIN_MAX_DEPTH)
            #         print(str(action) + " " + str(action_score))
            #         if action_score > best_score:
            #             best_score = action_score
            #             best_action = action
            # print(g.current_player().deck.character + " " + str(best_action))
            # g.play(best_action)
            # # if necessary choose what to discard
            # if len(g.other_player().hand) > INITIAL_CARDS_IN_HAND:
            #     best_discard, best_score = None, LOWEST_SCORE
            #     for card in g.other_player().hand.cards:
            #         gc = copy(g)
            #         gc.other_player().discard(card)
            #         discard_score = -prob_min_max(gc, MIN_MAX_DEPTH)
            #         print("Discard " + card.name + " " + str(discard_score))
            #         if discard_score > best_score:
            #             best_score = discard_score
            #             best_discard = card
            #     g.other_player().discard(best_discard)

            # MONTE CARLO
            valid_actions = [Action(ActionType.MOVE, move) for move in valid_moves]
            if g.can_draw(valid_moves):
                valid_actions.append(Action(ActionType.DRAW))
            if g.can_reguard(valid_moves):
                valid_actions.append(Action(ActionType.REGUARD))
            if len(valid_actions) == 0:
                g.play(Action(ActionType.TOUCHE))
            else:
                best_action, best_score = None, -99999999999
                for action in valid_actions:
                    gc = copy(g)
                    player = Turn.PLAYER_1 if g.current_player() == g.player_1 else Turn.PLAYER_2
                    gc.play(action)
                    action_score = get_action_score(gc, player, MONTE_CARLO_ITERATIONS)
                    print(str(action) + " " + str(action_score))
                    if action_score > best_score:
                        best_action = action
                        best_score = action_score
                g.play(best_action)
                print(g.other_player().deck.character + " " + str(best_action))
                if (best_action.action_type == ActionType.DRAW and
                    len(g.other_player().hand) > INITIAL_CARDS_IN_HAND):
                    g.other_player().discard_random(1)

    if g.winner() is None: print("THE GAME IS A DRAW!")
    else: print("THE WINNER IS: %s!" % g.winner().deck.character)
