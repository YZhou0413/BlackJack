######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################
import sys
import os

sys.path.append("../")
from player import Player, Dealer
from cards import Card
import random
import login_panda as login_panda
from pprint import pprint

dummy_player = Player("dummy")



class Game:
    gamer_stat = ["START", "WIN", "LOST", "BUST", "PUSH", "in-game"]
    def __init__(self, user):
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.dealer = Dealer()
        self.dealer.hand = []
        self.dealer.status = "START"
        self.player = user #make sure is a player obj
        self.player.hand = []
        self.player.status = "START"
        self.bet = 100
        self.ai_play = False
        self.phase = 0
        self.initialize_game()


    '''------------------Print Card------------------'''

    def print_card(self, hand_owner):
        if hasattr(hand_owner, "name"):
            print(hand_owner.name, [(card.rank, card.suit) for card in hand_owner.hand])
            print("Your current Hand value is: ", self.calculate_hand(hand_owner))
            print("\n")
        else:
            print("deck", [(card.rank, card.suit) for card in hand_owner])
            print(len(hand_owner))
            

    '''------------------Deck------------------'''

    def create_deck(self):                                              #Creates Deck
        deck = []
        for s in Card.SUITS:
            for r in Card.RANKS:
                deck.append(Card(r, s))
        return deck

    def shuffle_deck(self):                                             #Shuffles Deck
        random.shuffle(self.deck)
        
    def draw_card(self):                                                #Draw Card
        if self.deck:
            return self.deck.pop()
        

        
    '''------------------Game start/reset------------------'''   

    def reset_round(self):                                              #resets all values --> create_deck() and shuffle_deck()
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.player.hand = []
        self.dealer.hand = []
        self.player.status = "START"
        self.dealer.status = "START"
        self.bet = 100
        self.phase = 0
        print("Your current Score is: ", self.player.score)
        print("Your bet for the next game is: ", self.bet)
        print("\n")

        print(r'If you want to bet more or less type "game.add_bet()" or "game.minus_bet()!')
        print(r'If you want to let an AI play for you or want to toggle it off again type "game.toggle_ai()"')
        print(r'When your happy with your bet and your AI mode type "game.place_bet()" to start the game!')
        print("\n")
        print("\n")


    def initialize_game(self):                                          #New game / Start Game / Play Again  --> start_game() and place_bet() + / - and reset_round()
        self.reset_round()

        
    def start_game(self):                                               #Bet is Placed --> Deal Cards --> deal_initial_hands()        
        self.deal_initial_hands(self.player)
        self.print_card(self.player)

        self.deal_initial_hands(self.dealer)
        self.print_card(self.dealer)

        print(r'If you want to hit (pull another card) type "game.add_on_click()"')
        print(r'When your happy with your hand and want to end your turn type "game.player_stands()"')
        print("\n")
        print("\n")

        self.dealer.status = "in-game"
        self.player.status = "in-game"

        if self.ai_play == True:
            self.ai_plays()

    def deal_initial_hands(self, hand_owner):                           #Cards gotten --> Stand / Hit Button possible
        hand_owner.hand = [self.draw_card(), self.draw_card()]



    '''------------------Place bets <phase 0>------------------'''   

    def place_bet(self):                                                #Places bet
        if self.player.score == 0:
            print("YOU LOST! NO MONEY LEFT")
            return
        self.player.score -= self.bet
        self.phase_up()
        self.start_game()

    def add_bet(self):                                                  # + Button to higher bet
        if self.player.score > self.bet:
            self.bet += 100
            print("Your bet for the next game is: ", self.bet)
            print("\n")
        else:
            print("ur broke lol")
            print("\n")


    def minus_bet(self):                                                # - Button to lower bet
        if self.bet > 100:
            self.bet -= 100
            print("Your bet for the next game is: ", self.bet)
            print("\n")
        else:
            print("well... you have to bet at least something")
            print("\n")


        
    '''------------------Player actions <phase 1>------------------'''   

    def add_on_click(self):                                            #Hit --> draw_card() and if is_bust() --> dealer_draw()
        if self.phase != 1:
            return
        else:
            self.player.hand.append(self.draw_card())
            if self.is_bust(self.player):
                self.phase_up()  #phase 2 -> Dealer
                self.print_card(self.player)
                self.dealer_draw() #reveal dealer card -> dealer actions
                return
        self.print_card(self.player)
        print(r'If you want to hit (pull another card) type "game.add_on_click()"')
        print(r'When your happy with your hand and want to end your turn type "game.player_stands()"')
        print("\n")
        print("\n")

        
    def player_stands(self):                                            #Stand --> dealer_draw()
        self.phase_up() #phase 2 -> dealer
        self.print_card(self.player)
        self.dealer_draw()

        

    
    '''------------------Phase 2 Dealer------------------'''

    def dealer_draw(self):                                              #Dealer turn --> calc_winner()
        if self.phase != 2:
            return
        else:
            if self.player.status == "BUST":
                #reveal card
                pass
            else: #nicht busted, wait for dealer to finish
                while self.calculate_hand(self.dealer) < 17: 
                    self.dealer.hand.append(self.draw_card())
                    if self.is_bust(self.dealer):
                        self.update_status(self.dealer, "BUST")
                    elif self.calculate_hand(self.player) <= self.calculate_hand(self.dealer):
                        break
                    
            self.phase_up() # phase 3 -> calc score
            self.print_card(self.dealer)
            self.calc_winner()



    '''------------------AI Plays------------------'''

    def toggle_ai(self):  
        print(self.ai_play)                                              #toggles AI on button click
        self.ai_play = (self.ai_play == False)
        print("-----after-----")
        print(self.ai_play)
    
    def ai_plays(self):                                                 #AI Plays for Player if turned True --> player_stands()
        while self.calculate_hand(self.player) < 17:
            self.add_on_click()
        self.player_stands()



    '''------------------Outcome------------------'''

    def calculate_hand(self, hand_owner):                               #Calculate hand for is_bust() and calc_winner()
        score = 0
        aces = 0
        for c in hand_owner.hand:
            if c.rank == "A":
                score += 11
                aces += 1
            elif c.rank in ["J", "Q", "K"]:
                score += 10
            else:
                score += int(c.rank)

        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score


    def is_bust(self, hand_owner):                                      #Test for calc_winner() and add_on_click()
        if self.calculate_hand(hand_owner) > 21:
            self.update_status(hand_owner, "BUST")
            return True
        return False

    def phase_up(self): #Phase Counter
        self.phase += 1

    def update_status(self, hand_owner, status):                        #Status Overview
        hand_owner.status = status
                
    def calc_winner(self):                                              #After Dealer Turn --> player.score gets adjusted if needed --> should be able to play again afterwards
        p_total = self.calculate_hand(self.player)
        d_total = self.calculate_hand(self.dealer)

        if p_total > 21:                                                #Player Bust Dealer WIN
            self.update_status(self.player, "LOST")
            self.update_status(self.dealer, "WIN")
            self.save_score()
            print(" +----------------------------------+ \n |              U LOST              | \n +----------------------------------+")
            print("\n")
            print("New score: ", self.player.score)
            print("\n")
            print("\n")
            print(r'If you want to play another game type "game.reset_round()"')
            print("\n")
            return
        
        if d_total > 21:                                                #Dealer Bust Player Win
            self.update_status(self.player, "WIN")
            self.update_status(self.dealer, "LOST")
            self.player.score += self.bet * 2
            self.save_score()
            print(" +---------------------------------+ \n |              U WON              | \n +---------------------------------+")
            print("\n")
            print("New score: ", self.player.score)
            print("\n")
            print("\n")
            print(r'If you want to play another game type "game.reset_round()"')
            print("\n")

            return
        
        if p_total == d_total:                                          #PUSH
            self.update_status(self.player, "PUSH")
            self.update_status(self.dealer, "PUSH")
            self.player.score += self.bet
            self.save_score()
            print(" +--------------------------------+ \n |              PUSH              | \n +--------------------------------+")
            print("\n")
            print("New score: ", self.player.score)
            print("\n")
            print("\n")
            print(r'If you want to play another game type "game.reset_round()"')
            print("\n")
            return
        
        if p_total > d_total:                                           #Player Win
            self.update_status(self.player, "WIN")
            self.update_status(self.dealer, "LOST")
            self.player.score += self.bet * 2
            self.save_score()
            print(" +---------------------------------+ \n |              U WON              | \n +---------------------------------+")
            print("\n")
            print("New score: ", self.player.score)
            print("\n")
            print("\n")
            print(r'If you want to play another game type "game.reset_round()"')
            print("\n")
            return
        else:                                                           #Dealer Win
            self.update_status(self.player, "LOST")
            self.update_status(self.dealer, "WIN")
            print(" +----------------------------------+ \n |              U LOST              | \n +----------------------------------+")
            self.save_score()
            print("\n")
            print("New score: ", self.player.score)
            print("\n")
            print("\n")
            print(r'If you want to play another game type "game.reset_round()"')
            print("\n")
            return


    '''------------------Users------------------'''

    def login_user(self, username, password):                           #User Login / Create
        username = str(username).strip()
        if not username or not password:
            print("Username/Password empty.")
            return False

        if login_panda.user_exists(username):
            if login_panda.verify_user(username, password):
                self.player.name = username
                self.player.password = password
                self.player.score = login_panda.get_score(username)
                return True
            print("Wrong Password.")
            return False

        if login_panda.create_user(username, password, start_score = getattr(self.player, "score", 1000)):
            self.player.name = username
            self.player.password = password
            self.player.score = login_panda.get_score(username)
            return True
        print("Error at User Creation.")
        return False


    def logout_user(self):                                              #User Logout
        if not getattr(self.player, "name", ""):
            print("No logged in User.")
            return
        self.save_score()
        self.player.name = ""


    def save_score(self):                                               #Score Save
        name = getattr(self.player, "name", "")
        if not name:
            print("No logged in User.")
            return

        try:
            login_panda.set_score(name, int(self.player.score))
        except Exception as e:
            print("Save Error:", e)


    def load_all_scores(self):                                           #Load all Scores
        try:
            return login_panda.list_scores(as_df = False)
        except Exception:
            return {}




if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''

    # Example for how we might test your program:
    print(" +---------------------------------------------------------+ \n |              ♠ ♣  B L A C K   J A C K  ♥ ♦              | \n +---------------------------------------------------------+")
    print("\n")
    game = Game(dummy_player)                                           # create new game
    