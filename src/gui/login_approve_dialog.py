from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QVBoxLayout,
    QApplication
)


# Represents dialog for approving the creation of
# a new user account
class ApproveDialog(QDialog):
    # CONSTRUCTOR
    def __init__(self, parent=None, title=""):
        super().__init__()

        # set dialog title
        self.setWindowTitle(title)
        # create label for dialog message
        self.message_label = QLabel()

        #---- setup dialog buttons ----
        buttons = QDialogButtonBox.Yes | QDialogButtonBox.Cancel

        # config button events
        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        #---- create dialog layout ----
        layout = QVBoxLayout()
        # add dialog message
        # self.set_dialog_message("Do you want to create a new account for <username>?")
        layout.addWidget(self.message_label)
        # add dialog buttons
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)


    # INSTANCE METHODS
    # sets dialog message
    def set_dialog_message(self, new_message):
        self.message_label.setText(new_message)


if __name__ == "__main__":
    # create QApp instance
    app = QApplication([])

    # create and show dialog
    window = ApproveDialog()
    window.show()

    # start event loop
    app.exec()