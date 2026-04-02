"""Decktet deck definition using the Cardmaker framework.

The Decktet is a 45-card deck (basic + extended) with six suits and ten ranks.

Basic deck (36 cards):
  - Aces (6):          single-suited, one per suit
  - Number cards (24): double-suited, ranks 2-9, three cards per rank
  - Crowns (6):        single-suited, one per suit

Extended deck (9 cards):
  - Excuse (1): no suit, no rank
  - Pawns (4):  triple-suited, rank between 9 and Crown
  - Courts (4): triple-suited, rank between Pawn and Crown

Shared States:
  - Suits:  Moons, Suns, Waves, Leaves, Wyrms, Knots
  - Ranks:  Ace, 2-9, Pawn, Court, Crown
  - Suit1, Suit2, Suit3: suit slot States (all share the same values as Suits)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cardmaker import State, Card, Deck  # noqa: E402


# ---------------------------------------------------------------------------
# States
# ---------------------------------------------------------------------------

SUIT_VALUES = ['Moons', 'Suns', 'Waves', 'Leaves', 'Wyrms', 'Knots']
RANK_VALUES = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 'Pawn', 'Court', 'Crown']

suits_state = State('Suits', SUIT_VALUES)
ranks_state = State('Ranks', RANK_VALUES)

# Separate suit slot States for multi-suited cards
suit_1_state = State('Suit1', SUIT_VALUES)
suit_2_state = State('Suit2', SUIT_VALUES)
suit_3_state = State('Suit3', SUIT_VALUES)  # Pawns and Courts only


# ---------------------------------------------------------------------------
# Card definitions
# ---------------------------------------------------------------------------

# -- Aces (single-suited) ---------------------------------------------------
aces = [
    Card('Ace of Moons', attributes={ranks_state: 'Ace', suit_1_state: 'Moons'}),
    Card('Ace of Suns', attributes={ranks_state: 'Ace', suit_1_state: 'Suns'}),
    Card('Ace of Waves', attributes={ranks_state: 'Ace', suit_1_state: 'Waves'}),
    Card('Ace of Leaves', attributes={ranks_state: 'Ace', suit_1_state: 'Leaves'}),
    Card('Ace of Wyrms', attributes={ranks_state: 'Ace', suit_1_state: 'Wyrms'}),
    Card('Ace of Knots', attributes={ranks_state: 'Ace', suit_1_state: 'Knots'}),
]

# -- Number cards (double-suited) -------------------------------------------
# Suit combinations sourced from the official Decktet charts
number_cards = [
    # Rank 2
    Card('the Author', attributes={ranks_state: 2, suit_1_state: 'Moons', suit_2_state: 'Knots'}),
    Card('the Desert', attributes={ranks_state: 2, suit_1_state: 'Suns', suit_2_state: 'Wyrms'}),
    Card('the Origin', attributes={ranks_state: 2, suit_1_state: 'Waves', suit_2_state: 'Leaves'}),
    # Rank 3
    Card('the Painter', attributes={ranks_state: 3, suit_1_state: 'Moons', suit_2_state: 'Waves'}),
    Card('the Journey', attributes={ranks_state: 3, suit_1_state: 'Suns', suit_2_state: 'Knots'}),
    Card('the Savage', attributes={ranks_state: 3, suit_1_state: 'Leaves', suit_2_state: 'Wyrms'}),
    # Rank 4
    Card('the Mountain', attributes={ranks_state: 4, suit_1_state: 'Moons', suit_2_state: 'Suns'}),
    Card('the Sailor', attributes={ranks_state: 4, suit_1_state: 'Waves', suit_2_state: 'Leaves'}),
    Card('the Battle', attributes={ranks_state: 4, suit_1_state: 'Wyrms', suit_2_state: 'Knots'}),
    # Rank 5
    Card('the Forest', attributes={ranks_state: 5, suit_1_state: 'Moons', suit_2_state: 'Leaves'}),
    Card('the Discovery', attributes={ranks_state: 5, suit_1_state: 'Suns', suit_2_state: 'Waves'}),
    Card('the Soldier', attributes={ranks_state: 5, suit_1_state: 'Wyrms', suit_2_state: 'Knots'}),
    # Rank 6
    Card('the Lunatic', attributes={ranks_state: 6, suit_1_state: 'Moons', suit_2_state: 'Waves'}),
    Card('the Serpent', attributes={ranks_state: 6, suit_1_state: 'Suns', suit_2_state: 'Wyrms'}),
    Card('the Market', attributes={ranks_state: 6, suit_1_state: 'Leaves', suit_2_state: 'Knots'}),
    # Rank 7
    Card('the Chance Meeting', attributes={ranks_state: 7, suit_1_state: 'Moons', suit_2_state: 'Leaves'}),
    Card('the Castle', attributes={ranks_state: 7, suit_1_state: 'Suns', suit_2_state: 'Knots'}),
    Card('the Cave', attributes={ranks_state: 7, suit_1_state: 'Waves', suit_2_state: 'Wyrms'}),
    # Rank 8
    Card('the Diplomat', attributes={ranks_state: 8, suit_1_state: 'Moons', suit_2_state: 'Suns'}),
    Card('the Mill', attributes={ranks_state: 8, suit_1_state: 'Waves', suit_2_state: 'Leaves'}),
    Card('the Betrayal', attributes={ranks_state: 8, suit_1_state: 'Wyrms', suit_2_state: 'Knots'}),
    # Rank 9
    Card('the Pact', attributes={ranks_state: 9, suit_1_state: 'Moons', suit_2_state: 'Suns'}),
    Card('the Darkness', attributes={ranks_state: 9, suit_1_state: 'Waves', suit_2_state: 'Wyrms'}),
    Card('the Merchant', attributes={ranks_state: 9, suit_1_state: 'Leaves', suit_2_state: 'Knots'}),
]

# -- Crowns (single-suited) -------------------------------------------------
crowns = [
    Card('the Huntress', attributes={ranks_state: 'Crown', suit_1_state: 'Moons'}),
    Card('the Bard', attributes={ranks_state: 'Crown', suit_1_state: 'Suns'}),
    Card('the Sea', attributes={ranks_state: 'Crown', suit_1_state: 'Waves'}),
    Card('the End', attributes={ranks_state: 'Crown', suit_1_state: 'Leaves'}),
    Card('the Calamity', attributes={ranks_state: 'Crown', suit_1_state: 'Wyrms'}),
    Card('the Windfall', attributes={ranks_state: 'Crown', suit_1_state: 'Knots'}),
]

# -- Extended: Excuse (no suit, no rank) ------------------------------------
excuse = Card('the Excuse', attributes={})

# -- Extended: Pawns (triple-suited) ----------------------------------------
pawns = [
    Card('the Harvest', attributes={ranks_state: 'Pawn', suit_1_state: 'Moons', suit_2_state: 'Suns', suit_3_state: 'Leaves'}),
    Card('the Light Keeper', attributes={ranks_state: 'Pawn', suit_1_state: 'Suns', suit_2_state: 'Waves', suit_3_state: 'Knots'}),
    Card('the Watchman', attributes={ranks_state: 'Pawn', suit_1_state: 'Moons', suit_2_state: 'Wyrms', suit_3_state: 'Knots'}),
    Card('the Borderland', attributes={ranks_state: 'Pawn', suit_1_state: 'Waves', suit_2_state: 'Leaves', suit_3_state: 'Wyrms'}),
]

# -- Extended: Courts (triple-suited) ---------------------------------------
courts = [
    Card('the Consul', attributes={ranks_state: 'Court', suit_1_state: 'Moons', suit_2_state: 'Waves', suit_3_state: 'Knots'}),
    Card('the Rite', attributes={ranks_state: 'Court', suit_1_state: 'Moons', suit_2_state: 'Leaves', suit_3_state: 'Wyrms'}),
    Card('the Island', attributes={ranks_state: 'Court', suit_1_state: 'Suns', suit_2_state: 'Waves', suit_3_state: 'Wyrms'}),
    Card('the Window', attributes={ranks_state: 'Court', suit_1_state: 'Suns', suit_2_state: 'Leaves', suit_3_state: 'Knots'}),
]


# ---------------------------------------------------------------------------
# Deck assembly
# ---------------------------------------------------------------------------

decktet = Deck('Decktet')

decktet.add_cards(aces)
decktet.add_cards(number_cards)
decktet.add_cards(crowns)
decktet.add_card(excuse)
decktet.add_cards(pawns)
decktet.add_cards(courts)

decktet.build()
