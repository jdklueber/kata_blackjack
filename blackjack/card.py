from enum import Enum
from dataclasses import dataclass
import random


class Suit(Enum):
    HEARTS = chr(9829)  # Character 9829 is '♥'.
    DIAMONDS = chr(9830)  # Character 9830 is '♦'.
    SPADES = chr(9824)  # Character 9824 is '♠'.
    CLUBS = chr(9827)  # Character 9827 is '♣'.


rank_to_str = {
    1: "A",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "J",
    12: "Q",
    13: "K",
}


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: int

    @classmethod
    def build_deck(cls, shuffle=True) -> []:
        deck: [Card] = []
        for suit in Suit:
            for rank in rank_to_str:
                deck.append(Card(rank=rank, suit=suit))
        if shuffle:
            random.shuffle(deck)

        return deck

    def can_be_high(self):
        return self.rank == 1

    def numeric_value(self, use_high: bool = True):
        if self.rank == 1 and use_high:
            return 11
        elif self.rank > 10:
            return 10
        else:
            return self.rank

    def get_back(self):
        back = " _____ \n"
        back += "|##   |\n"
        back += "| ### |\n"
        back += "|___##|"

        return back

    def get_front(self):
        front = " _____ \n"
        front += "|{}   |\n".format(rank_to_str[self.rank].ljust(2))
        front += "|  {}  |\n".format(self.suit.value)
        front += "|___{}|".format(rank_to_str[self.rank].rjust(2, "_"))
        return front

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __eq__(self, __other: object) -> bool:
        if not isinstance(__other, Card):
            return NotImplemented

        return self.rank == __other.rank

    def __lt__(self, __other: object) -> bool:
        if not isinstance(__other, Card):
            return NotImplemented

        return self.rank < __other.rank


class Hand:
    TARGET = 21

    def __init__(self, card1: Card, card2: Card, is_player: bool = False) -> None:
        self.down: Card = card1
        self.up: [Card] = [card2]
        self.is_player = is_player

    def get_hand_display(self) -> [str]:
        output = self.down.get_back().split("\n")
        if self.is_player:
            output = self.down.get_front().split("\n")

        for card in self.up:
            for idx, line in enumerate(card.get_front().split("\n")):
                output[idx] = f"{output[idx]} {line}"

        return output

    def calculate_trial_total(self, ace_positions: [bool, [bool]]) -> int:
        tot = self.down.numeric_value(use_high=ace_positions[0])
        for idx, card in enumerate(self.up):
            ace_high = True if idx in ace_positions[1] else False
            tot += card.numeric_value(ace_high)
        return tot

    def total_can_be_lower(self, ace_positions: [bool, [bool]]) -> bool:
        if ace_positions[0]:
            ace_positions[0] = False
            return True
        if len(ace_positions[1]):
            ace_positions[1].pop()
            return True
        return False

    def get_total(self) -> int:
        ace_positions = [False, []]
        if self.down.can_be_high():
            ace_positions[0] = True
        for idx, card in enumerate(self.up):
            if card.can_be_high():
                ace_positions[1].append(idx)

        tot = self.calculate_trial_total(ace_positions=ace_positions)
        while tot > Hand.TARGET and self.total_can_be_lower(
            ace_positions=ace_positions
        ):
            tot = self.calculate_trial_total(ace_positions=ace_positions)

        return tot

    def get_visible_total(self) -> int:
        if self.is_player:
            return self.get_total()
        else:
            tot = 0
            for card in self.up:
                tot += card.numeric_value()
            return tot

    def __str__(self) -> str:
        return "\n".join(self.get_hand_display())
