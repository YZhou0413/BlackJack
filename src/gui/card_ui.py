from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

# gets the filename of the image fitting the specified card
def get_path_from_card(card):
    """
    :param card: the given card of class Card
    :return: the local filename of the image matching the given card
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
    if rank.isalpha():
        filename = f"{rank_string}_of_{suit_string}2.png"
    else:
        filename = f"{rank_string}_of_{suit_string}.png"

    return filename


# Represents a card ui instance
class CardUI(QLabel):
    PNG_PATH = "./PNG-cards/"
    CARD_HEIGHT = 120

    # CONSTRUCTOR
    def __init__(self, card, visible=True):
        super().__init__()

        # get path of card image
        self.card_image_path =  CardUI.PNG_PATH
        self.card_image_path += get_path_from_card(card) if visible else "back.png"
        print(self.card_image_path)

        # create pixmap from card image
        card_pixmap = QPixmap(self.card_image_path)
        card_pixmap = card_pixmap.scaledToHeight(CardUI.CARD_HEIGHT, mode=Qt.SmoothTransformation)

        # display pixmap wit QLabel and fit QLabel to size of the pixmap
        self.setPixmap(card_pixmap)
        self.setFixedSize(card_pixmap.size())