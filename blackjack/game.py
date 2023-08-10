import blackjack.consoleio as io
from blackjack.card import Card, Hand

MENU_HIT = 1
MENU_STAY = 2
MENU_YES = 1
MENU_NO = 0
DEALER_HIT_ON = 15

game_menu = {MENU_HIT: "Hit", MENU_STAY: "Stay"}
play_again_menu = {MENU_YES: "Play Again", MENU_NO: "Leave while you still have money"}


def run_series(starting_funds: int = 100):
    funds = starting_funds
    running = True
    while running:
        print(f"You currently have ${funds}")
        bet = io.get_int_from_user("Enter your bet", 10, funds)
        if run_game():
            funds += bet
        else:
            funds -= bet

        if funds <= 0:
            print(
                "You are out of funds and security is on their way to eject you from the casino.  RUN!"
            )
            return

        print(f"Current funds: {funds}")
        choice = io.get_menu_choice(play_again_menu)
        if choice != MENU_YES:
            running = False


def run_game() -> bool:
    deck = Card.build_deck()
    dealer_hand = Hand(deck.pop(), deck.pop())
    player_hand = Hand(deck.pop(), deck.pop(), is_player=True)

    print_game_state(dealer_hand, player_hand, deck)

    running = True

    # Player Round
    while running:
        choice = io.get_menu_choice(game_menu)

        if choice == MENU_HIT:
            player_hand.up.append(deck.pop())
            if player_hand.get_total() > Hand.TARGET:
                running = False
        else:
            running = False

        print_game_state(dealer_hand, player_hand, deck)

    if player_hand.get_total() > Hand.TARGET:
        io.print_title("BUSTED:  Dealer Wins")
        return False

    while dealer_hand.get_total() <= DEALER_HIT_ON:
        dealer_hand.up.append(deck.pop())

    dealer_hand.is_player = True
    print_game_state(dealer_hand, player_hand, deck)

    if dealer_hand.get_total() > Hand.TARGET:
        io.print_title("Dealer busted.  You win!!")
        return True
    elif dealer_hand.get_total() >= player_hand.get_total():
        io.print_title("Dealer wins!!")
        return False
    else:
        io.print_title("You win!")
        return True


def print_game_state(dealer_hand, player_hand, deck):
    io.print_title(f"{len(deck)} cards remain in the deck.")
    print(f"DEALER: {dealer_hand.get_visible_total()}")
    print(dealer_hand)
    print()
    print(f"PLAYER: {player_hand.get_visible_total()}")
    print(player_hand)
    print()
