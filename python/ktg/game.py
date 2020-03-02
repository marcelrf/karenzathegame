# coding: utf-8

from enum import Enum
from ktg.player import Player, PlayerState
from ktg.card import CardType, TechniqueType
from ktg.move import Move, MoveType
from copy import copy


class Turn(Enum):
    PLAYER_1 = 1
    PLAYER_2 = 2


INITIAL_CARDS_IN_HAND = 7

class Game(object):

    def __init__(self, player_1, player_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.player_1.draw(INITIAL_CARDS_IN_HAND)
        self.player_2.draw(INITIAL_CARDS_IN_HAND)
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

    def current_player_state(self):
        if self.last_move is not None and self.last_move.is_attack():
            return PlayerState.THREATENED
        else:
            return PlayerState.INITIATIVE

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
        standalones = current.hand.standalones()
        valid_moves = []

        # fixed-point algorithm to get all combinations of technique+equipment*
        move_set_1 = []
        move_set_2 = []
        for t in techniques:
            new_move = Move(MoveType.PLAY, t)
            if new_move not in move_set_2:
                move_set_2.append(new_move)
        while len(move_set_2) > 0:
            move_set_3 = []
            for move in move_set_2:
                move_technique = move.main_card
                move_equipments = move.equipments
                equipments_to_try = copy(equipments)
                for e in move_equipments:
                    equipments_to_try.remove(e)
                for e in equipments_to_try:
                    if self.can_equip(move_technique, e):
                        new_move = Move(MoveType.PLAY, move_technique, move_equipments + [e])
                        if new_move not in move_set_3:
                            move_set_3.append(new_move)
            move_set_1 += move_set_2
            move_set_2 = move_set_3

        # check of all which ones can be played
        for move in move_set_1:
            move_technique = move.main_card
            move_equipments = move.equipments
            for e in move_equipments:
                move_technique = self.equip(move_technique, e)
            if self.can_be_played(move_technique):
                valid_moves.append(move)

        # also add standalones
        for s in standalones:
            if self.can_be_played(s):
                valid_moves.append(Move(MoveType.PLAY, s))

        return valid_moves

    def can_equip(self, technique, equipment):
        # TODO add cummulative/only_by_itself field to equipments and take it into account here!
        return equipment.requirements(technique)

    def equip(self, technique, equipment):
        equipped = copy(technique)
        for field in [
            ['strike_resolution','power_increment'],
            ['strike_resolution','opponents_power_increment']]:
            self.increment_field(equipped.effects, field,
                self.get_field(equipment.effects, field))
        for field in [
            ['strike_resolution', 'nothing_happens'],
            ['trajectory_requirement'],
            ['discard_requirement']]:
            self.set_field(equipped.effects, field,
                self.get_field(equipment.effects, field))
        return equipped

    def get_field(self, obj, field):
        for f in field:
            if f in obj: obj = obj[f]
            else: return None
        return obj

    def set_field(self, obj, field, value):
        if value is None: return
        for f in field[0:-1]:
            if f not in obj:
                obj[f] = {}
            obj = obj[f]
        obj[field[-1]] = value

    def increment_field(self, obj, field, value):
        if value is None: return
        init_value = self.get_field(obj, field)
        incr_value = value if init_value is None else init_value + value
        self.set_field(obj, field, incr_value)

    def can_be_played(self, card):
        # TODO introduce abilities (card.effects) that alter can_be_played!
        current_player = self.current_player()
        if card.card_type == CardType.TECHNIQUE:
            if self.current_player_state() == PlayerState.THREATENED and card.technique_type != TechniqueType.DEFENSE:
                return False
            if self.current_player_state() == PlayerState.INITIATIVE and card.technique_type != TechniqueType.ATTACK:
                return False
            if current_player.in_sequence():
                for start in card.trajectory_starts:
                    if start in current_player.sequence_head().trajectory_ends:
                        return True
                return False
        elif card.card_type == CardType.ABILITY:
            return card.requirements(self)
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
