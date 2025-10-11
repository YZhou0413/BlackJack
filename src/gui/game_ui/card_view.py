from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsProxyWidget
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor
from src.gui.game_ui.card_ui import CardUI

# Represents view of hands
class CardView(QGraphicsView):
    VIEW_WIDTH = 450
    VIEW_HEIGHT = 150

    # set horizontal gap between cards
    X_GAP = 5

    def __init__(self):
        super().__init__()

        # ---- setup cards view ----
        self.setFixedSize(QSize(int(CardView.VIEW_WIDTH), int(CardView.VIEW_HEIGHT)))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scene_ = QGraphicsScene(self)
        self.scene_.setBackgroundBrush(QColor("#BDBAB9"))
        self.setScene(self.scene_)

    def update_view(self):
        pass

    def grey_up_view(self):
        pass

    # adds a card to this cardview
    def add_card_to_view(self, card):
        # get position index of new card from number of card
        position_id = len(self.scene_.items())
        # create card ui widget
        card_widget = CardUI(card)
        # add card widget to scene and get card scene item (corresponding to card widget)
        card_scene_item = self.scene_.addWidget(card_widget)
        # set position of card item
        card_scene_item.setPos(position_id * (card_widget.width() + CardView.X_GAP), 0)

    # displays initial cards of dealer
    def initialize_dealer_hand(self, dealer_hand : list):
        # show initial cards
        self.initialize_user_hand(dealer_hand)

        # get proxy widget of second card
        # (last added card, which comes first in .items() list)
        card_proxy = self.scene_.items()[0]

        # cover up card
        if isinstance(card_proxy, QGraphicsProxyWidget):
            card_proxy.widget().revealed = False
            card_proxy.adjustSize()


    # displays initial cards of user
    def initialize_user_hand(self, user_hand : list):
        for card in user_hand:
            self.add_card_to_view(card)
