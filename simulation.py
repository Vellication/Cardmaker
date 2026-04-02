"""Simulation tools for Cardmaker decks.

Tools for sampling hands, running trials, and aggregating results.
These functions are deck-agnostic and work with any deck built using
the Cardmaker framework.

Functions are organized into two categories:
  - Sampling:     drawing cards from a deck
  - Simulation:   running repeated trials and aggregating results
"""

import random
from cardmaker import Deck, Card


# ---------------------------------------------------------------------------
# Sampling
# ---------------------------------------------------------------------------

def draw(deck: Deck, n: int) -> list:
    """Draw n cards at random from the deck without replacement.

    Returns a list of n Card objects. Does not modify the deck.

    Example:
        hand = draw(bandalore, 3)
    """
    return random.sample(deck.cards, n)


def draw_split(deck: Deck, hand_size: int, river_size: int) -> tuple:
    """Draw a hand and a river from the deck without replacement.

    Returns (hand, river) as two separate lists.

    Example:
        hand, river = draw_split(bandalore, 3, 5)
    """
    sample = random.sample(deck.cards, hand_size + river_size)
    return sample[:hand_size], sample[hand_size:]


def draw_multiple(deck: Deck, n: int, count: int) -> list:
    """Draw multiple independent hands of n cards each.

    Returns a list of hands (each hand is a list of Cards).
    Each hand is drawn independently — cards may repeat across hands.

    Example:
        hands = draw_multiple(bandalore, 3, 4)  # 4 players, 3 cards each
    """
    return [draw(deck, n) for _ in range(count)]


# ---------------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------------

def simulate(deck: Deck, trial_fn, n_trials: int, **kwargs) -> list:
    """Run a trial function n_trials times and collect results.

    trial_fn receives the deck and any kwargs, and returns a result.
    Results are collected into a list.

    Example:
        def my_trial(deck):
            hand = draw(deck, 3)
            return shares_value(hand, suits_state)

        results = simulate(bandalore, my_trial, 10000)
        win_rate = sum(results) / len(results)
    """
    return [trial_fn(deck, **kwargs) for _ in range(n_trials)]


def distribution(results: list) -> dict:
    """Aggregate a list of results into a frequency distribution.

    Returns a dict mapping each unique result to its count,
    sorted by count descending.

    Example:
        results = simulate(bandalore, my_trial, 10000)
        dist = distribution(results)
        # {'Twain': 4200, 'Flush': 3100, None: 2700}
    """
    counts = {}
    for result in results:
        counts[result] = counts.get(result, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def probability(results: list, value) -> float:
    """Return the fraction of results equal to value.

    Example:
        results = simulate(bandalore, my_trial, 10000)
        probability(results, 'Twain')  # 0.42
    """
    return sum(1 for r in results if r == value) / len(results)


def print_distribution(dist: dict, n_trials: int):
    """Print a formatted frequency distribution table.

    Example:
        results = simulate(bandalore, my_trial, 10000)
        print_distribution(distribution(results), 10000)
    """
    print(f"\n{'Result':<35} {'Count':>8} {'Probability':>12}")
    print("-" * 57)
    for result, count in dist.items():
        prob = count / n_trials
        label = str(result) if result is not None else 'None'
        print(f"{label:<35} {count:>8} {prob:>11.2%}")
