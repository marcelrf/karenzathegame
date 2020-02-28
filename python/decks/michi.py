
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
            text="Equip any technique card. That card can be played regardless of any trajectory requirement.",
            requirements=lambda t: True,
            effects={
                "trajectory_requirement": lambda t: True
            }
        ) * 2,
        Card.new_ability(
            name="Dodge",
            type=AbilityType.STANDALONE,
            text="Play it like defense card (regardless of trajectory). Your opponent's attack has no effect and your opponent plays next turn.",
            requirements=lambda g: g.current_player_state() == PlayerState.THREATENED,
            effects={
                "strike_resolution": {
                    "nothing_happens": True
                }
            }
        ) * 2,
        Card.new_ability(
            name="Blade push",
            type=AbilityType.STANDALONE,
            text="You can play this card if the most recent technique in your sequence is an attack. This card becomes a copy of that attack, but its power is reduced by half (rounding down). You can play it regardless of the trajectory requirement.",
            requirements=lambda g: (
                g.current_player().sequence_head() is not None and
                g.current_player().sequence_head().main_card.card_type == CardType.TECHNIQUE and
                g.current_player().sequence_head().main_card.technique_type == TechniqueType.ATTACK
            ),
            effects={
                "materialize_technique": {
                    "technique_type": lambda g: TechniqueType.ATTACK,
                    "technique_subtype": lambda g: TechniqueSubype.HIT,
                    "trajectory_starts": lambda g: g.current_player().sequence_head().main_card.trajectory_ends,
                    "trajectory_ends": lambda g: g.current_player().sequence_head().main_card.trajectory_ends,
                    "power": lambda g: g.current_player().sequence_head().main_card.power / 2
                }
            }
        ) * 2,
        Card.new_ability(
            name="Explode",
            type=AbilityType.EQUIPMENT,
            text="Equip a technique card. When you play it, you have to discard 1 card at random. If you can not discard 1 card, you can not play 'Explode'. Increase the technique's power by 3.",
            requirements=lambda t: True,
            effects={
                "discards_required": +1,
                "strike_resolution": {
                    "power_increase": +3
                }
            }
        ) * 2
    ))
)
