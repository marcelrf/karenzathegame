# coding: utf-8

from enum import Enum
from copy import copy


class CardType(Enum):
    TECHNIQUE = 1
    ABILITY = 2


class TechniqueType(Enum):
    ATTACK = 1
    DEFENSE = 2
    NEUTRAL = 3


class TechniqueSubtype(Enum):
    SLASH = 1
    THRUST = 2
    HIT = 3
    DEFLECT = 4
    ABSORB = 5
    SHIELD = 6
    OTHER = 7


class AbilityType(Enum):
    EQUIPMENT = 1
    STANDALONE = 2
    INSTANT = 3


class SwordPosition(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4


class Card(object):

    @classmethod
    def new_technique(cls,
        name,
        type,
        subtype,
        trajectory_starts,
        trajectory_ends,
        power,
        image=None,
        text=None,
        can_be_chained=None,
        strike_resolution=None,
        apply_effects=None
    ):
        if type not in TechniqueType:
            raise Exception('Invalid technique type.')
        if subtype is not None and subtype not in TechniqueSubtype:
            raise Exception('Invalid technique subtype.')
        if len(set(trajectory_starts)) != len(trajectory_starts):
            raise Exception('Trajectory starts has duplicates.')
        if len(set(trajectory_ends)) != len(trajectory_ends):
            raise Exception('Trajectory ends has duplicates.')
        if set(trajectory_starts).intersection(set(trajectory_ends)):
            raise Exception('Trajectory starts and ends intersect.')
        if power < 0 or power > 9:
            raise Exception('Power outside of range 0-9.')
        return Card(
            name,
            CardType.TECHNIQUE,
            type,
            subtype,
            None,
            sorted(trajectory_starts),
            sorted(trajectory_ends),
            power,
            image,
            text,
            None,
            None,
            strike_resolution,
            can_be_chained,
            None,
            None,
            None,
            apply_effects
        )

    @classmethod
    def new_ability(cls,
        name,
        type,
        image=None,
        text=None,
        can_equip=None,
        equip=None,
        strike_resolution=None,
        can_be_chained=None,
        discard_requirement=None,
        materialize_technique=None,
        can_be_played=None,
        apply_effects=None
    ):
        if type not in AbilityType:
            raise Exception('Invalid ability type.')
        return Card(
            name,
            CardType.ABILITY,
            None,
            None,
            type,
            None,
            None,
            None,
            image,
            text,
            can_equip,
            equip,
            strike_resolution,
            can_be_chained,
            discard_requirement,
            materialize_technique,
            can_be_played,
            apply_effects
        )

    def __init__(self,
        name,
        card_type,
        technique_type,
        technique_subtype,
        ability_type,
        trajectory_starts,
        trajectory_ends,
        power,
        image,
        text,
        can_equip,
        equip,
        strike_resolution,
        can_be_chained,
        discard_requirement,
        materialize_technique,
        can_be_played,
        apply_effects
    ):
        self.name = name
        self.card_type = card_type
        self.technique_type = technique_type
        self.technique_subtype = technique_subtype
        self.ability_type = ability_type
        self.trajectory_starts = trajectory_starts
        self.trajectory_ends = trajectory_ends
        self.power = power
        self.image = image
        self.text = text
        self.can_equip = can_equip or default_can_equip
        self.equip = equip or default_equip
        self.strike_resolution = strike_resolution or {}
        self.can_be_chained = can_be_chained or self.default_can_be_chained
        self.discard_requirement = discard_requirement or 0
        self.materialize_technique = materialize_technique or (lambda g: None)
        self.can_be_played = can_be_played or (lambda g: False)
        self.apply_effects = apply_effects or (lambda g: None)

    def __copy__(self):
        return Card(
            self.name,
            self.card_type,
            self.technique_type,
            self.technique_subtype,
            self.ability_type,
            copy(self.trajectory_starts),
            copy(self.trajectory_ends),
            self.power,
            self.image,
            self.text,
            self.can_equip,
            self.equip,
            copy(self.strike_resolution),
            self.can_be_chained,
            self.discard_requirement,
            self.materialize_technique,
            self.can_be_played,
            self.apply_effects
        )

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.card_type == other.card_type and
            self.technique_type == other.technique_type and
            self.technique_subtype == other.technique_subtype and
            self.ability_type == other.ability_type and
            self.trajectory_starts == other.trajectory_starts and
            self.trajectory_ends == other.trajectory_ends and
            self.power == other.power and
            self.image == other.image and
            self.text == other.text and
            self.can_equip == other.can_equip and
            self.equip == other.equip and
            self.strike_resolution == other.strike_resolution and
            self.can_be_chained == other.can_be_chained and
            self.discard_requirement == other.discard_requirement and
            self.materialize_technique == other.materialize_technique and
            self.can_be_played == other.can_be_played and
            self.apply_effects == other.apply_effects
        )

    def __mul__(self, factor):
        return [copy(self) for i in range(factor)]

    def __str__(self):
        normalize = lambda s, l: s + ' ' * (l - len(s)) if len(s) < l else s[0:l]
        text  = '.-------------.\n'
        if self.card_type == CardType.TECHNIQUE:
            type_symbol = 'A' if self.technique_type == TechniqueType.ATTACK else 'D'
            text += '| ' + type_symbol + ' (' + normalize(str(self.power) + ')', 8) + ' |\n'
        else:
            text += '| S           |\n'
        text += '|             |\n'
        if self.card_type == CardType.TECHNIQUE:
            symbol = lambda p: 'o' if p in self.trajectory_starts else ('x' if p in self.trajectory_ends else '·')
            text += '|   %s     %s   |\n' % (symbol(SwordPosition.TOP_LEFT), symbol(SwordPosition.TOP_RIGHT))
            text += '|             |\n'
            text += '|   %s     %s   |\n' % (symbol(SwordPosition.BOTTOM_LEFT), symbol(SwordPosition.BOTTOM_RIGHT))
        elif self.card_type == CardType.ABILITY:
            card_text = normalize(self.text, 33)
            text += '| %s |\n' % card_text[0:11]
            text += '| %s |\n' % card_text[11:22]
            text += '| %s |\n' % card_text[22:33]
        text += '|             |\n'
        text += '|-------------|\n'
        text += '| ' + normalize(self.name, 11) + ' |\n'
        text += '\'-------------\''
        return text

    @classmethod
    def reverse_str(cls, name=''):
        normalize = lambda s, l: s + ' ' * (l - len(s)) if len(s) < l else s[0:l]
        text  = '.-------------.\n'
        text += '| %s |\n' % normalize(name, 11)
        for i in range(7):
            text += '|             |\n'
        text += '\'-------------\''
        return text

    def default_can_be_chained(self, technique):
        if len(technique.trajectory_ends) == 0:
            return True
        for start in self.trajectory_starts:
            if start in technique.trajectory_ends:
                return True
        return False

def default_can_equip(technique):
    return False

def default_equip(technique):
    return copy(technique)
