# coding: utf-8

from enum import Enum
from copy import copy


class ActionType(Enum):
    DRAW = 1
    MOVE = 2
    REGUARD = 3
    PASS = 4
    TOUCHE = 5


class Action(object):

    def __init__(self,
        action_type,
        move=None
    ):
        self.action_type = action_type
        self.move = move

    def __copy__(self):
        return Action(
            self.action_type,
            copy(self.move)
        )

    def __eq__(self, other):
        return (
            self.action_type == other.action_type and
            self.move == other.move
        )

    def __str__(self):
        if self.action_type == ActionType.DRAW:
            return "Draw"
        if self.action_type == ActionType.MOVE:
            return "Move: " + self.move.name()
        if self.action_type == ActionType.REGUARD:
            return "Reguard"
        if self.action_type == ActionType.TOUCHE:
            return "Touche"
        if self.action_type == ActionType.PASS:
            return "Pass"
