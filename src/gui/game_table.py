import sys
import os
from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QMainWindow, QApplication, QPushButton
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor

# Add src to sys.path if running from gui folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game import Game
from src.core.cards import Card
from src.core.player import Player, Dealer

# Dummy objects for testing
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

def dummy_dealer():
    return Dealer()


class CardView(QGraphicsView):
    VIEW_WIDTH = 500
    VIEW_HEIGHT = 150

    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setFixedSize(QSize(int(CardView.VIEW_WIDTH), int(CardView.VIEW_HEIGHT)))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scene_ = QGraphicsScene(self)
        self.setScene(self.scene_)
        self.scene_.setBackgroundBrush(QColor("#BDBAB9"))
    def update_view(self):
        pass

    def grey_up_view(self):
        pass


class PlayerHandWidget(QWidget):
    HAND_FIXED_WIDTH = 700
    HAND_FIXED_HEIGHT = 150  # hand takes 30% window height

    def __init__(self, hand_owner):
        super().__init__()

        # save reference to the hand owner and save their name
        self.owner = hand_owner
        self.owner_name = hand_owner.name if hasattr(hand_owner, "score") else "Dealer"

        # create horizontal layout for player hand
        self.hLayout = QHBoxLayout()
        self.setLayout(self.hLayout)
        self.setFixedHeight(int(PlayerHandWidget.HAND_FIXED_HEIGHT))

        # ---- Create stats area ----
        # set vertical layout for stats area
        self.vLayout = QVBoxLayout()
        self.stats_area = QWidget(parent=self)
        self.stats_area.setLayout(self.vLayout)

        self.stats_area.setFixedHeight(150)
        self.stats_area.setFixedWidth(180)

        # ------> layout of DEALER info
        # if the owner of this hand widget is an instance of Dealer
        # set name tag accordingly
        if isinstance(self.owner, Dealer):
            name_tag = QLabel('Dealer')
            self.vLayout.addWidget(name_tag)

        # ------> layout of PLAYER (USER) info
        # else if the owner is an instance of Player, show name, score
        # and highscore of the user
        elif isinstance(self.owner, Player):
            name_tag = QLabel(f'{self.owner_name}')
            score_tag = QLabel("score: " + f'{self.owner.score}')
            best_tag = QLabel("history best: " + f'{self.owner.best_score}')
            self.vLayout.addWidget(name_tag)
            self.vLayout.addWidget(score_tag)
            self.vLayout.addWidget(best_tag)

        # Add stats area to layout
        self.hLayout.addWidget(self.stats_area)

        # ---- add card view to hand widget ----
        self.card_widget = CardView()
        self.hLayout.addWidget(self.card_widget)
        self.setStyleSheet("border: 1px solid red; padding: 0px; margin: 0px;")



class GameTable(QWidget):
    WINDOW_FIXED_WIDTH = 700
    WINDOW_FIXED_HEIGHT = 490

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(GameTable.WINDOW_FIXED_WIDTH, GameTable.WINDOW_FIXED_HEIGHT))

        # Dealer and player hands
        self.dealer_card_view = PlayerHandWidget(dummy_dealer())
        self.player_card_view = PlayerHandWidget(dummy_player())

        #---- setup middle widget ----
        # controls widget containing status info and player action buttons
        self.controls = QWidget()
        self.controls.setFixedHeight(170)

        # status field
        self.status_info_field = QLabel("Good Luck!")
        self.status_info_field.setFixedSize(QSize(200, 50))

        # setup player action buttons
        hit_button = QPushButton("Hit")
        hit_button.clicked.connect(lambda : print("pressed hit"))
        stand_button = QPushButton("Stand")
        stand_button.clicked.connect(lambda : print("pressed stand"))

        # setup buttons container layout
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout(buttons_container)
        buttons_layout.addWidget(hit_button)
        buttons_layout.addWidget(stand_button)
        buttons_layout.setAlignment(buttons_container, Qt.AlignHCenter)

        # setup layout for controls widget
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.status_info_field)
        controls_layout.addWidget(buttons_container)
        self.controls.setLayout(controls_layout)

        # ---- setup gametable layout ----
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.dealer_card_view)
        self.vLayout.addWidget(self.controls)
        self.vLayout.addWidget(self.player_card_view)

        # set background color to casino table green
        self.setStyleSheet(" background-color: #0B7D0B ;padding: 0px; margin: 0px;")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Dummy main window
    window = QMainWindow()
    window.setFixedSize(700, 490)
    window.setWindowTitle("Test Game Table")
    window.setStyleSheet("background-color: #1b5b06; padding: 0px; margin: 0px;")

    widget = GameTable()
    window.setCentralWidget(widget)
    window.show()

    sys.exit(app.exec())



            
