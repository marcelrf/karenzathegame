
# https://afternoon-ridge-11972.herokuapp.com/decks/eka

from ktg.card import *
from ktg.deck import Deck
from ktg.player import PlayerState
from itertools import chain
from copy import copy


def equip_zone_out(technique):
    technique_copy = copy(technique)
    if "opponents_power_increment" not in technique_copy.strike_resolution:
        technique_copy.strike_resolution["opponents_power_increment"] = 0
    technique_copy.strike_resolution["opponents_power_increment"] += -3
    previous_effects = technique_copy.apply_effects
    technique_copy.apply_effects = lambda g: previous_effects(g) or g.current_player().draw()
    return technique_copy

def equip_flick_of_the_wrist(technique):
    technique_copy = copy(technique)
    if "extra_score" not in technique_copy.strike_resolution:
        technique_copy.strike_resolution["extra_score"] = 0
    technique_copy.strike_resolution["extra_score"] += 2
    return technique_copy

def equip_torque(technique):
    technique_copy = copy(technique)
    if "power_increment" not in technique_copy.strike_resolution:
        technique_copy.strike_resolution["power_increment"] = 0
    technique_copy.strike_resolution["power_increment"] += 3
    previous_effects = technique_copy.apply_effects
    technique_copy.apply_effects = lambda g: previous_effects(g) or g.current_player().draw()
    return technique_copy

def apply_effects_invite(game):
    game.properties["opponent_must_attack"] = True


deck = Deck(
    'Eka',
    list(chain(
        Card.new_technique(
            name="Numero uno",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=2
        ) * 2,
        Card.new_technique(
            name="High backhand",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.HIT,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=4
        ) * 2,
        Card.new_technique(
            name="Low horizontal",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=1
        ) * 2,
        Card.new_technique(
            name="Elevator",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.SLASH,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.TOP_LEFT],
            power=3
        ) * 2,
        Card.new_technique(
            name="Cave man",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.HIT,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=6
        ) * 2,
        Card.new_technique(
            name="Upward flip",
            type=TechniqueType.ATTACK,
            subtype=TechniqueSubtype.HIT,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=2
        ) * 2,
        Card.new_technique(
            name="Scissors",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.BOTTOM_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=4
        ) * 2,
        Card.new_technique(
            name="Rainbow",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.BOTTOM_LEFT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=2
        ) * 2,
        Card.new_technique(
            name="Assisted block",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=5
        ) * 2,
        Card.new_technique(
            name="Numero dos",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.TOP_LEFT],
            trajectory_ends=[SwordPosition.BOTTOM_RIGHT],
            power=3
        ) * 2,
        Card.new_technique(
            name="Escudo",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.SHIELD,
            trajectory_starts=[SwordPosition.BOTTOM_RIGHT],
            trajectory_ends=[SwordPosition.TOP_RIGHT],
            power=1
        ) * 2,
        Card.new_technique(
            name="Inside deflection",
            type=TechniqueType.DEFENSE,
            subtype=TechniqueSubtype.DEFLECT,
            trajectory_starts=[SwordPosition.TOP_RIGHT],
            trajectory_ends=[SwordPosition.BOTTOM_LEFT],
            power=2
        ) * 2,
        Card.new_ability(
            name="Zone out",
            type=AbilityType.EQUIPMENT,
            text="Equip a defense card. Decrease the power of the blocked attack by 3. Draw a card.",
            can_equip=lambda t: t.technique_type == TechniqueType.DEFENSE,
            equip=equip_zone_out
        ) * 2,
        Card.new_ability(
            name="Flick of the wrist",
            type=AbilityType.EQUIPMENT,
            text="Equip a defense card. At strike resolution, regardless of its outcome, score 2 points.",
            can_equip=lambda t: t.technique_type == TechniqueType.DEFENSE,
            equip=equip_flick_of_the_wrist
        ) * 2,
        Card.new_ability(
            name="Torque",
            type=AbilityType.EQUIPMENT,
            text="Equip an attack card. Increase its power by 3. Draw a card.",
            can_equip=lambda t: t.technique_type == TechniqueType.ATTACK,
            equip=equip_torque
        ) * 2,
        Card.new_ability(
            name="Invite",
            type=AbilityType.INSTANT,
            text="Play only if you are not threatened. If your opponent has playable attacks, they must attack next turn. If they can not, they skip their turn.",
            can_be_played=lambda g: g.current_player_state() == PlayerState.INITIATIVE,
            apply_effects=apply_effects_invite
        ) * 2
    ))
)
