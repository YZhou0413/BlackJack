from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget
)
from PySide6.QtCore import Qt
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

        #here create tags
        self.name_tag = QLabel()
        self.score_tag = QLabel()
        self.best_tag = QLabel()
        self.vLayout.addWidget(self.name_tag)
        self.vLayout.addWidget(self.score_tag)
        self.vLayout.addWidget(self.best_tag)


        # Add stats area to layout
        self.hLayout.addWidget(self.stats_area)

        # ---- add card view to hand widget ----
        self.card_widget = CardView()
        self.hLayout.addWidget(self.card_widget)

    #update display:
    def update_player_info(self):
        if isinstance(self.owner, Dealer):
            self.name_tag.setText("Dealer")
            self.score_tag.setText("")
            self.best_tag.setText("")
        elif isinstance(self.owner, Player):
            self.name_tag.setText(self.owner.name)
            self.score_tag.setText(f"score: {self.owner.score}")
            self.best_tag.setText(f"history best: {self.owner.best_score}")

    # used this method for player lose scenario, since removing the action buttons
    # leaves the player unactionable
    def grey_out(self):
        if not hasattr(self, "_overlay_widget"):
        # create a QWidget covering the entire view, so that our user know that they cant draw anymore
            self._overlay_widget = QWidget(self)
            self._overlay_widget.setStyleSheet("background-color: rgba(0, 0, 0, 150); border-radius: 6px")
            self._overlay_widget.setGeometry(self.rect())  # match size of QGraphicsView
            self._overlay_widget.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)  # block in
            self._overlay_widget.show()
        else:
            self._overlay_widget.show()

        # force repaint
        self._overlay_widget.update()
    def reverse_gray_out(self):
        if hasattr(self, "_overlay_widget"):
            self._overlay_widget.hide()

      
