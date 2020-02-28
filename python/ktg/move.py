# coding: utf-8

from enum import Enum
from copy import copy


class MoveType(Enum):
    PLAY = 1
    DRAW = 2
    REGUARD = 3


class Move(object):

    def __init__(self,
        move_type,
        technique=None,
        equipments=[],
        replacement=None
    ):
        self.move_type = move_type
        self.technique = technique
        self.equipments = equipments
        self.replacement = replacement
        self.compiled_technique = self._compile_technique()

    def _compile_technique(self):
        if self.technique is not None:
            compiled_technique = self.technique
            for e in self.equipments:
                compiled_technique = e.equip(move_technique)
            return compiled_technique
        else: return None

    def __copy__(self):
        return Move(
            self.move_type,
            copy(self.technique),
            [e for e in self.equipments],
            copy(self.replacement)
        )

    def is_attack(self):
        if self.compiled_technique is not None:
            return self.compiled_technique.technique_type == TechniqueType.ATTACK
        else: return False
