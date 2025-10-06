import pytest
from src.core.cards import Card


def dummy_deck():
    return {
        "2": Card("2", "Spades"),
        "8": Card("8", "Diamonds"),
        "10":Card("10", "Hearts"),
        "A": Card("A","Clubs"),
        "5": Card("5", "Spades"),
        "J": Card("J", "Clubs")
    }

