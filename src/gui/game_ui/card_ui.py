from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from src.core.game import Card
import os

def get_path_from_card(card):
    """
    gets the filename of the image fitting the specified card
    :param card: the given card instance of class Card
    :return: string of the local filename of the image matching the given card

    >>> get_path_from_card(Card("3", "Hearts"))
    '/3_of_hearts.png'

    >>> get_path_from_card(Card("A", "Spades"))
    '/ace_of_spades.png'

    >>> get_path_from_card(Card("J", "Diamonds"))
    '/jack_of_diamonds2.png'
    """

    # get suit and rank of given card
    suit = card.suit
    rank = card.rank

    # get matching string for suit and rank
    suit_string = suit.lower()

    match rank:
        case "A":
            rank_string = "ace"
        case "J":
            rank_string = "jack"
        case "K":
            rank_string = "king"
        case "Q":
            rank_string = "queen"
        case _:
            rank_string = rank


    # create filename from part strings
    if rank.isnumeric() or rank == "A":
        filename = f"/{rank_string}_of_{suit_string}.png"
    else:
        filename = f"/{rank_string}_of_{suit_string}2.png"

    return filename


# Represents a card ui instance
class CardUI(QLabel):
    PNG_PATH = os.path.abspath("./src/gui/PNG-cards") #path was problematic, fixed
    # full path to card back image
    BACK_PATH = PNG_PATH + "/back.png"
    # height of card ui widget
    CARD_HEIGHT = 120


    # CONSTRUCTOR
    def __init__(self, card):
        super().__init__()

        # set visibility of playing card
        self._revealed = True

        # full path to card front image
        self.front_path = CardUI.PNG_PATH + get_path_from_card(card)

        # set current card image path
        self._current_path = self.front_path

        # allows Qlabel to resize when pixmap size changes
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        # add pixmap to widget
        self.set_pixmap_from_path(self._current_path)


    # PROPERTIES
    @property
    def revealed(self):
        return self._revealed

    # changes revealed state of the card ui
    @revealed.setter
    def revealed(self, is_revealed):
        # revealed state has changed...
        if self.revealed != is_revealed:
            # update revealed attribute
            self._revealed = is_revealed
            # update image path
            self._current_path = self.front_path if self._revealed else CardUI.BACK_PATH
            # update pixmap of this widget
            self.set_pixmap_from_path(self._current_path)


    # INSTANCE METHODS
    def set_pixmap_from_path(self, img_path):
        """
        sets the pixmap of this widget from a path to the image file
        :param img_path: given path to the image
        :return: None
        """
        if not os.path.exists(img_path):
            print("File not found:", img_path)
        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print("Failed to load pixmap:", img_path)
        pixmap = pixmap.scaledToHeight(CardUI.CARD_HEIGHT, mode=Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(pixmap)
        self.resize(pixmap.size())


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)