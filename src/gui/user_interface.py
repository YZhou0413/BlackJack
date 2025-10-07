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
)
from menu import Menu


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


        # ---- setup menu ----
        # create menu page
        menu = Menu()

        # set menu as central widget of main window
        self.setCentralWidget(menu)


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
