# between human player and a computer dealer
""""
player have a bank roll
player plays a bet

player starts with 2 cards face up and dealer starts with one card face up and one card face down

player goes first in game play

Aim : to get closer to a total value of 21 than the dealer does

Possible Actions :
Hit : recieve another card
Stay : stop recieving cards

When player's turn is over, dealer starts hitting until he beats the player or busts i.e. goes over 21

Game endings:
    1> If a player keeps hitting and busts and lose the bet
    2> If after player's turn, dealer hits and computer sum is higher than player sum and is still under 21 >> Dealer beats the Player and Computer wins
    3> If after player's turn, dealer hits and gets busted >> Player wins and his money double.

Special Rules :
    Face cards (Jack, King, Queen) count as a value of 10)
    Aces can count as either 1 or 11 whichever value is preferable to the player
"""
import random
import time
import sys
import pyttsx3
import datetime
import test

# setting up engine for text to speech properties
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    '''
    takes string as an argument and provides a voice to it using engine we set up above
    '''
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    """
    Function to greet the user at the start of the game
    """
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Good Morning Sir !")
  
    elif hour>= 12 and hour<18:
        speak("Good Afternoon Sir !")  
  
    else:
        speak("Good Evening Sir !") 
    # speak("Welcome to Black Jack Game")
    speak("I am your Dealer Ben Affleck")


suits = ["Spades", "Clubs", "Hearts", "Diamonds"]
ranks = (
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Jack",
    "Queen",
    "King",
    "Ace",
)
values = {"Two" : 2,
    "Three" : 3,
    "Four" : 4,
    "Five" : 5,
    "Six" : 6,
    "Seven" : 7,
    "Eight" : 8,
    "Nine" : 9,
    "Ten" : 10,
    "Jack" : 10,
    "Queen" : 10,
    "King" : 10,
    "Ace" : 11,
    }

class Card:
    """
    This is a card class whose objects will be type of card in the deck and will contain rank, value and suit of the card
    """
    def __init__(self, suit, rank):
        self.suit = suit.capitalize()
        self.rank = rank.capitalize()
        self.value = values[self.rank]

    def __str__(self):
        return self.rank + " of " + self.suit
    
class Deck:
    """
    This is a Deck class which will contain the deck of cards
    """
    def __init__(self) -> None:
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_one(self):
        
        return self.deck.pop()
    

class Player:
    def __init__(self, name):
        self.hands = []
        self.name = name
        self.sum = 0

    def add_cards(self,card):
        self.hands.append(card)
        if (card.rank != "Ace"):
            self.sum += card.value
        else:
            if(self.sum + card.value >21):
                self.sum += 1
            else:
                self.sum += card.value

    def stand_hit(self):
        # user_choice = input("Please! Enter 0 for a stand and 1 for a hit ")
        print_str("Please! tell if you want to take a stand or a hit ")
        user_choice = test.capture()
        while(user_choice not in ["Hit","Stand"]):
            print_str("Not a valid input, Try again. . .")
            print_str("Please! tell if you want to take a stand or a hit ")
            # user_choice = input("Please! Enter 0 for a stand and 1 for a hit")
            user_choice = test.capture()
        return int(user_choice=="Hit")
    
    def display_player(self):
        print_str(f"\n{self.name}'s cards are : ")
        for i in range(0,len(self.hands)-1):
            print(self.hands[i],end=" + ")
            speak(self.hands[i])
        print(self.hands[len(self.hands)-1],"\n")
        speak(self.hands[len(self.hands)-1])


    def display_dealer(self):
        print_str(f"\n{self.name}'s cards are : ")
        print("Hidden",end = " + ")
        speak("Hidden")
        for i in range(1,len(self.hands)-1):
            print(self.hands[i],end=" + ")
            speak(self.hands[i])
        print(self.hands[len(self.hands)-1],"\n")
        speak(self.hands[len(self.hands)-1])

def print_str(string):
    for i in string:
        print(i,end="")
        # time.sleep(0.05)
    speak(string)
    print("")


# game logic
print_str("Welcome to Black Jack Game!!")
wishMe()
time.sleep(0.25)
dealer = Player("Ben Affleck")
# player = Player(input("Enter the name of the player:"))
player = Player("Player")
new_deck = Deck()
new_deck.shuffle_deck()

for i in range(2):
    player.add_cards(new_deck.deal_one())
    dealer.add_cards(new_deck.deal_one())

player.display_player()
dealer.display_dealer()
time.sleep(0.5)

print_str(f"\nIt's {player.name}'s turn\n")
time.sleep(0.25)
while(player.sum<=21 ):
    if(player.stand_hit()):
        print_str(f"\n{player.name} will be taking a hit\n")
        player.add_cards(new_deck.deal_one())
    else:
        print_str(f"\n{player.name} will be taking a stand\n")
        break
    player.display_player()
    dealer.display_dealer()
    time.sleep(0.5)

else:
    print_str(f"\nOOPS! {player.name} got busted!!!!! \n")
    sys.exit()

print_str("\nIt's now Dealer's turn\n")
time.sleep(0.25)
player.display_player()
dealer.display_player()
time.sleep(2)
while(dealer.sum<=21):
    if(dealer.sum<=player.sum):
        print_str("\nDealer will be taking a hit\n")
        time.sleep(0.25)
        dealer.add_cards(new_deck.deal_one())
    else:
        print_str(f"\nDealer reached player, thus {player.name} looses!!!!\n")
        player.display_player()
        dealer.display_player()
        break
    player.display_player()
    dealer.display_player()
    time.sleep(2)
else:
    print_str(f"\nOOPS! Dealer got busted!!!!! and {player.name} won the game \n")
    sys.exit()