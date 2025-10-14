import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtGui import QFont
from PySide6.QtCore import QSize, Signal
import markdown

class RuleWidget(QWidget):
    WINDOW_FIXED_WIDTH = 700
    WINDOW_FIXED_HEIGHT = int(WINDOW_FIXED_WIDTH * 0.66)
    back_signal = Signal()
    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(RuleWidget.WINDOW_FIXED_WIDTH, RuleWidget.WINDOW_FIXED_HEIGHT))
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.back_signal.emit())

        page_widget = QWidget(self)
        page_layout = QVBoxLayout(page_widget)
        page_layout.setContentsMargins(10, 0, 10, 10)
        page_layout.setSpacing(2)
        page_widget.setLayout(page_layout)

        text_browser = QTextBrowser(page_widget)
        text_browser.setFont(QFont("Source Han Sans SC Medium", 12))

        self.load_markdown_file(text_browser, "./README.md")

        page_layout.addWidget(text_browser)
        main_layout.addWidget(page_widget)

    def load_markdown_file(self, browser, file_path):
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