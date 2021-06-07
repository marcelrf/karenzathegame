
from ktg.card import *
from ktg.deck import Deck
from ktg.player import PlayerState
from ktg.game import INITIAL_CARDS_IN_HAND
from itertools import chain
from copy import copy


def equip_readiness(technique):
    technique_copy = copy(technique)
    technique_copy.strike_resolution["auto_reguard"] = True
    return technique_copy


def equip_disarm(technique):
    technique_copy = copy(technique)
    technique_copy.strike_resolution["counter_opponents_equipments"] = True
    return technique_copy


def apply_effects_reset(game):
    current = game.current_player()
    current.reguard()
    other = game.other_player()
    other.reguard()


def equip_camera_flash(technique):
    technique_copy = copy(technique)
    if "opponents_power_increment" not in technique_copy.strike_resolution:
        technique_copy.strike_resolution["opponents_power_increment"] = 0
    technique_copy.strike_resolution["opponents_power_increment"] += -3
    return technique_copy


deck = Deck(
    'Kitty',
    list(chain(
        Card.new_technique(
            name="Take that!",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.HIT,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=1
        ) * 2,
        Card.new_technique(
            name="Crouching tiger",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=2
        ) * 2,
        Card.new_technique(
            name="NSFL",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.THRUST,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=3
        ) * 2,
        Card.new_technique(
            name="CUL8R",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=4
        ) * 2,
        Card.new_technique(
            name="Tiger claw",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.THRUST,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=4
        ) * 2,
        Card.new_technique(
            name="FTW",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.TOP_LEFT],
            power=5
        ) * 2,
        Card.new_technique(
            name="Talk to the claw",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=1
        ) * 2,
        Card.new_technique(
            name="AFK",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.BOTTOM_LEFT],
            trajectory_ends=[SwordPosition.TOP_LEFT],
            power=2
        ) * 2,
        Card.new_technique(
            name="Wait for it...",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.BOTTOM_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=3
        ) * 2,
        Card.new_technique(
            name="NP",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=4
        ) * 2,
        Card.new_technique(
            name="Roooaarrrrr!",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.ABSORB,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=4
        ) * 2,
        Card.new_technique(
            name="Cat stance",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.TOP_LEFT],
            power=5
        ) * 2,
        Card.new_ability(
            name="Readiness",
            type=AbilityType.EQUIPMENT,
            text="Equip a technique card. After strike resolution automatically reguard.",
            can_equip=lambda t: True,
            equip=equip_readiness
        ) * 2,
        Card.new_ability(
            name="Reset",
            type=AbilityType.INSTANT,
            text="Play if you are threatened. Ignore your opponent's attack. Both players reguard. Your opponent plays next turn.",
            can_be_played=lambda g: g.current_player_state() == PlayerState.THREATENED,
            apply_effects=apply_effects_reset
        ) * 2,
        Card.new_ability(
            name="Disarm",
            type=AbilityType.EQUIPMENT,
            text="Equip a technique card. At strike resolution, equipments from your opponent have no effect.",
            can_equip=lambda t: True,
            equip=equip_disarm
        ) * 2,
        Card.new_ability(
            name="Camera flash",
            type=AbilityType.EQUIPMENT,
            text="Equip a technique card. At strike resolution, reduces the opponent's technique power by 3.",
            can_equip=lambda t: True,
            equip=equip_camera_flash
        ) * 2
    ))
)
