class Card:

    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    @property
    def rank(self):
        return self._rank
    
    @rank.setter
    def rank(self, rank):
        self._rank = rank

    @property
    def suit(self):
        return self._suit
    
    @suit.setter
    def suit(self, suit):
        self._suit = suit
        
    def __str__(self):
        return self.rank + " " + self.suit
