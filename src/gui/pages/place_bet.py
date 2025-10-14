from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QPushButton,
    QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QApplication, QLineEdit
)

from src.core.game import Game

# Represents place bet page
class PlaceBet(QWidget):
    # default placed bet after successfully signing up
    DEFAULT_START_BET = 100

    # maximum width of mid section
    MID_MAX_WIDTH = 280

    # width of bet buttons
    BET_BUTTON_WIDTH = 110

    # create signal for showing game view
    open_game_view_signal = Signal()

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        #game to be passed in later
        self.game = None
        # INSTANCE ATTRIBUTES
        # initialize  bet
        self._placed_bet = PlaceBet.DEFAULT_START_BET
        # name of logged in user
        # todo: fetch user data
        self.username = "blackjackwinner2010"
        # new minimal balance
        # todo: fetch user data
        self._new_min_bal = 900
        # current user balance
        self._current_balance = 900

        # LAYOUT
        #----elements of HEADER ----
        page_header = QLabel("Place your bet!")
        page_header.setProperty("role", "header")
        page_header.setAlignment(Qt.AlignCenter)

        #---- textfields and buttons of CENTER ----
        # create field displaying placed bet
        self.placed_bet_field = QLineEdit("100$")
        self.placed_bet_field.setProperty("role", "bet-field")
        self.placed_bet_field.setAlignment(Qt.AlignCenter)
        self.placed_bet_field.setReadOnly(True)

        # create increase bet button
        self.increase_bet_button = QPushButton("+100$")
        self.increase_bet_button.clicked.connect(self.increase_bet)
        # set property for styling
        self.increase_bet_button.setProperty("role", "increase-button")

        # create decrease bet button
        self.decrease_bet_button = QPushButton("-100$")
        self.decrease_bet_button.setEnabled(False)
        self.decrease_bet_button.clicked.connect(self.decrease_bet)
        # set property for styling
        self.decrease_bet_button.setProperty("role", "decrease-button")

        # set width of bet buttons
        self.decrease_bet_button.setFixedWidth(PlaceBet.BET_BUTTON_WIDTH)
        self.increase_bet_button.setFixedWidth(PlaceBet.BET_BUTTON_WIDTH)

        # create lock in button
        self.lock_in_button = QPushButton("Lock in")
        self.lock_in_button.clicked.connect(self.lock_in_bet)
        # set property for styling
        self.lock_in_button.setProperty("role", "lock-in-button")

        # create flow container for bet buttons
        bet_buttons_layout = QHBoxLayout()
        # remove margins around buttons
        bet_buttons_layout.setContentsMargins(0, 0, 0, 0 )
        bet_buttons_layout.addWidget(self.decrease_bet_button)
        bet_buttons_layout.addStretch()
        bet_buttons_layout.addWidget(self.increase_bet_button)

        bet_buttons_container = QWidget()
        bet_buttons_container.setLayout(bet_buttons_layout)

        # create layout for center elements
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.placed_bet_field)
        center_layout.addWidget(bet_buttons_container)
        center_layout.addWidget(self.lock_in_button)

        center_container = QWidget()
        center_container.setMaximumWidth(PlaceBet.MID_MAX_WIDTH)
        center_container.setLayout(center_layout)

        #---- status elements of FOOTER ----
        # create user info fields
        user_name_label = QLabel("Player: ")
        self.user_name_field = QLabel()
        self.user_name_field.setText(self._username)

        user_balance_label = QLabel("Balance: ")
        self.user_balance_field = QLabel()
        self.user_balance_field.setText(str(self._new_min_bal))

        user_min_bal_label = QLabel("New min balance: ")
        self.user_min_bal_field = QLabel()
        self.user_min_bal_field.setText(str(self._new_min_bal - 100))

        # create layout for user info fields
        footer_layout = QGridLayout()
        footer_layout.addWidget(user_name_label, 0, 0)
        footer_layout.addWidget(self.user_name_field, 0, 1)
        footer_layout.addWidget(user_balance_label, 1, 0)
        footer_layout.addWidget(self.user_balance_field, 1, 1)
        footer_layout.addWidget(user_min_bal_label, 2, 0)
        footer_layout.addWidget(self.user_min_bal_field, 2, 1)

        footer_container = QWidget()
        footer_container.setProperty("role", "user-data")
        footer_container.setLayout(footer_layout)

        #---- create page layout----
        placebet_layout = QVBoxLayout()
        placebet_layout.setAlignment(Qt.AlignHCenter)
        placebet_layout.addWidget(page_header)
        placebet_layout.addWidget(center_container)
        placebet_layout.addWidget(footer_container)
        self.setLayout(placebet_layout)


    # PROPERTIES
    @property
    def new_min_bal(self):
        return self._new_min_bal

    @new_min_bal.setter
    def new_min_bal(self, new_balance):
        self._new_min_bal = new_balance
        self.user_min_bal_field.setText(str(self._new_min_bal))

    @property
    def current_balance(self):
        return self._current_balance

    @current_balance.setter
    def current_balance(self, new_balance):
        self._current_balance = new_balance
        self.user_balance_field.setText(str(self._current_balance))

    @property
    def placed_bet(self):
        return self._placed_bet

    # sets placed bet and updates ui field
    @placed_bet.setter
    def placed_bet(self, new_bet):
        self._placed_bet = new_bet
        self.update_placed_bet_field()
        
    @property
    def game(self):
        return self._game 
    @game.setter
    def game(self, new_game):
        if type(new_game) is Game:
            self._game = new_game
            
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, new_name):
        self._username = new_name


    # INSTANCE METHODS
    def increase_bet(self):
        self.placed_bet += 100
        self.new_min_bal -= 100
        print("bet increased by 100")

        # if balance is below 100, disable increase bet button
        if self.new_min_bal < 100:
            self.increase_bet_button.setEnabled(False)

        # if placed bet is at least 200, enable decrease bet button
        if self.placed_bet >= 200:
            self.decrease_bet_button.setEnabled(True)

    def decrease_bet(self):
        self.placed_bet -= 100
        self.new_min_bal += 100
        print("bet decreased by 100")

        # if placed bet is below 200
        if self.placed_bet < 200:
            self.decrease_bet_button.setEnabled(False)

        # if balance is at least 100, enable the increase bet button
        if self.new_min_bal >= 100:
            self.increase_bet_button.setEnabled(True)

    # updates displayed bet value
    def update_placed_bet_field(self):
        self.placed_bet_field.setText(str(self._placed_bet) + "$")

    def update_user_balance_field(self):
        score = self.game.player.score
        bet = self.placed_bet

        # show current user balance
        self.current_balance = score

        if score == 0:
            self.new_min_bal = 0
            self.lock_in_button.setText("Out of score")
            self.lock_in_button.setDisabled(True)
            self.increase_bet_button.setDisabled(True)
            self.decrease_bet_button.setDisabled(True)

        elif score >= bet:
            self.new_min_bal = score - bet
            self.lock_in_button.setEnabled(True)
            self.increase_bet_button.setEnabled(score - bet >= 100)
            self.decrease_bet_button.setEnabled(bet > 100)
            self.lock_in_button.setText("Lock in")

        else: 
            while bet > score and bet > 100:
                bet -= 100
            self.placed_bet = bet
            self.new_min_bal = score - bet if score >= bet else 0
            self.lock_in_button.setEnabled(score >= bet)
            self.increase_bet_button.setEnabled(False)
            self.decrease_bet_button.setEnabled(bet > 100)
            self.lock_in_button.setText("Not enough score to play")



        
    def update_user_name(self):
        if self.game is not None:
            self.username = self.game.player.name
            self.user_name_field.setText(self.username)

    def lock_in_bet(self):
        print("bet locked in, starting game...")
        print("(new balance saved in database)")
        self.game.bet = self.placed_bet
        #back-end integration
        self.game.place_bet()

        # emit signal for opening game view
        self.open_game_view_signal.emit()
        
    def refresh_page(self):
        self.update_user_name()
        if self.game.player.score < self.placed_bet:
            self.placed_bet = PlaceBet.DEFAULT_START_BET
        self.update_user_balance_field()
        self.update_placed_bet_field()
            
        


if __name__ == "__main__":
    # create QApp instance
    app = QApplication([])

    # create and show place-bet window
    window = PlaceBet()
    window.show()

    # start event loop
    app.exec()
