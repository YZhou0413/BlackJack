######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################

import hashlib


class Player:

    def __init__(self, name):
        '''
        Creates a new Player. Think about which pieces of information you need at this time
        (e.g. name, highscore, input method) and add them as arguments.
        '''
        # Initialize player name
        self._name = name
        # Store the password hash instead of the plain password
        self.password_hash = ""
        # Current account balance (score)
        self._score = 1000
        # Highest historical score achieved by the player
        self._best_score = 1000


    '''------------------Pw Hash------------------'''

    @staticmethod
    def hash_password(password):
        # Hash the password using SHA-256 for security
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


    '''------------------Properties------------------'''

    @property
    def name(self):
        # Getter for player name
        return self._name
    
    @name.setter
    def name(self, new_name):
        # Setter for player name with input validation
        new = str(new_name).strip()
        if not new:
            raise NameError
        self._name = new

    @property
    def score(self):
        # Getter for current score (account balance)
        return self._score
    
    @score.setter
    def score(self, new_score):
        # Setter for score; also updates best score if necessary
        self._score = new_score

        if new_score > self._best_score:
            self._best_score = new_score

    @property
    def best_score(self):
        # Getter for best (highest) score
        return self._best_score
    
    @best_score.setter
    def best_score(self, new_best):
        # Setter for best score (e.g., when loading saved data)
        self._best_score = new_best

    @property
    def password(self):
        # Prevent direct access to the password
        raise AttributeError("Directly Reading the password is forbidden.")

    @password.setter
    def password(self, new_password):
        # When a new password is set, store its hash instead of the plaintext
        self.password_hash = self.hash_password(new_password)

    def check_password(self, password):
        # Check if the provided password matches the stored hash
        if not self.password_hash:
            return False
        return self.password_hash == self.hash_password(password)


class Dealer(Player):
    def __init__(self):
        # Initialize the dealer as a special type of player
        super().__init__("Dealer")
        # Dealer's current hand of cards
        self.hand = []
        # Dealer's current status (e.g., START, HIT, STAND)
        self.status = "START"


if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    
    # Create sample players for testing
    player1 = Player('Yoshi')  
    player2 = Player('Peach')  
