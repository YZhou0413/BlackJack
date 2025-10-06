class Card:

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
