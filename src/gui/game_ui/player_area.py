from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from src.core.player import Player, Dealer
from src.gui.game_ui.card_view import CardView


# Represents the player info and view of hand
class PlayerHandWidget(QWidget):
    HAND_FIXED_WIDTH = 700
    HAND_FIXED_HEIGHT = 150  # hand takes 30% window height

    def __init__(self, hand_owner):
        super().__init__()

        # save reference to the hand owner and save their name
        self.owner = hand_owner
        self.owner_name = hand_owner.name if hasattr(hand_owner, "score") else "Dealer"

        # create horizontal layout for player hand
        self.hLayout = QHBoxLayout()
        self.setLayout(self.hLayout)
        self.setFixedHeight(int(PlayerHandWidget.HAND_FIXED_HEIGHT))

        # ---- Create stats area ----
        # set vertical layout for stats area
        self.vLayout = QVBoxLayout()
        self.stats_area = QWidget(parent=self)
        self.stats_area.setLayout(self.vLayout)

        self.stats_area.setFixedHeight(150)
        self.stats_area.setFixedWidth(180)

        # ------> layout of DEALER info
        # if the owner of this hand widget is an instance of Dealer
        # set name tag accordingly
        if isinstance(self.owner, Dealer):
            name_tag = QLabel('Dealer')
            self.vLayout.addWidget(name_tag)

        # ------> layout of PLAYER (USER) info
        # else if the owner is an instance of Player, show name, score
        # and highscore of the user
        elif isinstance(self.owner, Player):
            name_tag = QLabel(f'{self.owner_name}')
            score_tag = QLabel("score: " + f'{self.owner.score}')
            best_tag = QLabel("history best: " + f'{self.owner.best_score}')
            self.vLayout.addWidget(name_tag)
            self.vLayout.addWidget(score_tag)
            self.vLayout.addWidget(best_tag)

        # Add stats area to layout
        self.hLayout.addWidget(self.stats_area)

        # ---- add card view to hand widget ----
        self.card_widget = CardView()
        self.hLayout.addWidget(self.card_widget)
        self.setStyleSheet("border: 1px solid red; padding: 0px; margin: 0px;")

