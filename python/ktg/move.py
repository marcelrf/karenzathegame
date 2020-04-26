# coding: utf-8

from hand import Hand
from copy import copy
from card import CardType


class Move(object):

    def __init__(self,
        main_card,
        equipments=[],
        materialized=None
    ):
        self.main_card = main_card
        self.equipments = equipments
        self.materialized = materialized

    def __copy__(self):
        return Move(
            copy(self.main_card),
            [e for e in self.equipments],
            copy(self.materialized)
        )

    def __eq__(self, other):
        if (self.main_card != other.main_card or
            self.materialized != other.materialized):
            return False
        other_equipments = copy(other.equipments)
        for e in self.equipments:
            if e not in other_equipments:
                return False
            other_equipments.remove(e)
        return len(other_equipments) == 0

    def __len__(self):
        return 1 + len(self.equipments)

    def __str__(self):
        move_cards = Hand()
        move_cards.add(self.main_card)
        for e in self.equipments:
            move_cards.add(e)
        return str(move_cards)

    def name(self):
        return ' + '.join([c.name for c in self.cards()])

    def add_equipment(self, equipment):
        self.equipments.append(equipment)
        self.materialized = None

    def cards(self):
        return [self.main_card] + self.equipments

    def materialize(self, game):
        if self.main_card.card_type == CardType.ABILITY:
            self.materialized = self.main_card.materialize_technique(game)
        else:
            equipped_technique = copy(self.main_card)
            for equipment in self.equipments:
                equipped_technique = equipment.equip(equipped_technique)
            self.materialized = equipped_technique
