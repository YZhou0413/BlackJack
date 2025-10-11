from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QFormLayout,
    QLineEdit,
    QApplication,
    QTextEdit
)
from src.gui.login.login_approve_dialog import ApproveDialog

class Login(QWidget):
    # create signal for opening place bet view
    open_place_bet_signal = Signal()

    # CONSTRUCTOR
    def __init__(self):
        super().__init__()

        #---- create login form ----
        form_layout = QFormLayout()

        # config layout
        form_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        # create user input field
        self.username_input_field = QLineEdit()
        self.username_input_field.setPlaceholderText("username")

        # create password input field
        self.password_input_field = QLineEdit()
        self.password_input_field.setPlaceholderText("password")

        # create signin button
        signin_button = QPushButton("Sign in")
        signin_button.clicked.connect(self.validate_signin)

        # create form info textfield
        self.form_info = QTextEdit()
        self.form_info.setText("Creates a new account, if the username is not yet taken.")
        self.form_info.setReadOnly(True)

        # add form elements to layout
        form_layout.addRow("username", self.username_input_field)
        form_layout.addRow("password", self.password_input_field)
        form_layout.addRow(signin_button)
        form_layout.addRow(self.form_info)

        # set layout of login widget
        self.setLayout(form_layout)


    # SIGNAL HANDLER METHODS
    # handles signin and account creation
    def validate_signin(self):
        # save current form input
        username = self.username_input_field.text()
        password = self.password_input_field.text()

        #---- validate input ----
        # check valid username
        if not Login.check_username(username):
            print("username not valid")
            self.form_info.setText("username \"%s\" invalid" % username)
            return None

        # check valid password
        if not Login.check_password(password):
            print("password not valid")
            self.form_info.setText("password invalid")
            return None

        #---- compare input with user base ----
        # if username is taken, check for matching credentials
        if Login.check_username_exists(username):
                if not Login.check_correct_credentials(username, password):
                    print("Username or password incorrect")
                    self.form_info.setText("username or password incorrect")

        # if username not yet taken, open modal for user approval of account creation
        else:
            #---- show modal dialog ----
            modal_dialog = ApproveDialog(parent=self, title="Confirm account creation")
            modal_dialog.set_dialog_message(
                "Do you want to create a new account for \"%s\"?" % username
            )

            # if user cancels, close modal
            if not modal_dialog.exec():
                self.form_info.setText("Account creation disapproved by user")
                # exit sign in validation
                return None

            # if user accepts, create new account
            else:
                print("User has approved. Account creation triggered")
                self.trigger_account_creation(username, password)

        #---- grant access to game ----
        # if credentials match or user approves account creation
        # send signal for showing place bet page
        self.open_place_bet_signal.emit()
        print("Load player data and open bet page")
        return None


    # BACKEND COMMUNICATION METHODS
    # checks if an account with the given username already exists
    @staticmethod
    def check_username_exists(username):
        print("Check if username exists in database")
        # todo: connect with backend
        return False

    # check if username and password match
    @staticmethod
    def check_correct_credentials(username, password):
        print("Checks if password is correct")
        # todo: connect with backend
        return False

    # trigger account creation
    @staticmethod
    def trigger_account_creation(username, password):
        # todo: connect with backend
        pass

    # HELPER METHODS
    # checks if username has valid format
    @staticmethod
    def check_username(username):
        if username is None:
            return False
        if len(username) < 2:
            return False
        return True

    # checks if password has valid format
    @staticmethod
    def check_password(password):
        if password is None:
            return False
        if len(password) < 5:
            return False
        return True


if __name__ == "__main__":
    # create QApp instance
    app = QApplication([])

    # create and show login window
    window = Login()
    window.show()

    # start event loop
    app.exec()