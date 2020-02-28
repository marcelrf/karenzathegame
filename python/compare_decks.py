
import importlib
import random
from ktg.game import Game
from copy import copy


NUMBER_OF_GAMES = 1000
MONTE_CARLO_DEPTH = 10
MONTE_CARLO_WIDTH = 1000
WINNING_SCORE = 3
DRAWING_SCORE = 1


def evaluate(game):
    current_score = game.current_player().score
    other_score = game.other_player().score
    difference = current_score - other_score
    return 0 if difference == 0 else int(difference / abs(difference))


def monte_carlo(game, depth):
    if game.is_finished():
        return game.winner()
    elif depth == 0:
        return evaluate(game)
    else:
        valid_moves = game.valid_moves()
        move = random.choice(valid_moves)
        game.play(move)
        return -monte_carlo(game, depth - 1)


def play_game(game):
    while not game.is_over():
        print('calculating best move...')
        best_move, best_score = None, 0
        for move in game.get_valid_moves():
            move_score = 0
            for i in range(MONTE_CARLO_WIDTH):
                print('executing montecarlo %d' % i)
                game_copy = copy(game)
                game_copy.play(move)
                game_copy.other_player().reshuffle_hand()
                winner = monte_carlo(game_copy, MONTE_CARLO_DEPTH)
                if winner == -1: move_score += WINNING_SCORE
                elif winner == 0: move_score += DRAWING_SCORE
            if move_score > best_score:
                best_move = move
                best_score = move_score
        game.play(best_move)
    return game.winner()


def compare_decks(deck_1, deck_2):
    # deck_1 wins, draws, deck_2 wins
    results = [0, 0, 0]
    for i in range(NUMBER_OF_GAMES):
        print('playing game %d' % i)
        if i % 2 == 0:
            game = Game(deck_1, deck_2)
            winner = play_game(game)
            results[-winner + 1] += 1
        else:
            game = Game(deck_2, deck_1)
            winner = play_game(game)
            results[winner + 1] += 1
    return results


if __name__ == '__main__':
    deck_eka = importlib.import_module("decks.eka").deck
    deck_michi = importlib.import_module("decks.michi").deck
    from ktg.hand import Hand
    hand = Hand()
    for i in range(7):
        hand.add(deck_eka.draw())
    print(hand)
    hand = Hand()
    for i in range(7):
        hand.add(deck_michi.draw())
    print(hand)


    # deck_2 = importlib.import_module("decks.karenza").deck
    # results = compare_decks(deck_1, deck_2)
    # print(results)
