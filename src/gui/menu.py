from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget
)


# represents game menu
class Menu(QWidget):
    # create signal for showing login page
    open_login_signal = Signal()
    open_scoreboard_signal = Signal()

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        #---- create menu buttons and slots ----
        # create login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.open_login_view)
        # create show rules button
        show_rules_button = QPushButton("Rules")
        show_rules_button.clicked.connect(self.open_rules_view)
        # create show scoreboard button
        show_scoreboard_button = QPushButton("Scoreboard")
        show_scoreboard_button.clicked.connect(self.open_scoreboard_view)
        # create app exit button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.exit_game)


        #---- create menu layout ----
        menu_layout = QVBoxLayout()
        menu_layout.addWidget(login_button)
        menu_layout.addWidget(show_rules_button)
        menu_layout.addWidget(show_scoreboard_button)
        menu_layout.addWidget(exit_button)

        # add menu elements to menu
        self.setLayout(menu_layout)


    # SIGNAL HANDLER METHODS
    def open_login_view(self):
        self.open_login_signal.emit()

    def open_rules_view(self):
        print("Rules button pressed")

    def open_scoreboard_view(self):
        self.open_scoreboard_signal.emit()
        
    def exit_game(self):
        print("Exit game button was pressed")
