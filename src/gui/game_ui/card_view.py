from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsScene,
    QGraphicsProxyWidget,
    
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QBrush
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
        self.scene_.setBackgroundBrush(QColor("#BDBAB9"))
        self.setScene(self.scene_)

    def update_view(self):
        pass    
    
            
    # adds a card to this cardview 
    def add_card_to_view(self, card, owner='user'):
        #decide which proxy list to use
        proxy_list = self._dealer_proxies if owner == 'dealer' else self._user_proxies
        position_id = len(proxy_list)

        card_widget = CardUI(card)
        card_scene_item = self.scene_.addWidget(card_widget)
        card_scene_item.setPos(position_id * (card_widget.width() - self.X_OVERLAP), 0)

        proxy_list.append(card_scene_item)
        return card_scene_item

    def initialize_dealer_hand(self, dealer_hand):
        self._dealer_proxies.clear()
        for i, card in enumerate(dealer_hand):
            proxy = self.add_card_to_view(card, owner='dealer')
            # hide second card
            if i == 1:
                proxy.widget().revealed = False
                proxy.widget().adjustSize()

    def initialize_user_hand(self, user_hand):
        self._user_proxies.clear()
        for card in user_hand:
            self.add_card_to_view(card, owner='user')

    def reveal_dealer_second_card(self):
        if len(self._dealer_proxies) > 1:
            second_proxy = self._dealer_proxies[1]
            second_proxy.widget().revealed = True
            second_proxy.widget().adjustSize()
            self.viewport().update() 
