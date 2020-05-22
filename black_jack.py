import random
import time


class Card:
    def __init__(self, suit, rank, value):
        self.suit = suit
        self.rank = rank
        self.value = value

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank, values[rank]))

    def __str__(self):
        res = []
        for card in self.deck:
            res.append(str(card))
        res = '\n'.join(res)
        return res

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self, *args):
        for hand in args:
            card = self.deck.pop()
            hand.add_card(card)


class Hand:
    def __init__(self, this_player):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.player = this_player

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_ace()

    def adjust_ace(self):
        if self.aces > 0 and self.value > 21:
            self.value -= 10
            self.aces -= 1

    def busted(self):
        if self.value > 21:
            return True
        return False

    def initialize(self):
        del self.cards
        self.cards = []
        self.value = 0
        self.aces = 0

    def is_blackjack(self):
        return True if self.value == 21 else False


class Chip:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def make_bet(self, amount):
        self.bet = amount

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(acc):
    valid_bet = False

    while not valid_bet:
        try:
            bet_amount = int(input('Please enter your bet: '))
            if bet_amount > acc.total:
                print('Bet must not exceed your balance!')
            else:
                acc.make_bet(bet_amount)
                print('Bet amount confirmed: $' + str(acc.bet))
                valid_bet = True
        except ValueError:
            print("Please enter a valid amount!")


def hit(this_deck, hand):
    this_deck.deal(hand)


def hit_or_stand(this_deck, hand):
    global playing
    respond = input("Would you like to hit or stand? Hit/Stand: ")
    if respond[0].lower() == 'h':
        hit(this_deck, hand)
    else:
        playing = False


def has_blackjack(this_player, this_dealer, this_player_acc):
    global bj_found

    if player.is_blackjack() or this_dealer.is_blackjack():
        bj_found = True
        show_all(this_player, this_dealer)
        if player.is_blackjack():
            print("Congratulation! You got a BlackJack!\n"
                  "You won ${}".format(this_player_acc.bet*2))
            this_player_acc.win_bet()
            this_player_acc.win_bet()
        elif this_dealer.is_blackjack():
            print("That's unfortunate, dealer got a Blackjack :(\n"
                  "You lost ${}".format(this_player_acc.bet))
            this_player_acc.lose_bet()


def show_some(this_player, this_dealer):
    print('--------------------------------')
    # Player's hand:
    print("Player's hand:")
    for index in range(0, len(this_player.cards)):
        print("\t {}. {}".format(index + 1, this_player.cards[index]))
    print("Player point: " + str(this_player.value))

    # Dealer's hand:
    print("Dealer's hand:")
    print("\t 1." + str(this_dealer.cards[0]))
    print("\t 2.'Card Hidden'")
    print("Dealer point: " + str(this_dealer.value))
    print('--------------------------------\n')


def show_all(this_player, this_dealer):
    print('--------------------------------')
    # Player's hand:
    print("Player's hand:")
    for index in range(0, len(this_player.cards)):
        print("\t {}. {}".format(index + 1, this_player.cards[index]))
    print("Player point: " + str(this_player.value))

    # Dealer's hand:
    print("Dealer's hand:")
    for index in range(0, len(this_dealer.cards)):
        print("\t {}. {}".format(index + 1, this_dealer.cards[index]))
    print("Dealer point: " + str(this_dealer.value))
    print('--------------------------------\n')


# Creating lists of suits, ranks, and cards
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

playing = True
bj_found = False
player_account = Chip(1000)
player = Hand('Hieu')
dealer = Hand('Dealer')

while True:
    print("Welcome to Las Vegas! Let's join us in a Blackjack game today!")
    if player_account.total == 0:
        print("We have to kick you out because you ran out of money.\n"
              "Goodbye and have fun at Vegas!")
        break

    # Create & shuffle a deck, and deal two cards to each player
    deck = Deck()
    deck.shuffle()
    player.initialize()
    dealer.initialize()
    deck.deal(player, dealer, player, dealer)

    # Take bet from player
    take_bet(player_account)

    # Show cards:
    show_some(player, dealer)

    # Check for blackjack:
    has_blackjack(player, dealer, player_account)

    if not bj_found:
        playing = True
        while playing:  # Global variable
            # Prompt the user to hit/stand
            hit_or_stand(deck, player)

            # Show cards:
            if playing:
                show_some(player, dealer)
            else:
                show_all(player, dealer)

            # Case 1: Player busted
            if player.busted():
                print("BUSTED! You lost ${}!".format(player_account.bet))
                player_account.lose_bet()
                break

        if not player.busted():
            while dealer.value < max(17, player.value) and not dealer.busted():
                deck.deal(dealer)
                time.sleep(3)
                show_all(player, dealer)

            # Case 2: Both players busted
            if dealer.busted() and player.busted():
                print("DRAW! You didn't lose")
                break

            # Case 3: Dealer busted:
            if dealer.busted():
                player_account.win_bet()
                print("DEALER BUSTED! You won ${}!".format(player_account.bet))
            else:
                # Case 4: Both didn't bust:
                if dealer.value > player.value:
                    player_account.lose_bet()
                    print("You lost ${}!".format(player_account.bet))
                else:
                    player_account.win_bet()
                    print("You won ${}!".format(player_account.bet))

    print("Balance: ${}".format(player_account.total))

    replay = str(input("Would you like to play again? Y/N: "))
    if replay.lower() == 'n':
        break
