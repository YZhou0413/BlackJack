######################################
# Introduction to Python Programming #
# Prof. Dr. Annemarie Friedrich      #
# FAI Universität Augsburg           #
# WiSe 2025/26                       #
# Software Assignment                #
######################################

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget
)
from menu import Menu
from src.gui.game_ui.game_table import GameTable
from src.gui.login.login import Login
from src.gui.place_bet import PlaceBet


# Represents app window
class MainWindow(QMainWindow):

    # CLASS CONSTANTS
    # fixed width and height of main window
    WINDOW_FIXED_WIDTH = 700
    WINDOW_FIXED_HEIGHT = int(WINDOW_FIXED_WIDTH * 0.66)


    # CONSTRUCTOR
    def __init__(self):
        #---- setup main window ----
        # call constructor method of QMainWindow
        super().__init__()

        # set title of window
        self.setWindowTitle("Black Jack")

        # set fixed size of the main window
        self.setFixedSize(QSize(MainWindow.WINDOW_FIXED_WIDTH, MainWindow.WINDOW_FIXED_HEIGHT))


        # ---- setup pages ----
        self.pages = QStackedWidget()

        # add menu page
        menu = Menu()
        self.pages.addWidget(menu)

        # add login page
        self.login = Login()
        self.pages.addWidget(self.login)

        # add place bet page
        self.place_bet = PlaceBet()
        self.pages.addWidget(self.place_bet)

        # add game view page
        self.game = GameTable()
        self.pages.addWidget(self.game)

        # connect login button in menu with login page
        menu.open_login_signal.connect(self.open_login_view)

        # connect signin button on login page with place bet view
        self.login.open_place_bet_signal.connect(self.open_place_bet_view)

        # connect lock in button on place bet page with game view
        self.place_bet.open_game_view_signal.connect(self.open_game_view)

        # set menu as initial central widget of main window
        self.setCentralWidget(self.pages)


    # SIGNAL HANDLER METHODS
    # sets login page as current page
    def open_login_view(self):
        self.pages.setCurrentWidget(self.login)

    # sets place bet page as current page
    def open_place_bet_view(self):
        self.pages.setCurrentWidget(self.place_bet)

    # sets place bet page as current page
    def open_game_view(self):
        # start game
        self.pages.setCurrentWidget(self.game)


if __name__ == '__main__':
    '''
    write additional testing code here for things that don't work well as unit tests:
    '''
    # create QApp instance
    app = QApplication([])

    # create and show main window
    window = MainWindow()
    window.show()

    # start event loop
    app.exec()
