from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QWidget, QVBoxLayout, QHBoxLayout,QPushButton, QApplication, QFileDialog, QLabel
from PySide6.QtGui import QColor, QPixmap, QImage, QPainter, QIcon, QTransform
from PySide6.QtCore import Qt, QRectF, QSize, QRect

import sys
sys.path.append('../')
from src.core.cards import Card
from src.core.player import Player, Dealer
from src.core.game import Game

#goal of this file is to draw game board
# ___dummy test object____
CARD_FOLDER_PATH = "Asset/PNG-Cards/"
def dummy_deck():
    return {
        "2": Card("2", "Spades"),
        "8": Card("8", "Diamonds"),
        "10": Card("10", "Hearts"),
        "A": Card("A", "Clubs"),
        "5": Card("5", "Spades"),
        "J": Card("J", "Clubs"),
        "9": Card("9", "Hearts")
    }


def dummy_player():
    return Player("Tester")


def game(dummy_player):
    return Game(dummy_player)

class PlayerHandWidget(QWidget):
    HAND_FIXED_WIDTH = 640
    HAND_FIXED_HEIGHT = int(HAND_FIXED_WIDTH * 0.66 * 0.3) #hand takes 30% window height
    
    def __init__(self, hand_owner):
        super().__init__()
        self.owner = hand_owner
        self.owner_name = hand_owner.name
        self.vLayout = QVBoxLayout()
        self.hLayout = QHBoxLayout()
        
        
        
        
    
    
    def setup_ui(self):
        self.setLayout(self.hLayout) 
        
        #stats area at left 
        self.stats_area =  QWidget(parent=self, width=int(PlayerHandWidget.HAND_FIXED_WIDTH * 0.2))
        self.stats_area.setLayout(self.vLayout)
        if type(self.owner) is Player:
            name_tag = QLabel(f'{self.owner_name}')
            score_tag = QLabel("score: " + f'{self.owner.score}')
            best_tag = QLabel("history best " + f'{self.owner.best_score}')
            self.vLayout.addChildWidget(name_tag)
            self.vLayout.addChildWidget(score_tag)
            self.vLayout.addChildWidget(best_tag)
        elif type(self.owner) is Dealer:
            name_tag = QLabel('Dealer')
            self.vLayout.addWidget(name_tag)
        
        #add the card view widget
        self.card_widget = CardView()
        self.hLayout.addChildWidget(self.card_widget)
            
#card area in the middle
class CardView(QGraphicsView):
    VIEW_WIDTH = 640 * 0.5
    VIEW_HEIGHT = int(640 * 0.66 * 0.3)
    
    def __init__(self):
        super().__init__()
        
        
    def setup_ui(self):
        self.setFixedSize(QSize(int(CardView.VIEW_WIDTH), int(CardView.VIEW_HEIGHT)))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scene_ = QGraphicsScene(self)
        self.setScene(self.scene_)  
        
    def update_view(self):                  #when a card is add to view, or a card needs to be reveal, we need to update view
        pass
    
    
    def grey_up_view(self):                 #when man busted or game finished, we will blend out the card view
        pass      

        
    
    
    

class GameTable(QWidget):
        WINDOW_FIXED_WIDTH = 700
        WINDOW_FIXED_HEIGHT = int(WINDOW_FIXED_WIDTH * 0.66)


    # CONSTRUCTOR
        def __init__(self):
        #---- setup game table----
            super().__init__()


            # set fixed size of the main window
            self.setFixedSize(QSize(GameTable.WINDOW_FIXED_WIDTH, GameTable.WINDOW_FIXED_HEIGHT))
            
        def setup_ui(self):
            self.dealer_card_view = PlayerHandWidget(dummy_player("Dealer"))
            self.vLayout = QVBoxLayout(self)
            self.vLayout
            
            


            
