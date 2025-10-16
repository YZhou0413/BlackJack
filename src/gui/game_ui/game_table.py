import sys
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QMainWindow, QApplication,
)
from PySide6.QtCore import QSize, QTimer, Signal, Qt
from src.gui.game_ui.buttons_stack import ButtonsStack

# Add src to sys.path if running from gui folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.game import Game
from src.core.player import Player, Dealer
from src.gui.game_ui.player_area import PlayerHandWidget
from src.gui.game_ui.test_dummys import dummy_player, dummy_dealer

# Represents game page
class GameTable(QWidget):
    WINDOW_FIXED_WIDTH = 700
    WINDOW_FIXED_HEIGHT = 490

    # create signal for returning to menu after game
    exit_to_menu_signal = Signal()
    # create signal for starting new game
    new_game_signal = Signal(object)

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()
        self.setMaximumSize(QSize(GameTable.WINDOW_FIXED_WIDTH, GameTable.WINDOW_FIXED_HEIGHT))

        # references to game, player and dealer instance
        self._game = None
        self._player = None
        self._dealer = None

        # setup game table ui
        self.setup_ui()

        # setup timer for ai player
        self._ai_timer = QTimer(self)
        self._ai_timer.setInterval(1000)
        self._ai_timer.timeout.connect(self._ai_step)
        self._ai_running = False


        # Dealer and player hands
    def setup_ui(self):
        self.dealer_area = PlayerHandWidget(self.dealer)
        self.player_area = PlayerHandWidget(self.player)

        #---- setup middle widget ----
        # controls widget containing status info and player action buttons
        self.controls = QWidget()
        self.controls.setMaximumHeight(140)

        # status field
        self.status_info_field = QLabel("It's your turn!")
        self.status_info_field.setAlignment(Qt.AlignCenter)
        self.status_info_field.setMinimumHeight(50)
        self.status_info_field.setFixedWidth(180)

        # create widget for switch between action buttons and game end buttons
        self.button_stack = ButtonsStack()

        # -- setup button slots
        # action buttons
        self.button_stack.hit_button.clicked.connect(self.player_draw_card_use_hit)
        self.button_stack.stand_button.clicked.connect(self.stand)
        self.button_stack.ai_button.clicked.connect(self.on_ai_clicked)
        # post game buttons
        self.button_stack.new_game_button.clicked.connect(self.on_new_game)
        self.button_stack.exit_to_menu_button.clicked.connect(self.on_exit_to_menu)

        # setup layout for controls widget
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.status_info_field)
        controls_layout.addWidget(self.button_stack)
        self.controls.setLayout(controls_layout)

        # ---- setup gametable layout ----
        self.vLayout = QVBoxLayout(self)
        self.vLayout.addWidget(self.dealer_area)
        self.vLayout.addWidget(self.controls)
        self.vLayout.addWidget(self.player_area)

    #property and setters
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
        """
        this function pass in-game property and user objs to the game table ui, also bound the signals to functions

        :return: None
        """
        self.dealer_area.owner = self.game.dealer
        self.player_area.owner = self.game.player
        
        self.dealer_area.update_player_info()
        self.player_area.update_player_info()
        self.player_area.card_widget.reset_view()
        self.dealer_area.card_widget.reset_view()
        self.render_initial_hands()

        self.game.dealer_drawn_card.connect(self.render_after_dealer_draw_new_card)
        self.game.dealer_finished_turn.connect(self.dealer_finished)
        self.game.card_reveal_signal.connect(self.reveal_dealer_card)
        
        #####test sig
        self.game.test_player_draw_signal.connect(self.player_draw_card_use_hit)

    # display winner and post game buttons
    def display_endgame_ui(self):
        """
        Determines winner and displays and according status info together with the
        post game buttons.

        :return: None
        """
        # get dealer's and player's busted states
        dealer_busted = self.game.dealer_is_busted
        player_busted = self.game.player_is_busted

        # Create fitting status message
        match self.game.player.status:
            # if user wins
            case "WIN":
                message = "Dealer's Bust" if dealer_busted else "Your hand is higher"
                message += "\n\nYou win, Congrats!"
                # grey out dealer's gametable area
                self.dealer_area.grey_out()
            # if user loses
            case "LOST":
                message = "Bust" if player_busted else "Dealer's hand is higher"
                message += "\n\nYou lose!"
                #grey out loser's gametable area
                self.player_area.grey_out()
            # if it's push
            case "PUSH":
                message = "Push\n\nYou've regained your bet :)"
            case _:
                # message to be displayed, if no other case matches
                message = "Something went wrong.\nPlease consult the Dev Team"

        # update game status message
        self.status_info_field.setText(message)

        # display post game buttons for starting a new game or returning to menu
        self.button_stack.show_end_buttons()

    
    # INSTANCE METHODS
    def player_draw_card_use_hit(self):
        """
        Lets user draw card and displays the card in the gui.

        :return: None
        """
        self.game.btn_hit_on_click()
        new_card = self.game.player.hand[-1]
        # add to player hand UI
        self.player_area.card_widget.add_card_to_view(new_card, owner="user")

        # if player busted, grey out the entire hand
        if self.game.player_is_busted: #bust actions
            self.player_area.grey_out()
            self.button_stack.disable_action_buttons()

    def render_initial_hands(self):
        """
        Renders initial hands of dealer and user.

        :return: None
        """
        #---- render DEALER hand ----
        dealer_cards_view = self.dealer_area.card_widget
        dealer_hand = self.dealer_area.owner.hand

        dealer_cards_view.initialize_dealer_hand(dealer_hand)

        #---- render USER hand ----
        user_cards_view = self.player_area.card_widget
        user_hand = self.player_area.owner.hand

        user_cards_view.initialize_user_hand(user_hand)

    
    def stand(self):
        """
        Ends player's turn, disable all player action buttons and start
        turn of the dealer.

        :return: None
        """
        #when stand is clicked, evolve from player turn to dealer turn
        self.game.btn_stand_on_click()
        self.button_stack.disable_action_buttons()
        # display status message
        self.status_info_field.setText("You stand\n\nDealer's turn")
        # start dealers turn
        self.dealer_turn_start()

    
    #dealer turn is now managed by the following funcs
    def dealer_turn_start(self):
        """
        Starts dealer's turn. This method starts a timer and call's the dealer_draw() method
        from class Game after the specified timeout.
        The timer ensures, that drawn cards aren't displayed all at once, but
        back to back, so that the user can follow more easily.

        :return: None
        """
        # if dealer's hand is higher than or equal to user's hand and dealer has more than 17..
        if self.game.calculate_hand(self.game.dealer) >= self.game.calculate_hand(self.game.player) \
            and self.game.calculate_hand(self.game.dealer) >= 17:
                #... end dealer's turn
                self.dealer_finished()

        # start drawing
        self.dealer_timer = QTimer()
        self.dealer_timer.setInterval(1000)  # 1s between cards
        self.dealer_timer.timeout.connect(self.game.dealer_draw)
        self.dealer_timer.start()

    def render_after_dealer_draw_new_card(self):
        """
        Renders the card, the dealer has drawn.

        :return: None
        """
        new_card = self.game.dealer.hand[-1]
        self.dealer_area.card_widget.add_card_to_view(new_card, owner='dealer')
        self.dealer_area.card_widget.viewport().update()

    #moved the phase up to end game from game to ui
    def dealer_finished(self):
        """
        Stops the dealer's card delay timer, calculates the winner
        and displays the endgame ui.

        :return: None
        """
        if getattr(self, 'dealer_timer', None):
            if self.dealer_timer.isActive():
                self.dealer_timer.stop()

        # trigger game result
        self.game.calc_winner()
        # display result
        self.display_endgame_ui()


    def reveal_dealer_card(self):
        """
        Reveals the second card of the dealer.

        :return: None
        """
        self.dealer_area.card_widget.reveal_dealer_second_card()


    def on_ai_clicked(self):
        """
        Activates the ai player.

        :return: None
        """
        # start AI only if not already running and we have a game
        if self._ai_running or self.game is None:
            return
        # display fitting status message
        self.status_info_field.setText("AI is playing for you now!")
        # disable all action buttons
        self.button_stack.disable_action_buttons()
        self._ai_running = True
        # run one immediate step for responsiveness, then continue on timer
        self._ai_step()
        if not self._ai_timer.isActive():
            self._ai_timer.start()


    def _ai_step(self):
        """
        Lets ai decide to stand or hit.

        :return: None
        """
        # guard
        if not self._ai_running or self.game is None:
            self._stop_ai()
            return

        # call model once (must return (res, info))
        res, info = self.game.ai_play_step()


        if res == "hit":
            self.player_area.card_widget.add_card_to_view(info, owner="user")
            self.player_area.card_widget.viewport().update()
            # if this hit ended the player's turn (bust or status changed)
            if getattr(self.game, "player_is_busted", False) or self.game.player.status != "in-game":
                self.player_area.grey_out()
                self.button_stack.disable_action_buttons()
                self._stop_ai()
                QTimer.singleShot(500, self.dealer_turn_start)
                return

        elif res == "bust":
            self.player_area.card_widget.add_card_to_view(info, owner="user")
            self.player_area.card_widget.viewport().update()
            self.player_area.grey_out()
            self.button_stack.disable_action_buttons()
            self._stop_ai()
            QTimer.singleShot(500, self.dealer_turn_start)
            return

        elif res == "stand":
            self._stop_ai()
            self.button_stack.disable_action_buttons()
            self.stand()
            return

        # noop -> next timer tick will call _ai_step again


    def _stop_ai(self):
        """
        Stops the ai mode.
        :return: None
        """
        if self._ai_timer.isActive():
            self._ai_timer.stop()
        self._ai_running = False




    #---- game end methods ----

    def on_new_game(self):
        """
        Starts a new game.
        :return: None
        """
        # initialise game
        self.game.initialize_game()
        # reset ui elements
        self.reset_ui()
        # fire new game signal for opening place bet page
        self.new_game_signal.emit(self.game.player.name)


    def on_exit_to_menu(self):
        """
        Returns the user to menu.

        :return: None
        """
        # fire open menu signal
        self.exit_to_menu_signal.emit()
    
        # reset buttons and status message
        self.reset_ui()


    def reset_ui(self):
        """
        Resets ui elements of the game table to be ready for the next game round.

        :return: None
        """
        # switch back to player action buttons
        self.player_area.reverse_gray_out()
        self.dealer_area.reverse_gray_out()
        self.button_stack.show_action_buttons()
        self.button_stack.enable_action_buttons()
        self.player_area.card_widget.reset_view()
        self.dealer_area.card_widget.reset_view()
        # switch back to initial status message
        self.status_info_field.setText("It's your turn!")


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



            
