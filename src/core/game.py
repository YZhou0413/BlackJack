######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################

from player import Player, Dealer
from cards import Card
import random
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


    """------------------print card------------"""
    def print_card(self, hand_owner):
        if hasattr(hand_owner, "name"):
            print(hand_owner.name, [(card.rank, card.suit) for card in hand_owner.hand])
            print(len(hand_owner.hand))
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
        self.ai_play = False


    def initialize_game(self):                                          #New game / Start Game / Play Again  --> start_game() and place_bet() + / - and reset_round()
        self.reset_round()
        pprint(vars(self))

        
    def start_game(self):                                               #Bet is Placed --> Deal Cards --> deal_initial_hands()
         #phase 1 -> player
        
        self.deal_initial_hands(self.player)
        self.print_card(self.player)
        self.deal_initial_hands(self.dealer)
        self.print_card(self.dealer)
        
        self.dealer.status = "in-game"
        self.player.status = "in-game"

    def deal_initial_hands(self, hand_owner):                           #Cards gotten --> Stand / Hit Button possible
        hand_owner.hand = [self.draw_card(), self.draw_card()]


        
    '''------------------Player actions <phase 1>------------------'''   

    def add_on_click(self):                                             #Hit --> draw_card() and if is_bust() --> dealer_draw()
        if self.phase != 1:
            return
        else:
            self.player.hand.append(self.draw_card())
            if self.is_bust(self.player):
                self.update_status(self.player, "BUST")
                self.phase_up()  #phase 2 -> Dealer
                self.dealer_draw() #reveal dealer card -> dealer actions
        self.print_card(self.player)
        print(self.calculate_hand(self.player))
        
    def player_stands(self):                                            #Stand --> dealer_draw()
        self.phase_up() #phase 2 -> dealer
        self.dealer_draw()
        self.print_card(self.player)
        print(self.calculate_hand(self.player))
        


    '''------------------Place bets <phase 0>------------------'''   

    def place_bet(self):                                                #Places bet
        self.player.score -= self.bet
        self.start_game()
        self.phase_up()

    def add_bet(self):                                                  # + Button to higher bet
        """
        when +100 clicked, self.bet += 100"""
        if self.player.score > self.bet:
            self.bet += 100
        else:
            print("ur broke")


    def minus_bet(self):                                                # - Button to lower bet
        if self.bet > 100:
            self.bet -= 100
        else:
            print("u have to bet something")


    
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
            self.calc_winner()
        self.print_card(self.dealer)
        print(self.calculate_hand(self.dealer))


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

        if p_total > 21:
            self.update_status(self.player, "LOST")
            self.update_status(self.dealer, "WIN")
            print("end game, player: " + str(p_total) + self.player.status + ". Dealer: "+ str(d_total) + self.dealer.status)
            return
        
        if d_total > 21:
            self.update_status(self.player, "WIN")
            self.update_status(self.dealer, "LOST")
            self.player.score += self.bet * 2
            print("end game, player: " + str(p_total) + self.player.status + ". Dealer: "+ str(d_total) + self.dealer.status)
            return
        
        if p_total == d_total:
            self.update_status(self.player, "PUSH")
            self.update_status(self.dealer, "PUSH")
            self.player.score += self.bet
            print("end game, player: " + str(p_total) + self.player.status + ". Dealer: "+ str(d_total) + self.dealer.status)
            return
        
        if p_total > d_total:
            self.update_status(self.player, "WIN")
            self.update_status(self.dealer, "LOST")
            self.player.score += self.bet * 2
            #check history best and save
            print("end game, player: " + str(p_total) + self.player.status + ". Dealer: "+ str(d_total) + self.dealer.status)
            return
        else:
            self.update_status(self.player, "LOST")
            self.update_status(self.dealer, "WIN")
            print("end game, player: " + str(p_total) + self.player.status + ". Dealer: "+ str(d_total) + self.dealer.status)
            return

    '''------------------placeholders------------------'''
    
    def login_user(self):
        pass

    def logout_user(self):
        pass

    def save_score(self):
        pass
    #update user score in json

    def exit_game(self):
        pass

    def load_allscores(self):
        pass
    #for scoreboard, migrate later



if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''

    # Example for how we might test your program:
    game = Game(dummy_player)           # create new game