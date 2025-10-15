from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget, QHBoxLayout
)
import sys


# represents game menu
class Menu(QWidget):
    # width of menu
    MENU_WIDTH = 280

    # create signal for showing login page
    open_login_signal = Signal()
    open_scoreboard_signal = Signal()
    open_rule_view_signal = Signal()
    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        #---- create menu buttons and slots ----
        # create login button
        login_button = QPushButton("Login")
        login_button.clicked.connect(self.open_login_view)
        # set property for styling
        login_button.setProperty("role", "login-button")

        # create show rules button
        show_rules_button = QPushButton("Rules")
        show_rules_button.clicked.connect(self.open_rules_view)

        # create show scoreboard button
        show_scoreboard_button = QPushButton("Scoreboard")
        show_scoreboard_button.clicked.connect(self.open_scoreboard_view)

        # create app exit button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.exit_game)
        # set property for styling
        exit_button.setProperty("role", "exit-button")


        #---- create menu layout ----
        menu_layout = QVBoxLayout()
        menu_layout.addWidget(login_button)
        menu_layout.addWidget(show_rules_button)
        menu_layout.addWidget(show_scoreboard_button)
        menu_layout.addWidget(exit_button)

        # create menu items container for centering menu in window
        menu_container = QWidget()
        menu_container.setMaximumSize(QSize(Menu.MENU_WIDTH, 240))
        menu_container.setLayout(menu_layout)

        # set all menu buttons focusable and activate on return
        for button in menu_container.findChildren(QPushButton):
            button.setAutoDefault(True)
            button.setFocusPolicy(Qt.StrongFocus)

        # create layout for page
        menu_page_layout = QHBoxLayout()
        menu_page_layout.addWidget(menu_container)

        # add menu elements to menu
        self.setLayout(menu_page_layout)


    # SIGNAL HANDLER METHODS
    def open_login_view(self):
        self.open_login_signal.emit()

    def open_rules_view(self):
        self.open_rule_view_signal.emit()

    def open_scoreboard_view(self):
        self.open_scoreboard_signal.emit()
        
    def exit_game(self):
        sys.exit()
