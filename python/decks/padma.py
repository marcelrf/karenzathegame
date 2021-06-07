
from ktg.card import *
from ktg.deck import Deck
from ktg.player import PlayerState
from itertools import chain
from copy import copy


def equip_poison_ivy(technique):
    technique_copy = copy(technique)
    if "opponent_discard" not in technique_copy.strike_resolution:
        technique_copy.strike_resolution["opponent_discard"] = 0
    technique_copy.strike_resolution["opponent_discard"] += 1
    return technique_copy


def apply_effects_insight(game):
    game.current_player().draw(3)


def equip_bark_skin(technique):
    technique_copy = copy(technique)
    technique_copy.strike_resolution["nothing_happens"] = True
    technique_copy.strike_resolution["play_next_turn"] = True
    return technique_copy


def equip_delusion(technique):
    technique_copy = copy(technique)
    technique_copy.strike_resolution["nothing_happens"] = True
    return technique_copy


deck = Deck(
    'Padma',
    list(chain(
        Card.new_technique(
            name="Slap",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.TOP_LEFT],
            power=1
        ) * 2,
        Card.new_technique(
            name="Opening lotus",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=2
        ) * 2,
        Card.new_technique(
            name="Vine attack",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.THRUST,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=2
        ) * 2,
        Card.new_technique(
            name="Hurricane",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.HIT,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=7
        ) * 2,
        Card.new_technique(
            name="Rose sting",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.THRUST,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=4
        ) * 2,
        Card.new_technique(
            name="Growth",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.BOTTOM_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=5
        ) * 2,
        Card.new_technique(
            name="Deflecting petal",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.BOTTOM_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=3
        ) * 2,
        Card.new_technique(
            name="Seeking root",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=1
        ) * 2,
        Card.new_technique(
            name="Flexible shield",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.TOP_LEFT],
            power=1
        ) * 2,
        Card.new_technique(
            name="Sunflower",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.ABSORB,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=2
        ) * 2,
        Card.new_technique(
            name="Vine curtain",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=6
        ) * 2,
        Card.new_technique(
            name="Whip",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.BOTTOM_LEFT],
            trajectory_ends=[SwordPosition.TOP_LEFT],
            power=4
        ) * 2,
        Card.new_ability(
            name="Poison ivy",
            type=AbilityType.EQUIPMENT,
            text="Equip an attack card. After strike resolution randomly discard 1 card from your opponent's hand.",
            can_equip=lambda t: t.technique_type == TechniqueType.ATTACK,
            equip=equip_poison_ivy
        ) * 2,
        Card.new_ability(
            name="Insight",
            type=AbilityType.INSTANT,
            text="Play only if you are not threatened. Draw 3 cards. If you have more than 7 cards after that, choose and discard until you go back to 7.",
            can_be_played=lambda g: g.current_player_state() == PlayerState.INITIATIVE,
            apply_effects=apply_effects_insight
        ) * 2,
        Card.new_ability(
            name="Bark skin",
            type=AbilityType.EQUIPMENT,
            text="Equip a defense card. At strike resolution, the attacking card does not score. Play next turn.",
            can_equip=lambda t: t.technique_type == TechniqueType.DEFENSE,
            equip=equip_bark_skin
        ) * 2,
        Card.new_ability(
            name="Delusion",
            type=AbilityType.EQUIPMENT,
            text="Equip an attack card. If defended, your attack has no effect and you play next turn after strike resolution.",
            can_equip=lambda t: t.technique_type == TechniqueType.ATTACK,
            equip=equip_delusion
        ) * 2
    ))
)
