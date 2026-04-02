"""Standard deck of playing cards using the Cardmaker framework.

The standard deck consists of 52 cards:
  - 13 ranks × 4 suits = 52 cards

Shared States:
  - Suits:  ♠, ♥, ♦, ♣
  - Ranks:  A, 2-10, J, Q, K
  - Colors: Red, Black

Shared Relationships:
  - ColorOfSuit: maps each suit to its color

Note: Ace rank and Jokers are intentionally left as game-level decisions.
"""

from cardmaker import State, Relationship, Card, Deck


# ---------------------------------------------------------------------------
# States
# ---------------------------------------------------------------------------

suits_state = State('Suits', ['♠', '♥', '♦', '♣'])
ranks_state = State('Ranks', ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K'])
colors_state = State('Colors', ['Red', 'Black'])


# ---------------------------------------------------------------------------
# Relationships
# ---------------------------------------------------------------------------

# ColorOfSuit: each suit maps to its color
color_of_suit = Relationship(
    name='ColorOfSuit',
    input_states=[suits_state],
    output_states=[colors_state],
    mapping={'♠': 'Black', '♥': 'Red', '♦': 'Red', '♣': 'Black'}
)


# ---------------------------------------------------------------------------
# Card generation
# ---------------------------------------------------------------------------

def make_card(rank, suit):
    """Create a standard playing card with the given rank and suit."""
    return Card(
        name=f'{rank}{suit}',
        attributes={
            ranks_state: rank,
            suits_state: suit,
            colors_state: color_of_suit.lookup(suit),
        }
    )


# ---------------------------------------------------------------------------
# Deck assembly
# ---------------------------------------------------------------------------

standard_deck = Deck('StandardDeck')

# Generate and add all 52 cards (4 suits × 13 ranks)
standard_deck.add_cards([
    make_card(rank, suit)
    for suit in suits_state.values
    for rank in ranks_state.values
])

# Infer shared States and Relationships from cards
standard_deck.build()
