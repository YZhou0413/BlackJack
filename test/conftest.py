import pytest
from src.core.cards import Card
from src.core.game import Game
from src.core.player import Player


@pytest.fixture
def dummy_deck():
    return {
        "2": Card("2", "Spades"),
        "8": Card("8", "Diamonds"),
        "10": Card("10", "Hearts"),
        "A": Card("A", "Clubs"),
        "5": Card("5", "Spades"),
        "J": Card("J", "Clubs"),
        "9": Card("9", "Hearts")
    }


@pytest.fixture
def dummy_player():
    return Player("Tester")


@pytest.fixture
def game(dummy_player):
    return Game(dummy_player)

