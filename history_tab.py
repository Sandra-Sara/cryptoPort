"""
HistoryTab – Reads history from Flask server instead of local files.
"""

import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QHBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal


class HistoryTab(QWidget):
    back_requested = pyqtSignal()

    def __init__(self, user_email: str):
        super().__init__()
        self.user_email = user_email
        self.server_url = "http://127.0.0.1:5000"

        self.init_ui()
        self.load_history()

    # -----------------------------------------------------------
    # UI
    # -----------------------------------------------------------
    def init_ui(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(25)

        title = QLabel("📜 File Transfer History")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel(f"History for: {self.user_email}")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Box
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #BBDEFB;
            }
        """)
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(25, 25, 25, 25)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                border: 1.5px solid #BBDEFB;
                border-radius: 10px;
                background-color: #FAFAFA;
                padding: 10px;
                font-size: 13px;
            }
        """)
        box_layout.addWidget(self.history_list)

        # Buttons
        button_row = QHBoxLayout()
        button_row.setSpacing(20)
        button_row.setAlignment(Qt.AlignCenter)

        # Refresh
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_refresh.clicked.connect(self.load_history)

        # Clear
        btn_clear = QPushButton("🗑 Clear History")
        btn_clear.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_clear.clicked.connect(self.clear_history)

        # Back
        btn_back = QPushButton("⬅ Back")
        btn_back.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_back.clicked.connect(self.back_requested.emit)

        button_row.addWidget(btn_refresh)
        button_row.addWidget(btn_clear)
        button_row.addWidget(btn_back)

        box_layout.addLayout(button_row)
        layout.addWidget(box)

    # -----------------------------------------------------------
    # Load History from Flask Server
    # -----------------------------------------------------------
    def load_history(self):
        self.history_list.clear()

        try:
            res = requests.get(f"{self.server_url}/history/{self.user_email}")

            if res.status_code != 200:
                self.history_list.addItem("Error loading history.")
                return

            records = res.json()

            if not records:
                self.history_list.addItem("No history yet.")
                return

            # Newest first
            for rec in reversed(records):
                line = f"[{rec['timestamp']}] {rec['action'].upper()} | {rec['filename']}"
                if "sender" in rec and rec["sender"]:
                    line += f" | from {rec['sender']}"
                self.history_list.addItem(line)

        except Exception as e:
            self.history_list.addItem("Error connecting to server.")
            print("History load error:", e)

    # -----------------------------------------------------------
    # Clear History on Server
    # -----------------------------------------------------------
    def clear_history(self):
        if QMessageBox.question(
            self, "Clear", "Clear all server history?",
            QMessageBox.Yes | QMessageBox.No
        ) == QMessageBox.Yes:

            try:
                res = requests.delete(f"{self.server_url}/history/{self.user_email}/clear")
                if res.status_code == 200:
                    self.history_list.clear()
                    self.history_list.addItem("History cleared.")
                else:
                    QMessageBox.warning(self, "Error", "Could not clear history.")

            except Exception as e:
                QMessageBox.warning(self, "Error", "Server not reachable.")
                print("Clear history error:", e)
