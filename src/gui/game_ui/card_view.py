from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
)
from PySide6.QtCore import Qt, QSize
from src.gui.game_ui.card_ui import CardUI

# Represents view of hands
class CardView(QGraphicsView):
    VIEW_WIDTH = 450
    VIEW_HEIGHT = 150

    # set horizontal gap between cards
    X_GAP = 5
    X_OVERLAP = 30 #now the cards are slightly overlaping with each other, it just looks nicer

    def __init__(self):
        super().__init__()
        self._dealer_proxies = []  #to track cards, and better use a enumerate for 2. card in dealer case to avoid potential bug
        self._user_proxies = [] 

        # ---- setup cards view ----
        self.setFixedSize(QSize(int(CardView.VIEW_WIDTH), int(CardView.VIEW_HEIGHT)))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.scene_ = QGraphicsScene(self)
        self.setScene(self.scene_)

    def reset_view(self):
        """
        triggered after new game is clicked, create a new scence obj
        """
        # create new scene for automatic centering behaviour
        self.scene_ = QGraphicsScene(self)
        self.setScene(self.scene_)
        self.viewport().update()

    # adds a card to this cardview 
    def add_card_to_view(self, card, owner='user'):
        """
        triggered when received a new card signal, add a new card widget by default to the users hand. When owner is specified as dealer, then add a new card widget to dealer's hand.
        """
        #decide which proxy list to use
        proxy_list = self._dealer_proxies if owner == 'dealer' else self._user_proxies
        position_id = len(proxy_list)

        card_widget = CardUI(card)
        card_scene_item = self.scene_.addWidget(card_widget)
        card_scene_item.setPos(position_id * (card_widget.width() - self.X_OVERLAP), 0)

        proxy_list.append(card_scene_item)
        return card_scene_item

    def initialize_dealer_hand(self, dealer_hand):
        """
        initialized the dealer's card in dealer's proxy list, set the card attr _revealed for the 2. card to False to let it render as a back at start of the game 
        """
        self._dealer_proxies.clear()
        for i, card in enumerate(dealer_hand):
            proxy = self.add_card_to_view(card, owner='dealer')
            # hide second card
            if i == 1:
                proxy.widget().revealed = False
                proxy.widget().adjustSize()

    def initialize_user_hand(self, user_hand):
        """
        initialized the dealer's card in player's proxy list
        """
        self._user_proxies.clear()
        for card in user_hand:
            self.add_card_to_view(card, owner='user')

    def reveal_dealer_second_card(self):
        """
        triggered when received dealer_round_start signal, will set the attr _revealed of the dealer's 2. initial card to True and force the view to update.
        """
        if len(self._dealer_proxies) > 1:
            second_proxy = self._dealer_proxies[1]
            second_proxy.widget().revealed = True
            second_proxy.widget().adjustSize()
            self.viewport().update() 
