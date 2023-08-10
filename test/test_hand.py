import pytest
from blackjack.card import Card, Hand, Suit

ace_of_hearts = Card(rank=1, suit=Suit.HEARTS)
king_of_hearts = Card(rank=13, suit=Suit.HEARTS)
eight_of_hearts = Card(rank=8, suit=Suit.HEARTS)


@pytest.fixture
def cards():
    return (Card(rank=2, suit=Suit.CLUBS), Card(rank=12, suit=Suit.HEARTS))


@pytest.fixture
def hand(cards: (Card)):
    return Hand(cards[0], cards[1])


def test_get_hand_display(hand: Hand):
    expected = [
        " _____   _____ ",
        "|##   | |Q    |",
        "| ### | |  ♥  |",
        "|___##| |____Q|",
    ]
    actual = hand.get_hand_display()
    assert actual == expected


def test_get_hand_display_player(hand: Hand):
    expected = [
        " _____   _____ ",
        "|2    | |Q    |",
        "|  ♣  | |  ♥  |",
        "|____2| |____Q|",
    ]
    actual = hand.get_hand_display(is_player=True)
    assert actual == expected


def test_get_hand_display_two_up(hand: Hand):
    hand.up.append(Card(rank=4, suit=Suit.HEARTS))
    expected = [
        " _____   _____   _____ ",
        "|##   | |Q    | |4    |",
        "| ### | |  ♥  | |  ♥  |",
        "|___##| |____Q| |____4|",
    ]
    actual = hand.get_hand_display()
    assert actual == expected


def test_get_total_no_aces(hand: Hand):
    expected = 12
    actual = hand.get_total()
    assert actual == expected


def test_get_total_ace_down():
    my_hand = Hand(ace_of_hearts, king_of_hearts)
    expected = 21
    assert my_hand.get_total() == expected


def test_get_total_ace_up():
    my_hand = Hand(king_of_hearts, ace_of_hearts)
    expected = 21
    assert my_hand.get_total() == expected


def test_get_total_ace_down_avoid_bust():
    my_hand = Hand(ace_of_hearts, king_of_hearts)
    my_hand.up.append(king_of_hearts)
    expected = 21
    assert my_hand.get_total() == expected


def test_get_total_ace_up_avoid_bust():
    my_hand = Hand(king_of_hearts, ace_of_hearts)
    my_hand.up.append(king_of_hearts)
    expected = 21
    assert my_hand.get_total() == expected


def test_get_total_multiple_ace_up_avoid_bust():
    my_hand = Hand(king_of_hearts, ace_of_hearts)
    my_hand.up.append(eight_of_hearts)
    my_hand.up.append(ace_of_hearts)
    my_hand.up.append(ace_of_hearts)
    expected = 21
    assert my_hand.get_total() == expected


def test_get_total_ace_down_multiple_ace_up_avoid_bust():
    my_hand = Hand(ace_of_hearts, ace_of_hearts)
    my_hand.up.append(eight_of_hearts)
    my_hand.up.append(ace_of_hearts)
    my_hand.up.append(ace_of_hearts)
    expected = 12
    assert my_hand.get_total() == expected
