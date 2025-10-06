######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################

from src.core.player import Player
from src.core.cards import Card
import random

class Game:
    gamer_stat = ["START", "WIN", "LOST", "BUST", "PUSH", "not yet"]
    def __init__(self, user):
        self.deck = self.create_deck()
        self.shuffle_deck()
        self.dealer = Dealer.dealer()
        self.dealer.hand = []
        self.dealer.status = "START"
        self.player = user
        self.player.hand = []
        self.player.status = "START"
        self.bet = 100
        self.ai_play = False
        self.phase = 0


    def create_deck(self):
        deck = []
        for s in Card.SUITS:
            for r in Card.RANKS:
                deck.append(Card(r, s))
        return deck

    def shuffle_deck(self):
        random.shuffle(self.deck)
        
    def draw_card(self):
        if self.deck:
            return self.deck.pop()
        
        """if who is self.player:
            
                """
    def add_on_click(self):
        self.player.hand.append(self.draw_card())
        if self.is_bust(self.player):
                self.phase_up()  #phase 2 -> Dealer
        

    def calculate_hand(self, who):    
        score = 0
        aces = 0

        for c in who.hand:
            if c.rank == "A":
                score += 11
                aces += 1
            elif c.rank == "J" or "Q" or "K":
                score += 10
            else:
                score += int(c.rank)
        
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        
        return score
            
    def phase_up(self):
        self.phase += 1

    def is_bust(self, who):
        if self.calculate_hand(who) > 21:
            self.update_status(who, "BUST")
            return True
        return False



    def login_user(self):
        pass

    def logout_user(self):
        pass

    def initialize_game(self):
        self.player.place_bet()

        

    def start_game(self):
        self.phase_up() #phase 1 -> player
        self.deal_initial_hands(self.player)
        self.deal_initial_hands(self.dealer)

    def place_bet(self):
        self.player.score - self.bet

    def add_bet(self):
        """
        when +100 clicked, self.bet += 100"""
        if self.player.score > self.bet:
            self.bet += 100
        else:
            print("ur broke")


    def minus_bet(self):
        if self.bet > 100:
            self.bet -= 100
        else:
            print("u have to bet something")

    def reset_round(self):
        self.bet = 100


    def deal_initial_hands(self, who):
        who.hand.append(self.draw_card(who))
        who.hand.append(self.draw_card(who))

    def player_stands(self):
        self.phase_up() #phase 2 -> dealer
    
    def dealer_draw(self):
        if self.phase != 2:
            pass
        else:
            while self.calculate_hand(self.dealer) < 17: 
                self.dealer.hand.append(self.draw_card())
                if self.is_bust(self.dealer):
                    self.update_status(self.dealer, "BUST")
                    self.phase_up() # phase 3 -> calc score
                

    def update_status(self, who, status):
        who.status = status

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
    game = Game()           # create new game
    for i in range(3):               # run for 3 steps
        game.step()
    game.save_game('saved')          # save game state
    game2 = Game.load_game('saved')  # load game state
    assert game.get_current_state() == game2.get_current_state()
