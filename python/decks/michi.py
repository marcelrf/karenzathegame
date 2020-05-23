
# https://afternoon-ridge-11972.herokuapp.com/decks/eka

from ktg.card import *
from ktg.deck import Deck
from ktg.player import PlayerState
from itertools import chain
from copy import copy
from math import ceil


def equip_flow(technique):
    technique_copy = copy(technique)
    technique_copy.can_be_chained = lambda g: True
    return technique_copy

def equip_explode(technique):
    technique_copy = copy(technique)
    if "power_increment" not in technique_copy.strike_resolution:
        technique_copy.strike_resolution["power_increment"] = 0
    technique_copy.strike_resolution["power_increment"] += 2
    technique_copy.discard_requirement += 1
    return technique_copy

def materialize_technique_dodge(game):
    if game.current_player().in_sequence():
        trajectory_ends = game.current_player().sequence_head().materialized.trajectory_ends
    else:
        trajectory_ends = []
    return Card.new_technique(
        name="Dodge",
        type=TechniqueType.DEFENSE,
        subtype=TechniqueSubtype.OTHER,
        trajectory_starts=[],
        trajectory_ends=trajectory_ends,
        power=0,
        can_be_chained=lambda t: True,
        strike_resolution={"nothing_happens": True}
    )

def materialize_technique_blade_push(game):
    if game.current_player().in_sequence():
        trajectory_ends = game.current_player().sequence_head().materialized.trajectory_ends
    else:
        trajectory_ends = []
    can_be_played = (
        game.current_player().in_sequence() and
        game.current_player().sequence_head().main_card.technique_type == TechniqueType.ATTACK
    )
    if can_be_played:
        power = int(ceil(float(game.current_player().sequence_head().main_card.power) / 2))
    else: power = 0
    return Card.new_technique(
        name="Blade push",
        type=TechniqueType.ATTACK if can_be_played else TechniqueType.NEUTRAL,
        subtype=TechniqueSubtype.OTHER,
        trajectory_starts=[],
        trajectory_ends=trajectory_ends,
        power=power,
        can_be_chained=lambda t: can_be_played,
    )


deck = Deck(
    'Michi',
    list(chain(
        Card.new_technique(
            name="Quick blow",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.HIT,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=1
        ) * 2,
        Card.new_technique(
            name="Reverse dragon",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=5
        ) * 2,
        Card.new_technique(
            name="Celestial whip",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.HIT,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=2
        ) * 2,
        Card.new_technique(
            name="Snake",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.BOTTOM_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=3
        ) * 2,
        Card.new_technique(
            name="Planted power",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=6
        ) * 2,
        Card.new_technique(
            name="Side hammer",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.HIT,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=3
        ) * 2,
        Card.new_technique(
            name="Dew drop",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.ABSORB,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=1
        ) * 2,
        Card.new_technique(
            name="Delicate feather",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=6
        ) * 2,
        Card.new_technique(
            name="Twister",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=2
        ) * 2,
        Card.new_technique(
            name="Double twister",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=4
        ) * 2,
        Card.new_technique(
            name="Inner blow",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=5
        ) * 2,
        Card.new_technique(
            name="High wing",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.ABSORB,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.TOP_LEFT],
            power=3
        ) * 2,
        Card.new_ability(
            name="Flow",
            type=AbilityType.EQUIPMENT,
            text="Equip any technique card with power 4 or less. That card can be played regardless of any trajectory requirement.",
            can_equip=lambda t: t.power <= 4,
            equip=equip_flow
        ) * 2,
        Card.new_ability(
            name="Explode",
            type=AbilityType.EQUIPMENT,
            text="Equip a technique card. When you play it, you have to discard 1 card at random. If you can not discard 1 card, you can not play 'Explode'. Increase the technique's power by 2.",
            can_equip=lambda t: True,
            equip=equip_explode
        ) * 2,
        Card.new_ability(
            name="Dodge",
            type=AbilityType.STANDALONE,
            text="Play it like a defense card (regardless of trajectory). Your opponent's attack has no effect and your opponent plays next turn.",
            materialize_technique=materialize_technique_dodge
        ) * 2,
        Card.new_ability(
            name="Blade push",
            type=AbilityType.STANDALONE,
            text="You can play this card if you played an attack on your last turn. This card becomes a copy of that attack, but its power is reduced by half (rounding up).",
            materialize_technique=materialize_technique_blade_push
        ) * 2
    ))
)
