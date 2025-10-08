from PySide6.QtWidgets import (
    QWidget,
    QTextEdit,
    QPushButton,
    QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QApplication
)


# Represents place bet page
class PlaceBet(QWidget):
    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        # INSTANCE ATTRIBUTES
        # current user balance
        self._current_balance = 900
        # placed bet
        self._placed_bet = 100

        # LAYOUT
        #----elements of HEADER ----
        page_header = QLabel("Place your bet!")

        #---- textfields and buttons of CENTER ----
        # create field displaying placed bet
        self.placed_bet_field = QTextEdit("100$")
        self.placed_bet_field.setReadOnly(True)

        # create increase bet button
        increase_bet_button = QPushButton("+100$")
        increase_bet_button.clicked.connect(self.increase_bet)

        # create decrease bet button
        decrease_bet_button = QPushButton("-100$")
        decrease_bet_button.clicked.connect(self.decrease_bet)

        # create lock in button
        lock_in_button = QPushButton("Lock in")
        lock_in_button.clicked.connect(self.lock_in_bet)

        # create flow container for bet buttons
        bet_buttons_layout = QHBoxLayout()
        bet_buttons_layout.addWidget(decrease_bet_button)
        bet_buttons_layout.addWidget(increase_bet_button)

        bet_buttons_container = QWidget()
        bet_buttons_container.setLayout(bet_buttons_layout)

        # create layout for center elements
        center_layout = QVBoxLayout()
        center_layout.addWidget(self.placed_bet_field)
        center_layout.addWidget(bet_buttons_container)
        center_layout.addWidget(lock_in_button)

        center_container = QWidget()
        center_container.setLayout(center_layout)

        #---- status elements of FOOTER ----
        footer_layout = QGridLayout()

        footer_container = QWidget()
        footer_container.setLayout(footer_layout)

        #---- create page layout----
        placebet_layout = QVBoxLayout()
        placebet_layout.addWidget(page_header)
        placebet_layout.addWidget(center_container)
        placebet_layout.addWidget(footer_container)
        self.setLayout(placebet_layout)


    # PROPERTIES
    @property
    def current_balance(self):
        return self._current_balance

    @current_balance.setter
    def current_balance(self, new_balance):
        self._current_balance = new_balance

    @property
    def placed_bet(self):
        return self._placed_bet

    @placed_bet.setter
    def placed_bet(self, new_bet):
        self._placed_bet = new_bet
        self.update_placed_bet_field()


    # INSTANCE METHODS
    def increase_bet(self):
        self.placed_bet += 100
        self.current_balance -= 100
        print("bet increased by 100")

    def decrease_bet(self):
        self.placed_bet -= 100
        self.current_balance += 100
        print("bet decreased by 100")

    def lock_in_bet(self):
        print("bet locked in, starting game...")
        print("(new balance saved in database)")
        # todo: connect to backend

    # updates displayed bet value
    def update_placed_bet_field(self):
        self.placed_bet_field.setText(str(self._placed_bet) + "$")

    def set_initial_user_balance(self, balance):
        pass


if __name__ == "__main__":
    # create QApp instance
    app = QApplication([])

    # create and show place-bet window
    window = PlaceBet()
    window.show()

    # start event loop
    app.exec()
