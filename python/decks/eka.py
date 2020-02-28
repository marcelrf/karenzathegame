
# https://afternoon-ridge-11972.herokuapp.com/decks/eka

from ktg.card import *
from ktg.deck import Deck
from ktg.player import PlayerState
from itertools import chain
from copy import copy


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
            name="Caveman",
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
            power=1
        ) * 2,
        Card.new_ability(
            name="Zone out",
            type=AbilityType.EQUIPMENT,
            text="Equip a defense card. Increase its power by 2.",
            requirements=lambda t: t.technique_type == TechniqueType.DEFENSE,
            effects={
                "strike_resolution": {
                    "opponents_power_increase": -2
                }
            }
        ) * 2,
        Card.new_ability(
            name="Flick of the wrist",
            type=AbilityType.EQUIPMENT,
            text="Equip a technique card. Increase its power by 1.",
            requirements=lambda t: True,
            effects={
                "strike_resolution": {
                    "power_increase": +1
                }
            }
        ) * 2,
        Card.new_ability(
            name="Torque",
            type=AbilityType.EQUIPMENT,
            text="Equip an attack card. Increase its power by 2.",
            requirements=lambda t: t.technique_type == TechniqueType.ATTACK,
            effects={
                "strike_resolution": {
                    "power_increase": +2
                }
            }
        ) * 2,
        Card.new_ability(
            name="Invite",
            type=AbilityType.STANDALONE,
            text="Play only if you are not threatened. If your opponent has playable attacks, they must attack next turn.",
            requirements=lambda g: g.current_player_state() == PlayerState.INITIATIVE,
            effects={
                "opponents_next_turn": {
                    "must_attack": True
                }
            }
        ) * 2
    ))
)
