# Blackjack
# Introduction to Interactive Programming in Python Course
# RICE University - coursera.org
# by Joe Warren, John Greiner, Stephen Wong, Scott Rixner

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
message = ""
num_of_A = 1
score = 0
win = 0
loss = 0
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    
    def __init__(self):
        self.hand = []	# create Hand object

    def __str__(self):
        ans = ""        # return a string representation of a hand
        for i in range(len(self.hand)):
            ans += str(self.hand[i])
            ans += " "
        return "Hand contains " + ans
    
    def add_card(self, card):
        self.hand.append(card)	# add a card object to a hand
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        global num_of_A  
        
        sum_ = 0
        
        if self.hand == []:
             return 0
        else:          
            for i in range(len(self.hand)):
                if Card.get_rank(self.hand[i]) == "A":
                    if num_of_A == 1 or num_of_A == 2 and sum_ <= 10:
                        sum_ += VALUES[Card.get_rank(self.hand[i])] + 10
                        num_of_A += 1
                        if (num_of_A == 2 and len(self.hand) == 2):
                            sum_ += VALUES[Card.get_rank(self.hand[i])] + 10
                        
                    else:
                        sum_ += VALUES[Card.get_rank(self.hand[i])] 
                else:
                    sum_ += VALUES[Card.get_rank(self.hand[i])]       
                    
        return sum_

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        i = 0
        for card in self.hand:
            card.draw(canvas, [pos[0] + i * 100, pos[1]])
            i += 1
 
        

    
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS 
                     for rank in RANKS]
         
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)    # use random.shuffle()

    def deal_card(self):
        # deal a card object from the deck
        card = self.deck[-1]
        self.deck.remove(card)
        return card
        
    def __str__(self):
        # return a string representing the deck
        ans = ''
        for i in range(len(self.deck)):
            ans += str(self.deck[i]) + " "
        return "Deck contains " + ans    
        




#define event handlers for buttons
def deal():
    global outcome, in_play, dealer, player, loss, deck, message
    
    outcome = ""
    message = "" 
    if in_play == False:
        deck = Deck()
        deck.shuffle()
        dealer.hand = []
        player.hand = [] 
        player.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        print "Player's " + str(player)
        print "Dealer's " + str(dealer)
        message = "Hit or Stand ?"
        in_play = True
        
    elif in_play == True:
        outcome = "Do not cheat. New Game but you lost"
        print outcome
        in_play = False
        message = ""
        loss += 1
        deck.shuffle()

def hit():
    global outcome, in_play, deck, loss, message
    # if the hand is in play, hit the player
    if in_play == True:
        player.add_card(deck.deal_card())
        print "Player's " + str(player)
        
        # if busted, assign a message to outcome, update in_play and score
        if player.get_value() > 21 and in_play == True:
            outcome = "You have busted"
            print outcome
            in_play = False
            loss += 1
            message = ""
    
       
def stand():
    global outcome, dealer, deck, player, in_play, win, loss, message	# replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    message = ""
    if in_play == True and dealer.get_value() <= 17:
        while dealer.get_value() <= 17:
            dealer.add_card(deck.deal_card())
            print "Dealer's " + str(dealer)
            stand()
        # assign a message to outcome, update in_play and score
    if in_play == True and dealer.get_value() > 21:
        outcome = "Player Wins!"
        print outcome
        in_play = False
        win += 1
        
    elif in_play == True and dealer.get_value() >= player.get_value():
        outcome = "Dealer Wins!"
        print outcome
        in_play = False
        loss += 1
    
   
   

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, message, win, loss
    
    player.draw(canvas,[50,400])
    canvas.draw_text("Sexy boy's hand", [50, 385], 20, "White")
    
    dealer.draw(canvas,[50,150])
    canvas.draw_text("Dealer's hand", [50, 135], 20, "White")
        
    canvas.draw_text("Black Jack", [20, 50], 50 , "Black")
    canvas.draw_text(outcome, [445, 550], 20, "Red")
    canvas.draw_text(message, [350, 350], 30, "White")
    
    canvas.draw_text("Wins = " + str(win) + " /" + " Losses = " + str(loss), [370, 50], 20, "Yellow")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, 
                          [50+36.5,198], CARD_BACK_SIZE)
    
    
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
player = Hand()
dealer = Hand()
deal()
deck = Deck()
frame.start()


# remember to review the gradic rubric