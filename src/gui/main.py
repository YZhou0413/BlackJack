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
from src.gui.pages.menu import Menu
from src.gui.game_ui.game_table import GameTable
from src.gui.login.login import Login
from src.gui.pages.place_bet import PlaceBet

from src.core.player import Player
from src.core.game import Game
import src.core.login_panda as lgpd

from src.gui.pages.scoreboard import Scoreboard
from src.gui.pages.rules_view import RuleWidget

#linus password 12345


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
        self.menu = Menu()
        self.pages.addWidget(self.menu)

        # add login page
        self.login = Login()
        self.pages.addWidget(self.login)

        # add place bet page
        self.place_bet = PlaceBet()
        self.pages.addWidget(self.place_bet)

        # add game view page
        self.game_ui = GameTable()
        self.pages.addWidget(self.game_ui)

        self.scoreboard = Scoreboard()
        self.pages.addWidget(self.scoreboard)
        
        self.rule = RuleWidget()
        self.pages.addWidget(self.rule)

        # connect login button in menu with login page
        self.menu.open_login_signal.connect(self.open_login_view)
        self.menu.open_scoreboard_signal.connect(self.open_scoreboard_view)
        self.menu.open_login_signal.connect(self.open_login_view)
        self.menu.open_rule_view_signal.connect(self.open_rule_view)

        # connect signin button on login page with place bet view
        self.login.send_user_info_to_main_signal.connect(self.init_game_with_given_user)

        # connect new game button post game with place bet view
        self.game_ui.new_game_signal.connect(self.init_game_with_given_user)

        # connect lock in button on place bet page with game view
        self.place_bet.open_game_view_signal.connect(self.switch_from_place_bet_to_game_ui)

        self.scoreboard.back_signal.connect(self.show_menu)
        self.rule.back_signal.connect(self.show_menu)
        # connect exit to menu event to opening menu method
        self.game_ui.exit_to_menu_signal.connect(self.open_menu_after_game)
        

        # set menu as initial central widget of main window
        self.setCentralWidget(self.pages)
        
        
        
 
            
    def init_game_with_given_user(self, username):
        user_cur_score = lgpd.get_score(username)
        user_best = lgpd.get_best_core(username)
        self.cur_player = Player(username)
        self.cur_player.score = user_cur_score
        self.cur_player.best_score = user_best
        self.game = Game(self.cur_player)
        self.place_bet.game = self.game
        self.place_bet.refresh_page()
        self.open_place_bet_view()
        
    def switch_from_place_bet_to_game_ui(self):
        self.game_ui.game = self.game
        self.game_ui.update_game_info()
        self.open_game_view()
        


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
        self.pages.setCurrentWidget(self.game_ui)

    def show_menu(self):
        """Zeige das Menü (erste Seite)."""
        self.pages.setCurrentIndex(0)

    def open_scoreboard_view(self):
        self.scoreboard.load_scores()
        self.pages.setCurrentWidget(self.scoreboard)
        
    def open_rule_view(self):
        self.pages.setCurrentWidget(self.rule)
        
    # sets menu as current page (post game)
    def open_menu_after_game(self):
        self.pages.setCurrentWidget(self.menu)


def run():
    # create QApp instance
    app = QApplication([])

    # create and show main window
    window = MainWindow()
    window.show()

    # load stylesheet for app
    with open("./src/gui/main.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    # start event loop
    app.exec()


if __name__ == '__main__':
    run()
