from PySide6.QtWidgets import QStackedWidget, QPushButton, QHBoxLayout, QWidget, QSizePolicy
from PySide6.QtCore import Qt

class ButtonsStack(QStackedWidget):
    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        #---- player action buttons ----
        # create player action buttons
        self.hit_button = QPushButton("Hit")
        self.stand_button = QPushButton("Stand")
        self.ai_button = QPushButton("AI")

        # setup action buttons container layout
        self.action_buttons_container = QWidget()
        self.action_buttons_layout = QHBoxLayout()

        self.action_buttons_layout.addWidget(self.hit_button)
        self.action_buttons_layout.addWidget(self.stand_button)
        self.action_buttons_layout.addWidget(self.ai_button)

        self.action_buttons_container.setLayout(self.action_buttons_layout)


        #---- end game buttons ----
        # create post game buttons
        self.new_game_button = QPushButton("New Game")
        self.exit_to_menu_button = QPushButton("Exit to Menu")

        # setup post game buttons container layout
        self.end_buttons_container = QWidget()
        end_buttons_layout = QHBoxLayout()
        end_buttons_layout.addWidget(self.new_game_button)
        end_buttons_layout.addWidget(self.exit_to_menu_button)
        self.end_buttons_container.setLayout(end_buttons_layout)

        #---- setup stack ----
        self.addWidget(self.action_buttons_container)
        self.addWidget(self.end_buttons_container)
        self.setCurrentWidget(self.action_buttons_container)

    # INSTANCE METHODS
    # disables hit and stand button
    def disable_action_buttons(self):
        self.hit_button.setEnabled(False)
        self.stand_button.setEnabled(False)
        self.ai_button.setEnabled(False)

    # enables hit and stand button
    def enable_action_buttons(self):
        self.hit_button.setEnabled(True)
        self.stand_button.setEnabled(True)
        self.ai_button.setEnabled(True)

    # show player action buttons (hit, stand)
    def show_action_buttons(self):
        self.setCurrentWidget(self.action_buttons_container)

    # show end game buttons (new game, exit to menu)
    def show_end_buttons(self):
        self.setCurrentWidget(self.end_buttons_container)
