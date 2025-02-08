# BlackJack Project

import random #importing the random library because we are working with the probability of the numbers and cards

#coloring the fonts with ANSI codes
WHITE = "\033[0;37m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
BLUE = "\033[0;34m"
MAGENTA = "\033[0;35m"
RESET = "\033[0m"

# Game's information  
suits = ('Hearts','Diamonds','Spades', 'Clubs') #creating tuple named suits and ranks because of the constant data
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten',
         'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6,
          'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11} #creating a dictionary because each card has own numeric value

# Global variable to control the game loop which means that game is actually active
playing = True


# Card Class (first class with variables suit and rank)
class Card:
    def __init__(self, suit, rank): #using the first magic method which is about inilization of the variables 
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}" #using second magic method which is about string responce 


# Deck Class (second class)
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks] #creating a clone list called Card
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.deck) #shuffling the game cards using randomizer

    def deal(self):
        return self.deck.pop() #removing the 1 card step by step, because, when shuffling the cards, after using the one card, it will be eliminated from the list.  


# Participant Class (Base Class or Parent Class for Player and Dealer)
class Participant:
    def __init__(self):
        self._hand = Hand()  # Encapsulated attribute (private) which works or depends only for Participant class

    def add_card(self, card):
        self._hand.add_card(card) #Method lets us add a card to the participant’s hand

    def get_hand_value(self):
        return self._hand.calculate_value() #method lets us check how strong the player's hand is

    def show_hand(self):
        return str(self._hand)  #method shows us what cards the participant has in their hand


# Hand Class (Fourth class)
class Hand:
    def __init__(self):
        self.cards = []  # creating an empty list for the cards dealt to the player or dealer

    def add_card(self, card):
        self.cards.append(card) # method is used to add a card to the player's hand

    def calculate_value(self):
        value = sum(values[card.rank] for card in self.cards)
        aces = sum(1 for card in self.cards if card.rank == 'Ace') #what is interesting in this part of the code is: 
        #If the total value of the hand is more than 21 (which means the player is "busted" in Blackjack), 
        # and the hand has Aces, the value of each Ace is reduced from 11 to 1 until the hand’s total 
        # value is below 21. so this is the interesting thing in this game. 
        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

    def __str__(self):
        return ', '.join(str(card) for card in self.cards) #method defines how to show the hand as a string


# Player Class (Inherits from Participant class)
class Player(Participant):
    def __init__(self):
        super().__init__()  # directly initialize the Participants methods
        self.chips = Chips()  # Player specific attribute

    def place_bet(self):
        self.chips.place_bet() # method allows the player to place a bet by 
        #calling the place_bet method of the chips object, which handles the actual betting logic.


# Dealer Class (Inherits from Participant class)
class Dealer(Participant):
    def show_hand(self):
        return f"{self._hand.cards[1]} |  hidden card" #here we use 1st indexed card, due that 0 indexed card went to player.


# Chips Class
class Chips:
    def __init__(self):
        self.total = 100000 #it can be any number,but i chose 100,000 tenge.  
        self.bet = 0 #defaulty it will be 0, because we are going to change it by ourselves. 

    def place_bet(self): 
        while True:
            try: #overseeing the errors which might exist in our code, and making them part of our code. 
                bet = int(input(f"{BLUE}You totally have ${self.total}. Enter your bet: {RESET}")) #inputting our desired beat
                if 0 < bet <= self.total:
                    self.bet = bet
                    break
                else:
                    print("Bet must be between 1 and your total chips.") #errors which will occur in the console if we didnt do the required conditions
            except ValueError:
                print("Please enter a valid integer.")


# Game Functions
def hit(deck, hand): #by using this part, we are going to add a card to the Participant where Player can HIT the card, in that shuffled list. 
    card = deck.deal() # Take the top card from the deck
    hand.add_card(card)  # Add the card to the participant's hand


