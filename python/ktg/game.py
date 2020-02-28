# coding: utf-8

from enum import Enum
from ktg.player import Player
from ktg.card import CardType
from ktg.move import Move, MoveType
from copy import copy


class Turn(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2


class Game(object):

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.turn = Turn.PLAYER_1
        self.last_move = None

    def __copy__(self):
        other = Game(
            copy(self.player_1),
            copy(self.player_2),
        )
        other.turn = self.turn
        other.last_move = copy(self.last_move)
        return other

    def current_player(self):
        return self.player_1 if self.turn == Turn.PLAYER_1 else self.player_2

    def other_player(self):
        return self.player_2 if self.turn == Turn.PLAYER_1 else self.player_1

    def current_player_is_threatened(self):
        return self.last_move is not None and self.last_move.is_attack()

    def is_over(self):
        return any([
            (
                player.touche or
                player.score >= 10 or
                not player.can_draw()
            )
            for player in [self.player_1, self.player_2]
        ])

    def winner(self):
        if not self.is_over():
            raise Exception("Game is not over yet.")
        if self.player_2.touche or self.player_1.score > self.player_2.score:
            return self.player_1
        if self.player_1.touche or self.player_2.score > self.player_1.score:
            return self.player_2
        return None

    def get_valid_moves(self):
        current = self.current_player()
        techniques = current.hand.techniques()
        equipments = current.hand.equipments()
        replacements = current.hand.replacements()
        valid_moves = []

        # fixed-point algorithm to get all combinations of technique+equipment*
        prev_move_set = []
        next_move_set = techniques
        while len(next_move_set) > len(prev_move_set):
            prev_move_set = next_move_set
            next_move_set = copy(prev_move_set)
            for move in prev_move_set:
                move_technique = move.technique()
                move_equipments = move.equipments()
                equipments_to_try = copy(equipments)
                for e in move_equipments:
                    equipments_to_try.remove(e)
                for e in equipments_to_try:
                    if e.can_equip(move_technique):
                        next_move_set.append(Move(MoveType.PLAY, move_technique, move_equipments + [e]))

        # check of all which ones can be played
        for move in next_move_set:
            move_technique = move.technique()
            move_equipments = move.equipments()
            for e in move_equipments:
                move_technique = e.equip(move_technique)
            if move_technique.can_be_played(self):
                valid_moves.append(move)

        # also add replacements
        for r in replacements:
            if r.can_be_played(self):
                valid_moves.append(Move(MoveType.PLAY, r))

        return valid_moves

    def can_be_played(self, compiled_technique):
        current_player = self.current_player()
        if self.current_player_is_threatened() and compiled_technique.technique_type != TechniqueType.DEFENSE:
            return False
        if not self.current_player_is_threatened() and compiled_technique.technique_type != TechniqueType.ATTACK:
            return False
        if current_player.in_sequence():
            for start in compiled_technique.trajectory_starts:
                if start in current_player.sequence.head.trajectory_ends():
                    return True
            return False
        return True

    def play(self, move):
        current_player = self.current_player()
        if move.move_type == MoveType.DRAW:
            current_player.draw()
        elif move.move_type == MoveType.REGUARD:
            current_player.reguard()
        else: # PLAY
            current_player.play(move)
            pass
        self.last_move = move
