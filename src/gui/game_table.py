import sys
import os
from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QMainWindow, QApplication, QPushButton, QGraphicsItem, QGraphicsPixmapItem, QGraphicsProxyWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor, QPixmap

# Add src to sys.path if running from gui folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game import Game
from src.core.cards import Card
from src.core.player import Player, Dealer
from card_ui import CardUI

# Represents view of hands
class CardView(QGraphicsView):
    VIEW_WIDTH = 450
    VIEW_HEIGHT = 150

    # set horizontal gap between cards
    X_GAP = 5

    def __init__(self):
        super().__init__()

        # ---- setup cards view ----
        self.setFixedSize(QSize(int(CardView.VIEW_WIDTH), int(CardView.VIEW_HEIGHT)))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scene_ = QGraphicsScene(self)
        self.scene_.setBackgroundBrush(QColor("#BDBAB9"))
        self.setScene(self.scene_)

    def update_view(self):
        pass

    def grey_up_view(self):
        pass

    # adds a card to this cardview
    def add_card_to_view(self, card):
        # get position index of new card from number of card
        position_id = len(self.scene_.items())
        # create card ui widget
        card_widget = CardUI(card)
        # add card widget to scene and get card scene item (corresponding to card widget)
        card_scene_item = self.scene_.addWidget(card_widget)
        # set position of card item
        card_scene_item.setPos(position_id * (card_widget.width() + CardView.X_GAP), 0)

    # displays initial cards of dealer
    def initialize_dealer_hand(self, dealer_hand : list):
        # show initial cards
        self.initialize_user_hand(dealer_hand)

        # get proxy widget of second card
        # (last added card, which comes first in .items() list)
        card_proxy = self.scene_.items()[0]

        # cover up card
        if isinstance(card_proxy, QGraphicsProxyWidget):
            card_proxy.widget().revealed = False
            card_proxy.adjustSize()


    # displays initial cards of user
    def initialize_user_hand(self, user_hand : list):
        for card in user_hand:
            self.add_card_to_view(card)


# Represents the player info and view of hand
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


# Represents game page
class GameTable(QWidget):
    WINDOW_FIXED_WIDTH = 700
    WINDOW_FIXED_HEIGHT = 490

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(GameTable.WINDOW_FIXED_WIDTH, GameTable.WINDOW_FIXED_HEIGHT))

        # references to dummy player and dummy dealer for testing
        # todo: get references from game instance
        self.player = dummy_player()
        self.dealer = dummy_dealer()

        # Dealer and player hands
        self.dealer_card_view = PlayerHandWidget(self.dealer)
        self.player_card_view = PlayerHandWidget(self.player)

        #---- setup middle widget ----
        # controls widget containing status info and player action buttons
        self.controls = QWidget()
        self.controls.setFixedHeight(170)

        # status field
        self.status_info_field = QLabel("Good Luck!")
        self.status_info_field.setFixedSize(QSize(200, 50))

        # setup player action buttons
        hit_button = QPushButton("Hit")
        hit_button.clicked.connect(self.draw_card)
        stand_button = QPushButton("Stand")
        stand_button.clicked.connect(self.stand)

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


    # INSTANCE METHODS
    # let user draw card and display card in the gui
    def draw_card(self):
        # let player draw card
        # todo: connect with Backend, call add_on_click on game instance
        self.player.hand.append(dummy_deck()["5"])

        # save this new card
        new_card = self.player.hand[-1]

        # add card to player view
        user_card_view = self.player_card_view.card_widget
        user_card_view.add_card_to_view(new_card)

    # renders initial hands of dealer and user
    def render_initial_hands(self):
        #---- render DEALER hand ----
        dealer_cards_view = self.dealer_card_view.card_widget
        dealer_hand = self.dealer_card_view.owner.hand

        dealer_cards_view.initialize_dealer_hand(dealer_hand)

        #---- render USER hand ----
        user_cards_view = self.player_card_view.card_widget
        user_hand = self.player_card_view.owner.hand

        user_cards_view.initialize_user_hand(user_hand)


    def stand(self):
        print("pressed stand")


if __name__ == "__main__":
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
        player = Player("Tester")
        deck = dummy_deck()

        # initialize player hand
        player.hand = [deck["2"], deck["10"]]
        return player

    def dummy_dealer():
        dealer = Dealer
        deck = dummy_deck()

        # initialize dealer hand
        dealer.hand = [deck["8"], deck["A"]]
        return dealer


    # ---- open gametable window ----

    app = QApplication(sys.argv)

    # Dummy main window
    window = QMainWindow()
    window.setFixedSize(700, 490)
    window.setWindowTitle("Test Game Table")
    window.setStyleSheet("background-color: #1b5b06; padding: 0px; margin: 0px;")

    widget = GameTable()
    window.setCentralWidget(widget)
    window.show()

    # test displaying initial hands
    widget.render_initial_hands()

    sys.exit(app.exec())



            
