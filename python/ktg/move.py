# coding: utf-8

from hand import Hand
from enum import Enum
from card import Card
from copy import copy


class MoveType(Enum):
    PLAY = 1
    DRAW = 2
    REGUARD = 3


class Move(object):

    def __init__(self,
        move_type,
        main_card=None,
        equipments=[]
    ):
        self.move_type = move_type
        self.main_card = main_card
        self.equipments = equipments

    def __copy__(self):
        return Move(
            self.move_type,
            copy(self.main_card),
            [e for e in self.equipments]
        )

    def __eq__(self, other):
        other_equipments = copy(other.equipments)
        if (self.move_type != other.move_type or
            self.main_card != other.main_card or
            len(self.equipments) != len(other_equipments)):
            return False
        for e in self.equipments:
            if e not in other_equipments:
                return False
            other_equipments.remove(e)
        return len(other_equipments) == 0

    def __str__(self):
        if self.move_type == MoveType.PLAY:
            move_cards = Hand()
            move_cards.add(self.main_card)
            for e in self.equipments:
                move_cards.add(e)
            return str(move_cards)
        elif self.move_type == MoveType.DRAW:
            return Card.reverse_str('DRAW')
        elif self.move_type == MoveType.REGUARD:
            return Card.reverse_str('REGUARD')
