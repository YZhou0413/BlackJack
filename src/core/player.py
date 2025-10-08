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
        self._name = name
        self.password_hash = ""
        self._score = 1000 #acutual account saldo
        
        self._best_score = 1000 #history best, checked after every round



    @staticmethod
    def _hash_password_simple(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        new = str(new_name).strip()
        if not new:
            raise NameError
        self._name = new

    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, new_score):
        self._score = new_score

        if new_score > self._best_score:
            self._best_score = new_score

    @property
    def best_score(self):
        return self._best_score
    
    @best_score.setter
    def best_score(self, new_best):
        self._best_score = new_best

    @property
    def password(self):
        raise AttributeError("Directly Reading the password is forbidden.")

    @password.setter
    def password(self, new_password):
        self.password_hash = self._hash_password_simple(new_password)

    def check_password(self, password):
        if not self.password_hash:
            return False
        return self.password_hash == self._hash_password_simple(password)

    def getScore(self):
        return self.score

    def getUsername(self):
        return self.name
    
    def set_password(self, new_password):
        self.password = new_password

    def set_score(self, new_score):
        self.score = new_score

    def update_from_input(self, new_info, new_val):
        pass

    def update_to_somewhere(self, info_to_save, new_val):
        pass 

class Dealer(Player):
    """Temporary for test"""
    def __init__(self):
        super().__init__("Dealer")
        self.hand = []
        self.status = "START"


if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    
    player1 = Player('Yoshi')  # create new player
    player2 = Player('Peach')  # create new player

    