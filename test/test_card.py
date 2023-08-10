from blackjack.card import Card, Suit, rank_to_str


def test_card_equality_same_suit():
    card1 = Card(suit=Suit.HEARTS, rank=2)
    card2 = Card(suit=Suit.HEARTS, rank=2)

    assert card1 == card2


def test_card_equality_diff_suit():
    card1 = Card(suit=Suit.HEARTS, rank=2)
    card2 = Card(suit=Suit.CLUBS, rank=2)

    assert card1 == card2


def test_card_lt_same_suit():
    card1 = Card(suit=Suit.HEARTS, rank=2)
    card2 = Card(suit=Suit.HEARTS, rank=3)

    assert card1 < card2


def test_card_lt_diff_suit():
    card1 = Card(suit=Suit.HEARTS, rank=2)
    card2 = Card(suit=Suit.CLUBS, rank=3)

    assert card1 < card2


def test_card_hash():
    card1 = Card(suit=Suit.HEARTS, rank=2)
    card2 = Card(suit=Suit.HEARTS, rank=2)
    card3 = Card(suit=Suit.CLUBS, rank=2)
    assert hash(card1) == hash(card2)
    assert hash(card1) != hash(card3)


def test_deck():
    deck = Card.build_deck()
    assert len(deck) == 52
    for suit in Suit:
        for rank in rank_to_str:
            candidate_card = Card(rank=rank, suit=suit)
            assert candidate_card in deck
            deck.remove(candidate_card)
    assert len(deck) == 0
