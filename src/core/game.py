######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################

from player import Player
from cards import Card
import random

class Game:

    def __init__(self):
        self.deck = self.create_deck()
        self.shuffle_deck

    def create_deck(self):
        deck = []
        for s in Card.SUITS:
            for r in Card.RANKS:
                deck.append((r, s))

    def shuffle_deck(self):
        random.shuffle(self.deck)
        
    def draw_card(self):
        if self.deck:
            return self.deck.pop()
        #TODO add card to hand
    

    def calculate_hand(self, hand):    
        score = 0
        aces = 0

        for c in hand:
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
            


    def is_bust(self):
        if self.calculate_hand() > 21:
            return True
        return False



    def login_user(self):
        pass

    def logout_user(self):
        pass

    def initialize_game(self):
        pass

    def start_game(self):
        pass

    def place_bet(self):
        pass

    def deal_initial_hands(self):
        pass

    def draw_card(self):
        pass

    def player_stands(self):
        pass

    def save_score(self):
        pass

    def exit_game(self):
        pass

    def load_allscores(self):
        pass



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