def hit_or_stand(deck, player): #the function is about Player's decision about to decide HIT or STAND 
    global playing #This allows the hit_or_stand function to change the global playing variable
    while True:
        choice = input(f"{MAGENTA}Would you like to Hit or Stand? (h/s: {RESET}").lower() #inputting our decision
        if choice == 'h':
            hit(deck, player._hand) #addition of that card which were chosen to the hand
            print(f"{GREEN}You hit:{RESET} {player._hand.cards[-1]}") #inputting the value
            if player.get_hand_value() > 21:
                print(f"{RED}You busted!{RESET}") #stating the main condition of the game: if the players or dealers card will be more than 21, the player or dealer will be BUSTED. 
                playing = False #function will not be further active
            break
        elif choice == 's': 
            print(f"{GREEN}You stand.{RESET}") #if player will stand, it means that nothing will be changed in the hand of the player.
            playing = False #function will not be further active
            break
        else:
            print("Invalid response. Please enter 'h' or 's'.") #if in the console will not be printed H or s, the next reply will be an error. 


def show_some(player, dealer): #printing the hands of the player and dealer
    print(f"\n{RED}Dealer's Hand:{RESET}") 
    print(dealer.show_hand())
    print(f"{BLUE}\nYour Hand:{RESET}")
    print(player.show_hand())


def show_all(player, dealer): #printing the hands of the player and dealer
    print(f"\n{RED}Dealer's Hand:{RESET}")
    print(dealer.show_hand())
    print(f"{BLUE} \nYour Hand:{RESET}")
    print(player.show_hand())


def player_busts(chips): #counting the bets if Player Busts:
    print(f"{RED}Player busts! Dealer Python BRATISHKA wins!{RESET}")
    chips.total -= chips.bet


def player_wins(chips): #counting the bets if Player Wins:
    print(f"{BLUE}Player wins!{RESET}")
    chips.total += chips.bet


def dealer_busts(chips): #counting the bets if Dealer Busts:
    print(f"{BLUE}Dealer Python BRATISHKA busts! Player wins!{RESET}")
    chips.total += chips.bet


def dealer_wins(chips):  #counting the bets if Dealer Wins:
    print(f"{RED}Dealer Python BRATISHKA wins!{RESET}")
    chips.total -= chips.bet


# Game Loop
while True:
    print(f"{MAGENTA}Welcome to {BLUE}Nursaya's BlackJack game!{RESET} {MAGENTA}I'm glad to see you here.{RESET}")
    print(f"{MAGENTA}In this game, {RED}Python BRATISHKA{RESET} {MAGENTA}will be your Dealer! Be ready!!!{RESET}")
    deck = Deck() #creating a variable which is instance of the Deck Class
    player = Player() #creating a variable which is instance of the Player Class
    dealer = Dealer() #creating a variable which is instance of the Dealer Class

    player.place_bet()

    for i in range(2): #running two times the add_card part because each participant (player and dealer) receives two cards at the start of the game.
        player.add_card(deck.deal())
        dealer.add_card(deck.deal())

    show_some(player, dealer) #running the displaying the card part

    while playing: #running the part where player should choose hit or stand
        hit_or_stand(deck, player)

    if player.get_hand_value() <= 21: #cheching the condition for each participant
        while dealer.get_hand_value() < 17:
            hit(deck, dealer)

    show_all(player, dealer) #showing the all cards 

    player_value = player.get_hand_value() #getting the card for player
    dealer_value = dealer.get_hand_value() #getting the card for dealer

    if dealer_value > 21: #checking the game, winning or loss or tie
        dealer_busts(player.chips) 
    elif player_value > dealer_value:
        player_wins(player.chips)
    elif player_value < dealer_value:
        dealer_wins(player.chips)
    else:
        print(f"{GREEN}OHH,NOO It's a tie!{RESET}") #tie version

    print(f"\n{MAGENTA}Your total chips: ${player.chips.total}{RESET}") #showing the total bet after playing

    new_game = input(f"{MAGENTA}Would you like to play again? (yes/no): {RESET}").lower() #asking for the player to play again or not
    if new_game != 'yes':
        print(f"{MAGENTA}Thanks for playing!Bye Bye! {MAGENTA}") #leaving the game after writing the "no" and other. 
        break
    playing = True #is used to reset the game loop to continue playing.