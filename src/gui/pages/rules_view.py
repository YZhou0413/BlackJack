from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtCore import QSize, Signal, Qt
import sys
import markdown

class RuleWidget(QWidget):
    WINDOW_FIXED_WIDTH = 700
    WINDOW_FIXED_HEIGHT = int(WINDOW_FIXED_WIDTH * 0.66)
    back_signal = Signal()
    def __init__(self):
        super().__init__()
        # create widget
        self.setFixedSize(QSize(RuleWidget.WINDOW_FIXED_WIDTH, RuleWidget.WINDOW_FIXED_HEIGHT))
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # create back button for returning to menu
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.back_signal.emit())
        back_btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        back_btn.setAutoDefault(True)

        # text brower widget
        page_widget = QWidget(self)
        page_layout = QVBoxLayout(page_widget)
        page_layout.setContentsMargins(10, 0, 10, 10)
        page_layout.setSpacing(2)
        page_widget.setLayout(page_layout)

        #text brower
        text_browser = QTextBrowser(page_widget)
        #file path
        self.load_markdown_file(text_browser, "./src/gui/pages/rules.md")

        page_layout.addWidget(text_browser)
        main_layout.addWidget(page_widget)
        main_layout.addWidget(back_btn)


    def load_markdown_file(self, browser, file_path):
        """
        try to load the markdown file from given path
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                markdown_text = f.read()
            html_content = markdown.markdown(markdown_text)
            browser.setHtml(html_content)
        except IOError:
            print(f"Error: Could not open or read file {file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = RuleWidget()
    mainWin.show()
    sys.exit(app.exec())