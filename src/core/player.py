######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################


class Player:

    def __init__(self, name):
        '''
        Creates a new Player. Think about which pieces of information you need at this time
        (e.g. name, highscore, input method) and add them as arguments.
        '''
        self.name = name
        self.password = "0000"
        self.score = 1000 #acutual account saldo
        
        self.best_score = 1000 #history best, checked after every round


    def getScore():
        pass

    def getUsername():
        pass
    
    def set_password(self, new_password):
        pass

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
