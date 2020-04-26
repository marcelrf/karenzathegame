# coding: utf-8

from enum import Enum
from ktg.player import Player, PlayerState
from ktg.card import CardType, TechniqueType, AbilityType, Card
from ktg.action import Action, ActionType
from ktg.move import Move
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
        self.last_action = None
        self.properties = {}

    def __copy__(self):
        other = Game(
            copy(self.player_1),
            copy(self.player_2),
        )
        other.turn = self.turn
        other.last_action = copy(self.last_action)
        other.properties = copy(self.properties)
        return other

    def __str__(self):
        player_1_text = self.player_1.top_str(self.current_player_state() if self.current_player() == self.player_1 else None)
        separator = '+' * 172
        player_2_text = self.player_2.bottom_str(self.current_player_state() if self.current_player() == self.player_2 else None)
        return ''.join([player_1_text, separator, player_2_text])

    def current_player(self):
        return self.player_1 if self.turn == Turn.PLAYER_1 else self.player_2

    def other_player(self):
        return self.player_2 if self.turn == Turn.PLAYER_1 else self.player_1

    def current_player_state(self):
        if (self.last_action is not None and self.last_action.action_type == ActionType.MOVE and
            self.last_action.move.main_card.ability_type != AbilityType.INSTANT and
            self.last_action.move.materialized.technique_type == TechniqueType.ATTACK):
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
        if self.player_2.touche or (not self.player_1.touche and self.player_1.score > self.player_2.score):
            return self.player_1
        if self.player_1.touche or (not self.player_2.touche and self.player_2.score > self.player_1.score):
            return self.player_2
        return None

    def get_valid_moves(self):
        current = self.current_player()
        techniques = current.hand.techniques()
        equipments = current.hand.equipments()
        standalones = current.hand.standalones()
        instants = current.hand.instants()
        valid_moves = []

        # fixed-point algorithm to get all combinations of technique+equipment*
        move_set_1 = []
        move_set_2 = self.deduplicated([Move(t) for t in techniques])
        while len(move_set_2) > 0:
            move_set_3 = []
            for move in move_set_2:
                move_technique = move.main_card
                move_equipments = move.equipments
                move.materialize(self)
                equipments_to_try = copy(equipments)
                for e in move_equipments:
                    equipments_to_try.remove(e)
                for e in equipments_to_try:
                    if e.can_equip(move.materialized):
                        new_move = Move(move_technique, move_equipments + [e])
                        if new_move not in move_set_3:
                            move_set_3.append(new_move)
            move_set_1 += move_set_2
            move_set_2 = move_set_3

        # check of all which ones can be played
        for move in move_set_1:
            if self.can_be_played(move):
                valid_moves.append(move)

        # also add standalones
        for s in standalones:
            move = Move(s)
            if self.can_be_played(move):
                valid_moves.append(move)

        # also add instants
        if "current_must_attack" not in self.properties:
            for i in instants:
                if i.can_be_played(self):
                    valid_moves.append(Move(i))

        return self.deduplicated(valid_moves)

    def can_be_played(self, move):
        current_player = self.current_player()
        move.materialize(self)
        if move.materialized.discard_requirement + 1 > len(current_player.hand):
            return False
        if move.materialized.card_type == CardType.TECHNIQUE:
            if self.current_player_state() == PlayerState.THREATENED and move.materialized.technique_type != TechniqueType.DEFENSE:
                return False
            if self.current_player_state() == PlayerState.INITIATIVE and move.materialized.technique_type != TechniqueType.ATTACK:
                return False
            if current_player.in_sequence():
                return move.materialized.can_be_chained(current_player.sequence_head().materialized)
        return True

    def play(self, action):
        current_player = self.current_player()
        if action.action_type == ActionType.DRAW:
            current_player.draw()
            self.turn = Turn.PLAYER_1 if self.turn == Turn.PLAYER_2 else Turn.PLAYER_2
        elif action.action_type == ActionType.REGUARD:
            current_player.reguard()
            self.turn = Turn.PLAYER_1 if self.turn == Turn.PLAYER_2 else Turn.PLAYER_2
        elif action.action_type == ActionType.TOUCHE:
            current_player.touche = True
            self.turn = Turn.PLAYER_1 if self.turn == Turn.PLAYER_2 else Turn.PLAYER_2
        else: # ActionType.MOVE
            if action.move.main_card.card_type == CardType.ABILITY and action.move.main_card.ability_type == AbilityType.INSTANT:
                current_player.play_instant(action.move)
                # discard if required
                if action.move.main_card.discard_requirement > 0:
                    current_player.discard_random(action.move.main_card.discard_requirement)
                action.move.main_card.apply_effects(self)
                self.turn = Turn.PLAYER_1 if self.turn == Turn.PLAYER_2 else Turn.PLAYER_2
            else: # regular technique or standalone
                action.move.materialize(self)
                current_player.play(action.move)
                # discard if required
                if action.move.materialized.discard_requirement > 0:
                    current_player.discard_random(action.move.materialized.discard_requirement)
                if self.current_player_state() == PlayerState.THREATENED:
                    self.strike_resolution()
                else:
                    self.turn = Turn.PLAYER_1 if self.turn == Turn.PLAYER_2 else Turn.PLAYER_2
        self.last_action = action
        self.update_properties()

    def can_draw(self, valid_moves):
        valid_attack_moves = [
            move for move in valid_moves
            if move.main_card.ability_type != AbilityType.INSTANT and
            move.materialized.technique_type == TechniqueType.ATTACK
        ]
        return (
            ("current_must_attack" not in self.properties or len(valid_attack_moves) == 0) and
            self.current_player_state() != PlayerState.THREATENED and
            self.current_player().can_draw()
        )

    def can_reguard(self, valid_moves):
        valid_attack_moves = [
            move for move in valid_moves
            if move.main_card.ability_type != AbilityType.INSTANT and
            move.materialized.technique_type == TechniqueType.ATTACK
        ]
        return (
            ("current_must_attack" not in self.properties or len(valid_attack_moves) == 0) and
            self.current_player_state() != PlayerState.THREATENED and
            self.current_player().can_reguard()
        )

    def strike_resolution(self):
        attack = self.other_player().sequence_head().materialized
        defense = self.current_player().sequence_head().materialized
        # resolve abilities
        if "opponents_power_increment" in defense.strike_resolution:
            attack.power += defense.strike_resolution["opponents_power_increment"]
        if "power_increment" in defense.strike_resolution:
            defense.power += defense.strike_resolution["power_increment"]
        if "power_increment" in attack.strike_resolution:
            attack.power += attack.strike_resolution["power_increment"]
        if "nothing_happens" in defense.strike_resolution:
            self.turn = Turn.PLAYER_1 if self.turn == Turn.PLAYER_2 else Turn.PLAYER_2
            return
        # prevent power < 1
        if attack.power < 1: attack.power = 1
        if defense.power < 1: defense.power = 1
        # calculate score and next turn
        if attack.power >= defense.power:
            self.other_player().score += attack.power - defense.power
            self.turn = Turn.PLAYER_1 if self.turn == Turn.PLAYER_2 else Turn.PLAYER_2

    def deduplicated(self, items):
        _deduplicated = []
        for item in items:
            if item not in _deduplicated:
                _deduplicated.append(item)
        return _deduplicated

    def update_properties(self):
        if "current_must_attack" in self.properties:
            del self.properties["current_must_attack"]
        if "opponent_must_attack" in self.properties:
            self.properties["current_must_attack"] = True
            del self.properties["opponent_must_attack"]
