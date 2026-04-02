"""Analysis tools for Cardmaker decks.

General-purpose functions for querying cards and decks by State values,
traversing Relationships, and generating combinations. These functions
are deck-agnostic and work with any deck built using the Cardmaker framework.

Functions are organized into four categories:
  - Composition:   questions about the deck as a whole
  - Querying:      filtering cards by State values
  - Relationships: traversing inter-card connections
  - Combinatorics: generating and filtering card combinations

For generating combinations, use itertools.combinations directly.
"""

from itertools import combinations
from cardmaker import State, Relationship, Card, Deck


# ---------------------------------------------------------------------------
# Composition
# ---------------------------------------------------------------------------

def value_counts(deck: Deck, state: State) -> dict:
    """Count how many cards hold each value for a given State.

    Returns a dict mapping each value to its count.

    Example:
        value_counts(bandalore, suits_state)
        # {'O': 20, 'G': 20, 'P': 20}
    """
    counts = {}
    for card in deck.cards:
        value = card.get(state)
        if value is not None:
            counts[value] = counts.get(value, 0) + 1
    return counts


def state_coverage(deck: Deck, state: State) -> float:
    """Return the fraction of cards that have a value for the given State.

    Example:
        state_coverage(decktet, suit_1_state)  # 1.0 (all cards have suit_1)
        state_coverage(decktet, suit_3_state)  # fraction with a third suit
    """
    count = sum(1 for card in deck.cards if card.get(state) is not None)
    return count / len(deck) if deck.cards else 0.0


# ---------------------------------------------------------------------------
# Querying
# ---------------------------------------------------------------------------

def query(cards: list, state: State, value) -> list:
    """Return all cards whose value for the given State matches value.

    Example:
        query(bandalore.cards, suits_state, 'O')
    """
    return [card for card in cards if card.get(state) == value]


def exclude(cards: list, state: State, value) -> list:
    """Return all cards whose value for the given State does not match value.

    Example:
        exclude(bandalore.cards, suits_state, 'O')
    """
    return [card for card in cards if card.get(state) != value]


def has_state(cards: list, state: State) -> list:
    """Return all cards that have any value for the given State.

    Example:
        has_state(decktet.cards, suit_3_state)  # only Pawns and Courts
    """
    return [card for card in cards if card.get(state) is not None]


# ---------------------------------------------------------------------------
# Shared value checks (used in combination evaluation)
# ---------------------------------------------------------------------------

def shares_value(cards: list, state: State) -> bool:
    """Check if all cards share the same value for the given State.

    Example:
        shares_value(hand, suits_state)  # True if all cards share a suit
    """
    values = [card.get(state) for card in cards if card.get(state) is not None]
    return len(set(values)) == 1 if values else False


def get_values(cards: list, state: State) -> list:
    """Return the list of values for the given State across all cards.

    Example:
        get_values(hand, pip_ranks_state)  # [3, 7, 9]
    """
    return [card.get(state) for card in cards if card.get(state) is not None]


# ---------------------------------------------------------------------------
# Relationships
# ---------------------------------------------------------------------------

def related_values(value, relationship: Relationship):
    """Look up the related values for a given input value via a Relationship.

    Example:
        related_values(3, kin_pips)  # (3, 8)
    """
    return relationship.lookup(value)


def related_cards(card: Card, relationship: Relationship, deck: Deck) -> list:
    """Return all cards in the deck related to the given card via a Relationship.

    Looks up the card's value in the relationship's input State, then finds
    all deck cards whose value matches the related output values.

    Example:
        related_cards(face_card, kin_pips, bandalore)
        # returns all pip cards with kin ranks
    """
    if relationship not in card.relationships:
        return []

    input_state = relationship.input_states[0]
    output_state = relationship.output_states[0]
    input_value = card.get(input_state)

    if input_value is None:
        return []

    output_values = relationship.lookup(input_value)
    if output_values is None:
        return []

    # output_values may be a single value or a tuple/list
    if not isinstance(output_values, (list, tuple)):
        output_values = [output_values]

    return [c for c in deck.cards if c.get(output_state) in output_values]


# ---------------------------------------------------------------------------
# Combinatorics
# ---------------------------------------------------------------------------

def filter_combinations(cards: list, n: int, predicate) -> list:
    """Return all n-card combinations that satisfy a predicate function.

    The predicate takes a tuple of cards and returns True/False.

    Example:
        from itertools import combinations
        filter_combinations(bandalore.cards, 3,
                            lambda combo: shares_value(combo, suits_state))
    """
    return [combo for combo in combinations(cards, n) if predicate(combo)]


def count_combinations(cards: list, n: int, predicate) -> int:
    """Count how many n-card combinations satisfy a predicate function.

    More efficient than filter_combinations when you only need the count.

    Example:
        from itertools import combinations
        count_combinations(bandalore.cards, 3,
                           lambda combo: shares_value(combo, suits_state))
    """
    return sum(1 for combo in combinations(cards, n) if predicate(combo))
