from src.core.cards import Card
from src.core.player import Player, Dealer
from src.core.game import Game

# Dummy objects for testing
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

def dummy_player():
    player = Player("Tester")
    deck = dummy_deck()

    # initialize player hand
    player.hand = [deck["2"], deck["10"]]
    return player

def dummy_dealer():
    dealer = Dealer
    deck = dummy_deck()

    # initialize dealer hand
    dealer.hand = [deck["8"], deck["A"]]
    return dealer
