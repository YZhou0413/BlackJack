import pytest
from src.core.game import Game





@pytest.mark.parametrize("hand_keys, expected", [
    (["A", "A", "10"], 21),
    (["2", "8"], 10),
    (["A", "J", "A"], 21),
    (["5", "8", "10"], 23),
])
def test_calculate_hand(hand_keys, expected, dummy_deck):
    hand = [dummy_deck[rank] for rank in hand_keys]
    result = Game.calculate_hand(dummy_round(), hand)
    assert result == expected


@pytest.mark.parametrize("hand, expected", [
    (["A", "A", "10"], False),
    (["2", "8"], False),
    (["A", "J", "A"], False),
    (["5", "8", "10"], True),
])
def test_is_bust(hand, expected, dummy_deck):
    hand = [dummy_deck[rank] for rank in hand]
    result = Game.is_bust(dummy_round(), hand)
    assert result == expected


@pytest.mark.parametrize("dealer_hand, player_hand, expected", 
                         [(["2", "8"], ["5", "8"], True), 
                          (["A", "10"], ["9", "9"], False),
                          (["6"], ["A", "A", "10"], True), 
                          (["A", "10"], ["9", "9"], False)])
def test_dealer_can_hit(dealer_hand, player_hand, expected):
    result = Game.dealer_can_hit(dummy_round(), dealer_hand, player_hand)
    assert result == expected


@pytest.fixture
def dummy_round():
    class DummyPlayer:
        def __init__(self):
            self.hand = []
            self.status = "START"

    class DummyDealer:
        def __init__(self):
            self.hand = []
            self.status = "START"

    class DummyRound:
        def __init__(self):
            self.phase = 1
            self.bet = 0
            self.ai_play = False
            self.deck = []
            self.player = DummyPlayer()
            self.dealer = DummyDealer()

    return DummyRound()


def test_reset_round():
    Game.reset_round(dummy_round())
    assert dummy_round.phase == 1
    assert len(dummy_round.player.hand) == 0
    assert len(dummy_round.dealer.hand) == 0
    assert dummy_round.bet == 0
    assert not dummy_round.ai_play
    assert len(dummy_round.deck) == 52
    assert dummy_round.player.status == "START"
    assert dummy_round.dealer.status == "START"
