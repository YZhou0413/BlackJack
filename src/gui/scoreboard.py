from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QPushButton,
    QAbstractItemView
)
import pandas as pd

from PySide6.QtWidgets import QTableWidgetItem

class NumericItem(QTableWidgetItem):
    def __init__(self, text: str, value=None):
        super().__init__(str(text))

        value = int(value)

        self._num = int(value)

        self.setData(Qt.EditRole, self._num)
        self.setData(Qt.UserRole, self._num)

    def __lt__(self, other):
        if isinstance(other, QTableWidgetItem):
            other_num = other.data(Qt.EditRole)
            return self._num < int(other_num)

        return super().__lt__(other)

class Scoreboard(QWidget):
    back_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.load_scores()

    def _build_ui(self):
        title = QLabel("Scoreboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 18px;")

        self.table_top = QTableWidget(0, 3)
        self.table_top.setHorizontalHeaderLabels(["Username", "Score", "Best Score"])
        self.table_top.horizontalHeader().setStretchLastSection(True)
        self.table_top.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_top.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_top.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_top.setSortingEnabled(True)
        self.table_top.setStyleSheet("background-color: #f5f0dc;")

        shame_label = QLabel("Hall of Shame")
        shame_label.setAlignment(Qt.AlignCenter)
        shame_label.setStyleSheet("font-weight: bold; font-size: 18px;")

        self.table_shame = QTableWidget(0, 3)
        self.table_shame.setHorizontalHeaderLabels(["Username", "Score", "Best Score"])
        self.table_shame.horizontalHeader().setStretchLastSection(True)
        self.table_shame.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_shame.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_shame.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_shame.setSortingEnabled(True)
        self.table_shame.setStyleSheet("background-color: #f5f0dc;")


        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.back_signal.emit())

        layout = QVBoxLayout(self)
        layout.addWidget(title)
        layout.addWidget(self.table_top)
        layout.addWidget(shame_label)
        layout.addWidget(self.table_shame)
        layout.addWidget(back_btn)

    def load_scores(self):

        self.table_top.setRowCount(0)
        self.table_shame.setRowCount(0)

        df = pd.read_csv("users.csv", dtype=str, keep_default_na=False, encoding="utf-8")

        df["username"] = df["username"].astype(str).str.strip()
        df["score"] = df["score"].astype(str).str.strip()
        df["best_score"] = df["best_score"].astype(str).str.strip()

        df["score"] = pd.to_numeric(df["score"].str.replace(",", "", regex=False).replace({"": pd.NA}), errors="coerce")
        df["best_score"] = pd.to_numeric(df["best_score"].str.replace(",", "", regex=False).replace({"": pd.NA}), errors="coerce")
        
        # disable sorting while filling
        self.table_top.setSortingEnabled(False)
        self.table_shame.setSortingEnabled(False)

        df_top = df[df["score"] > 0].sort_values("score", ascending=False)
        self.table_top.setSortingEnabled(False)
        for _, row in df_top.iterrows():
            self._append_row(self.table_top, row["username"], row["score"], row["best_score"])


        df_shame = df[df["score"] == 0].sort_values("username", ascending=True)
        for _, row in df_shame.reset_index(drop=True).iterrows():
            self._append_row(self.table_shame, str(row["username"]), "0", str(int(row["best_score"])))

        self.table_top.setSortingEnabled(True)
        self.table_top.sortItems(1, Qt.DescendingOrder)
        self.table_shame.setSortingEnabled(True)

    def _append_row(self, table: QTableWidget, username: str, score: str, best: str):
        r = table.rowCount()
        table.insertRow(r)

        item0 = QTableWidgetItem(username)


        score_val = int(str(score))

        best_val = int(str(best))


        item1 = NumericItem(str(score_val), score_val)
        item2 = NumericItem(str(best_val), best_val)

        table.setItem(r, 0, item0)
        table.setItem(r, 1, item1)
        table.setItem(r, 2, item2)

