"""Cardmaker framework — core primitives for defining custom card decks."""


class State:
    """A set of values that cards can reference.

    One of the foundational primitives of the Cardmaker framework.
    States are shared across card types within a deck, providing
    a common vocabulary for traits and relationships.

    Example:
        suits = State('Suits', ['♠', '♥', '♦', '♣'])
        ranks = State('Ranks', [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'])
        colors = State('Colors', ['Red', 'Black'])
    """

    def __init__(self, name: str, values: list):
        assert len(values) >= 2, "A State must have at least two values."
        self.name = name
        self.values = values
        self.relationships = {}  # {relationship_name: Relationship}

    def __contains__(self, value):
        return value in self.values

    def __repr__(self):
        return f"State({self.name!r}, {self.values})"


class Relationship:
    """A mapping between values in one or more States.

    Relationships define how values across States connect to each other.
    The mapping can be provided as a dict (lookup table) or a callable
    (formula). If a callable is provided, it is eagerly converted to a
    dict using the input State values at initialization time.

    Note: Multi-input State support (cartesian product) is deferred.
    Currently only single-input States are supported for callable mappings.

    Example:
        # Callable — Blackjack value: each rank maps to its point value
        blackjack_value = Relationship('BlackjackValue', [ranks], [ranks],
                                       mapping=lambda r: 11 if r == 'A' else
                                                        10 if r in ('J', 'Q', 'K') else r)

        # Dict — explicit lookup table for the same relationship
        blackjack_value = Relationship('BlackjackValue', [ranks], [ranks],
                                       mapping={2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7,
                                                8: 8, 9: 9, 10: 10, 'J': 10,
                                                'Q': 10, 'K': 10, 'A': 11})
    """

    def __init__(self, name: str, input_states: list, output_states: list, mapping):
        self.name = name
        self.input_states = input_states
        self.output_states = output_states
        self.mapping = self._build_mapping(mapping)

        # Register this Relationship on all referenced States
        all_states = set(self.input_states + self.output_states)
        for state in all_states:
            state.relationships[self.name] = self

    def _build_mapping(self, mapping) -> dict:
        """Convert a callable mapping to a dict using input State values."""
        if callable(mapping):
            assert len(self.input_states) == 1, \
                "Callable mappings currently only support a single input State."
            return {value: mapping(value) for value in self.input_states[0].values}
        assert isinstance(mapping, dict), \
            "Mapping must be a dict or a callable."
        return mapping

    def lookup(self, value):
        """Look up the related values for a given input value."""
        return self.mapping.get(value)

    def __repr__(self):
        return f"Relationship({self.name!r})"


class Card:
    """A bundle of attributes and Relationships.

    A Card's attributes are stored as a dict mapping State objects to
    values, preserving the link to the shared State for each attribute.
    This allows the simulation engine to reason across card types using
    a common State vocabulary.

    For States where a card holds multiple values (e.g. the Decktet's
    double-suited cards), the value should be a list.

    A Card with no attributes or Relationships is valid
    (e.g. the Excuse in Decktet).

    Example:
        card = Card('A♠', attributes={suits_state: '♠', ranks_state: 'A'})
        card.get(suits_state)  # '♠'
    """

    def __init__(self, name: str, attributes: dict = None, relationships: list = None):
        self.name = name
        self.attributes = attributes if attributes is not None else {}
        self.relationships = relationships if relationships is not None else []

    def get(self, state: State):
        """Return the value for the given State, or None."""
        return self.attributes.get(state)

    def __repr__(self):
        attrs = {s.name: v for s, v in self.attributes.items()}
        return f"Card({self.name!r}, {attrs})"


class Deck:
    """A collection of Cards built from shared States and Relationships.

    The Deck acts as the top-level container for a card deck definition.
    Rather than manually registering States and Relationships, call
    build() after adding all cards to infer them automatically from
    the cards in the deck.
    """

    def __init__(self, name: str):
        self.name = name
        self.states = {}        # {name: State}
        self.relationships = {} # {name: Relationship}
        self.cards = []         # [Card]

    def add_card(self, card: Card):
        """Add a single Card to the deck."""
        self.cards.append(card)

    def add_cards(self, cards: list):
        """Add multiple Cards to the deck."""
        self.cards.extend(cards)

    def build(self):
        """Infer shared States and Relationships from the cards in the deck."""
        for card in self.cards:
            for state in card.attributes:
                self.states[state.name] = state
            for rel in card.relationships:
                self.relationships[rel.name] = rel

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __repr__(self):
        return f"Deck({self.name!r}, {len(self)} cards)"
