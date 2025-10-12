import sys
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QMainWindow, QApplication, QPushButton,
)
from PySide6.QtCore import Qt, QSize, QTimer

# Add src to sys.path if running from gui folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game import Game
from src.core.cards import Card
from src.core.player import Player, Dealer
from src.gui.game_ui.player_area import PlayerHandWidget
from src.gui.game_ui.test_dummys import dummy_player, dummy_dealer, dummy_deck

# Represents game page
class GameTable(QWidget):
    WINDOW_FIXED_WIDTH = 700
    WINDOW_FIXED_HEIGHT = 490

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()
        self.setMaximumSize(QSize(GameTable.WINDOW_FIXED_WIDTH, GameTable.WINDOW_FIXED_HEIGHT))

        # references to dummy player and dummy dealer for testing
        # todo: get references from game instance
        self._game = None
        self._player = dummy_player()
        self._dealer = dummy_dealer()
        self.player_bust_flag = False

        # Dealer and player hands
        self.dealer_area = PlayerHandWidget(self.dealer)
        self.player_area = PlayerHandWidget(self.player)

        #---- setup middle widget ----
        # controls widget containing status info and player action buttons
        self.controls = QWidget()
        self.controls.setMaximumHeight(170)

        # status field
        self.status_info_field = QLabel("Good Luck!")
        self.status_info_field.setFixedSize(QSize(200, 50))

        # setup player action buttons
        hit_button = QPushButton("Hit")
        hit_button.clicked.connect(self.player_draw_card_use_hit)
        stand_button = QPushButton("Stand")
        stand_button.clicked.connect(self.stand)

        # setup buttons container layout
        self.buttons_container = QWidget()
        buttons_layout = QHBoxLayout(self.buttons_container)
        buttons_layout.addWidget(hit_button)
        buttons_layout.addWidget(stand_button)
        buttons_layout.setAlignment(self.buttons_container, Qt.AlignmentFlag.AlignHCenter)

        # setup layout for controls widget
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.status_info_field)
        controls_layout.addWidget(self.buttons_container)
        self.controls.setLayout(controls_layout)

        # ---- setup gametable layout ----
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.dealer_area)
        self.vLayout.addWidget(self.controls)
        self.vLayout.addWidget(self.player_area)

        # set background color to casino table green
        self.setStyleSheet(" background-color: #0B7D0B ;padding: 0px; margin: 0px;")
        
        
    @property
    def game(self):
        return self._game 
    @game.setter
    def game(self, new_game):
        if type(new_game) is Game:
            self._game = new_game
            
    @property
    def dealer(self):
        return self._dealer 
    @dealer.setter
    def dealer(self, new_dealer):
        if type(new_dealer) is Dealer:
            self._dealer = new_dealer
    
    @property
    def player(self):
        return self._player 
    @player.setter
    def player(self, new_player):
        if type(new_player) is Player:
            self._player = new_player
    
    def update_game_info(self):
        self.dealer_area.owner = self.game.dealer
        self.player_area.owner = self.game.player
        
        self.dealer_area.update_player_info()
        self.player_area.update_player_info()
        
        self.render_initial_hands()
        
        self.game.dealer_start_turn.connect(self.dealer_turn_start)
        self.game.dealer_drawn_card.connect(self.dealer_draw_new_card)
        self.game.dealer_finished_turn.connect(self.dealer_finished)
        
    # TODO:add ui elements for these
    #deal with signals sent from game:
    def player_busted(self):
        #have to disable and hide hit/stand btns 
        #have to grey out player card widget
        #have to update dealer card view
        self.player_bust_flag = True
        pass

    def display_endgame_ui(self):
        #check status of players, display end game ui
        #trigger new round dialog
        pass
    
    
    # INSTANCE METHODS
    # let user draw card and display card in the gui
    def player_draw_card_use_hit(self):
        self.game.btn_hit_on_click()
        new_card = self.game.player.hand[-1]
        print("Player drew:", new_card.rank, new_card.suit)
        # add to player hand UI
        self.player_area.card_widget.add_card_to_view(new_card, owner="user")

        # if player busted, grey out the entire hand
        if self.player_bust_flag: #bust actions
            self.player_area.grey_out()
            self.buttons_container.setVisible(False)

    # renders initial hands of dealer and user
    def render_initial_hands(self):
        #---- render DEALER hand ----
        dealer_cards_view = self.dealer_area.card_widget
        dealer_hand = self.dealer_area.owner.hand

        dealer_cards_view.initialize_dealer_hand(dealer_hand)

        #---- render USER hand ----
        user_cards_view = self.player_area.card_widget
        user_hand = self.player_area.owner.hand

        user_cards_view.initialize_user_hand(user_hand)

    def stand(self):
        self.player_area.grey_out()
        self.game.btn_stand_on_click()
        self.buttons_container.setVisible(False)

    #TODO: render cards for dealer

    def dealer_turn_start(self):
        # reveal dealer's hidden card first
        self.dealer_area.card_widget.reveal_dealer_second_card()
        self.dealer_area.card_widget.viewport().update()

        # start stepwise drawing
        self.dealer_timer = QTimer()
        self.dealer_timer.setInterval(500)  # 0.5s between cards
        self.dealer_timer.timeout.connect(self.game.dealer_draw)
        self.dealer_timer.start()

    def dealer_draw_new_card(self):
        new_card = self.game.dealer.hand[-1]
        print("Dealer drew:", new_card.rank, new_card.suit)
        self.dealer_area.card_widget.add_card_to_view(new_card, owner='dealer')
        self.dealer_area.card_widget.viewport().update()

    def dealer_finished(self):
        self.dealer_area.grey_out()
        self.game.print_card(self.game.dealer)
        if hasattr(self, 'dealer_timer'):
            self.dealer_timer.stop()
            self.dealer_timer.deleteLater()
        self.game.phase_up()
        self.game.calc_winner()


if __name__ == "__main__":
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



            
