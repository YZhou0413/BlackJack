from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QFormLayout,
    QLineEdit,
    QApplication,
    QTextEdit
)

class Login(QWidget):

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        #---- create login form ----
        # create signin button
        signin_button = QPushButton("Sign in")
        signin_button.clicked.connect(self.validate_signin)

        # create form info textfield
        form_info = QTextEdit()
        form_info.setText("Creates a new account, if the username is not yet taken.")
        form_info.setReadOnly(True)


        #---- create login layout ----
        form_layout = QFormLayout()

        # config layout
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # create user input field
        username_input_field = QLineEdit()
        username_input_field.setPlaceholderText("username")

        # create password input field
        password_input_field = QLineEdit()
        password_input_field.setPlaceholderText("password")

        # add form elements to layout
        form_layout.addRow("username", username_input_field)
        form_layout.addRow("password", password_input_field)
        form_layout.addRow(signin_button)
        form_layout.addRow(form_info)

        # set layout of login widget
        self.setLayout(form_layout)

    # SIGNAL HANDLER METHODS
    def validate_signin(self):
        print("Check if username and password are valid")
        print("Check if username exist. If it does, compare passwords.")
        print("If password invalid, show error")


if __name__ == "__main__":
    # create QApp instance
    app = QApplication([])

    # create and show main window
    window = Login()
    window.show()

    # start event loop
    app.exec()