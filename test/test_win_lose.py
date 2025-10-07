import pytest


@pytest.mark.parametrize("hand_keys, expected", [
    (["A", "A", "10"], 12),   # (A=11, A=1, 10=10)
    (["2", "8"], 10),
    (["A", "J", "A"], 12),
    (["5", "8", "10"], 23),
    (["A", "A", "9"], 21),
    
])
def test_calculate_hand(game, dummy_deck, dummy_player, hand_keys, expected):
    dummy_player.hand = [dummy_deck[r] for r in hand_keys]
    result = game.calculate_hand(dummy_player)
    assert result == expected


@pytest.mark.parametrize("hand_keys, expected", [
    (["A", "A", "10"], False),
    (["2", "8"], False),
    (["A", "J", "A"], False),
    (["5", "8", "10"], True),
    (["A", "A", "9"], False),
])
def test_is_bust(game, dummy_deck, dummy_player, hand_keys, expected):
    dummy_player.hand = [dummy_deck[r] for r in hand_keys]
    result = game.is_bust(dummy_player)
    assert result == expected


def test_reset_round(game, dummy_deck):
    game.player.hand = [dummy_deck["A"]]
    game.dealer.hand = [dummy_deck["10"]]
    game.bet = 500
    game.phase = 2
    game.reset_round()
    assert len(game.deck) == 52
    assert game.bet == 100
    assert game.phase == 0
    assert game.player.status == "START"
    assert game.dealer.status == "START"
    assert len(game.player.hand) == 0
    assert len(game.dealer.hand) == 0
