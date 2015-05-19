
import json
import sys
from ktg.card import ATTACK, DEFENSE, Card
from ktg.deck import Deck
from ktg.hand import Hand
from collections import defaultdict


STOP, PLAYER, OPPONENT = range(3)
ITERATIONS = 10000
CARDS_IN_HAND = 5


class Player(object):

    def __init__(self, hand):
        self.hand = hand
        self.played = []

    def last_played(self):
        if len(self.played) == 0:
            return None
        else:
            return self.played[-1]

    def last_played_hard(self):
        clear_played = [x for x in self.played if x is not None]
        if len(clear_played) == 0:
            return None
        else:
            return clear_played[-1]

    def get_playables(self, last_played_by_opponent):
        playables = set([])
        for card in self.hand.cards:
            if (
                (not self.last_played_hard() or self.last_played_hard().leads_to(card)) and
                (
                    not last_played_by_opponent and card.type == ATTACK or
                    last_played_by_opponent and (
                        last_played_by_opponent.type == ATTACK and card.type == DEFENSE or
                        last_played_by_opponent.type == DEFENSE and card.type == ATTACK
                    )
                )
            ): playables.add(card)
        playables.add(None)
        return list(playables)

    def get_score_and_next(self, card_to_play, last_played_by_opponent):
        # if the initiative is conceded, should stop generating
        if card_to_play is None and (last_played_by_opponent is None or last_played_by_opponent.type == DEFENSE):
            return 0, STOP
        # if player has the initiative, just go on
        elif (last_played_by_opponent is None or
                last_played_by_opponent.type == DEFENSE):
            return 0, OPPONENT
        # if player is threatened
        elif last_played_by_opponent.type == ATTACK:
            # if player does not respond, opponent scores
            if card_to_play is None:
                return -last_played_by_opponent.power, OPPONENT
            # if player responds with a >= defense, block and play
            elif card_to_play.power >= last_played_by_opponent.power:
                return 0, PLAYER
            # if player responds with a < defense, block and go on
            else: return 0, OPPONENT

    def play(self, card_to_play):
        if card_to_play is not None:
            self.hand.cards.remove(card_to_play)
        self.played.append(card_to_play)

    def revert(self):
        if len(self.played) > 0:
            card_to_revert = self.played.pop()
            if card_to_revert is not None:
                self.hand.cards.append(card_to_revert)


def main():
    home_deck_dict = get_deck_dict(sys.argv[1])
    away_deck_dict = get_deck_dict(sys.argv[2])

    # initialize counters
    bouts_won, bouts_won_score = 0, 0
    bouts_lost, bouts_lost_score = 0, 0
    bouts_tied = 0
    combo_hist = defaultdict(lambda: 0)
    
    # loop for hand draw samples
    samples = []
    for _ in range(ITERATIONS):
        home_deck = Deck(home_deck_dict)
        away_deck = Deck(away_deck_dict)
        home_hand, away_hand = Hand(), Hand()
        for _ in range(CARDS_IN_HAND):
            home_hand.add(home_deck.draw())
            away_hand.add(away_deck.draw())
        home_player = Player(home_hand)
        away_player = Player(away_hand)

        # begin experiment
        bout = get_best_bout(home_player, away_player, 'home', True)
        
        # print result
        combination = [x if x is not None else Card() for x in bout['combination']]
        print '======================================='
        print Hand(combination)
        print zip(bout['turn_sequence'], bout['score_sequence'])
        print 'final score:', bout['score']
        print '======================================='

        # get stats
        if bout['score'] == 0:
            bouts_tied += 1
        elif bout['score'] < 0:
            bouts_lost += 1
            bouts_lost_score += -bout['score']
        elif bout['score'] > 0:
            bouts_won += 1
            bouts_won_score += bout['score']

        combo_hist[str(Hand(combination))] += 1

    combo_freq_pairs = combo_hist.items()
    combo_freq_pairs.sort(key=lambda x: -x[1])
    for i in range(10):
        combo, freq = combo_freq_pairs[i]
        print '++++++++++++++++++++++++++++++++++++++++++++'
        print combo
        print freq
        print '++++++++++++++++++++++++++++++++++++++++++++'

    print 'bouts won', bouts_won, float(bouts_won_score) / bouts_won
    print 'bouts tied', bouts_tied
    print 'bouts lost', bouts_lost, float(bouts_lost_score) / bouts_lost


def get_deck_dict(file_name):
    deck_json = open(file_name).read()
    return json.loads(deck_json)


def get_best_bout(player, opponent, turn, initial=False):
    bouts = []
    playables = player.get_playables(opponent.last_played())

    for playable in playables:
        player.play(playable)
        outcome_score, next_turn = player.get_score_and_next(playable, opponent.last_played())
        if next_turn == STOP:
            bouts.append({
                'combination': [playable],
                'score_sequence': [outcome_score],
                'score': outcome_score,
                'turn_sequence': [turn],
            })
        elif next_turn == OPPONENT:
            other_turn = 'home' if turn == 'away' else 'away'
            bout = get_best_bout(opponent, player, other_turn)
            bouts.append({
                'combination': [playable] + bout['combination'],
                'score_sequence': [outcome_score] + bout['score_sequence'],
                'score': outcome_score - bout['score'],
                'turn_sequence': [turn] + bout['turn_sequence'],
            })
        elif next_turn == PLAYER:
            opponent.play(None)
            bout = get_best_bout(player, opponent, turn)
            bouts.append({
                'combination': [playable] + bout['combination'],
                'score_sequence': [outcome_score] + bout['score_sequence'],
                'score': outcome_score + bout['score'],
                'turn_sequence': [turn] + bout['turn_sequence'],
            })
            opponent.revert()
        player.revert()

    max_bout = None
    for bout in bouts:
        if (max_bout is None or
            max_bout['combination'] == [None] or
            bout['combination'] != [None] and bout['score'] > max_bout['score']):
            max_bout = bout
    return max_bout


if __name__ == '__main__':
    main()
