class Card:
    # Define possible ranks and suits for standard playing cards
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

    def __init__(self, rank, suit):
        # Initialize a card with given rank and suit
        self.rank = rank
        self.suit = suit

    @property
    def rank(self):
        # Getter for rank
        return self._rank

    @rank.setter
    def rank(self, rank):
        # Setter for rank
        self._rank = rank

    @property
    def suit(self):
        # Getter for suit
        return self._suit

    @suit.setter
    def suit(self, suit):
        # Setter for suit
        self._suit = suit

    def __str__(self):
        # Return string representation of the card (e.g., "A Hearts")
        return self.rank + " " + self.suit
