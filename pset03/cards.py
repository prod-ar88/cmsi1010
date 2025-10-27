from dataclasses import dataclass
from random import shuffle


@dataclass(frozen=True)
class Card:
    suit: str
    rank: int

    def __post_init__(self):
        if self.suit not in ("S", "H", "D", "C"):
            raise ValueError("suit must be one of 'S', 'H', 'D', 'C'")
        if self.rank not in range(1, 14):
            raise ValueError("rank must be an integer between 1 and 13")

    def __str__(self):
        suit_str = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}[self.suit]
        rank_str = {1: "A", 11: "J", 12: "Q", 13: "K"}.get(
            self.rank, str(self.rank))
        return f"{rank_str}{suit_str}"


def standard_deck():
    return [Card(suit, rank) for suit in "SHDC" for rank in range(1, 14)]


def shuffled_deck():
    cards = standard_deck()
    shuffle(cards)
    return cards


def deal_one_five_card_hand():
    deck = shuffled_deck()
    return set(deck[:5])


def deal(number_of_hands, cards_per_hand):
    if not isinstance(number_of_hands, int) or not isinstance(cards_per_hand, int):
        raise TypeError("number_of_hands and cards_per_hand must be integers")
    if number_of_hands < 1:
        raise ValueError("number_of_hands must be at least 1")
    if cards_per_hand < 1:
        raise ValueError("cards_per_hand must be at least 1")
    if number_of_hands * cards_per_hand > 52:
        raise ValueError("not enough cards in deck to deal")
    deck = shuffled_deck()
    hands = []
    for i in range(number_of_hands):
        start = i * cards_per_hand
        hand_cards = deck[start:start + cards_per_hand]
        hands.append(set(hand_cards))
    return hands


def poker_classification(hand):
    if not isinstance(hand, set):
        raise TypeError("hand must be a set")
    if len(hand) != 5:
        raise ValueError("hand must contain exactly 5 cards")
    for card in hand:
        if not isinstance(card, Card):
            raise TypeError("hand must contain only Card objects")

    ranks = [card.rank for card in hand]
    suits = [card.suit for card in hand]

    rank_counts = {}
    for rank in ranks:
        rank_counts[rank] = rank_counts.get(rank, 0) + 1
    counts = sorted(rank_counts.values(), reverse=True)

    is_flush = len(set(suits)) == 1

    unique_ranks = sorted(set(ranks))
    is_straight = False
    if len(unique_ranks) == 5:
        if max(unique_ranks) - min(unique_ranks) == 4:
            is_straight = True
        elif set(unique_ranks) == {1, 10, 11, 12, 13}:
            is_straight = True

# Code below prints out the classification for poker_game.py
    if is_straight and is_flush:
        if set(ranks) == {1, 10, 11, 12, 13}:
            return "Royal Flush"
        return "Straight Flush"
    if counts[0] == 4:
        return "Four of a Kind"
    if counts[0] == 3 and counts[1] == 2:
        return "Full House"
    if is_flush:
        return "Flush"
    if is_straight:
        return "Straight"
    if counts[0] == 3:
        return "Three of a Kind"
    if counts[0] == 2 and counts[1] == 2:
        return "Two Pair"
    if counts[0] == 2:
        return "One Pair"
    return "High Card"
