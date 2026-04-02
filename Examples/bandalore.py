"""Bandalore deck definition using the Cardmaker framework.

The Bandalore deck consists of 60 cards in two card types:
  - PipCards: ranks 1-10 in three suits (30 cards)
  - FaceCards: ranks 1-5 in three suits, two spins (30 cards)

Shared States:
  - Suits: O, G, P
  - PipRanks: 1-10
  - FaceRanks: 1-5
  - Spins: ↑, ↓

Shared Relationships:
  - KinPips: maps each face rank to its two kin pip ranks (r and 11-r)
"""

from cardmaker import State, Relationship, Card, Deck


# ---------------------------------------------------------------------------
# States
# ---------------------------------------------------------------------------

suits_state = State('Suits', ['O', 'G', 'P'])
pip_ranks_state = State('PipRanks', list(range(1, 11)))
face_ranks_state = State('FaceRanks', list(range(1, 6)))
spins_state = State('Spins', ['↑', '↓'])


# ---------------------------------------------------------------------------
# Relationships
# ---------------------------------------------------------------------------

# KinPips: face rank r is kin to pip ranks r and (11 - r)
# e.g. face rank 3 -> pip ranks (3, 8)
kin_pips = Relationship(
    name='KinPips',
    input_states=[face_ranks_state],
    output_states=[pip_ranks_state],
    mapping=lambda r: (r, 11 - r)
)


# ---------------------------------------------------------------------------
# Card generation
# ---------------------------------------------------------------------------

def make_pip_card(suit, rank):
    """Create a PipCard with the given suit and rank."""
    return Card(
        name=f'{suit}{rank}',
        attributes={
            suits_state: suit,
            pip_ranks_state: rank,
        }
    )


def make_face_card(suit, rank, spin):
    """Create a FaceCard with the given suit, rank, and spin."""
    return Card(
        name=f'{suit} {spin}{rank}{spin}',
        attributes={
            suits_state: suit,
            face_ranks_state: rank,
            spins_state: spin,
        },
        relationships=[kin_pips]
    )


# ---------------------------------------------------------------------------
# Deck assembly
# ---------------------------------------------------------------------------

bandalore = Deck('Bandalore')

# Generate and add PipCards (3 suits × 10 ranks = 30 cards)
bandalore.add_cards([
    make_pip_card(suit, rank)
    for suit in suits_state.values
    for rank in pip_ranks_state.values
])

# Generate and add FaceCards (3 suits × 5 ranks × 2 spins = 30 cards)
bandalore.add_cards([
    make_face_card(suit, rank, spin)
    for suit in suits_state.values
    for rank in face_ranks_state.values
    for spin in spins_state.values
])

# Infer shared States and Relationships from cards
bandalore.build()
