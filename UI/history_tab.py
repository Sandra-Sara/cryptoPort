"""
Local HistoryTab (H1) for CryptPort
Stores history locally per user in:
history/<email>.json
"""

import os
import json
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QHBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal


class HistoryTab(QWidget):
    """Local history viewer for each logged-in user"""
    back_requested = pyqtSignal()  # Go back to FileTab

    def __init__(self, user_email: str):
        super().__init__()
        self.user_email = user_email
        self.history_dir = os.path.join(os.getcwd(), "history")
        self.history_file = os.path.join(self.history_dir, f"{self.user_email}.json")

        os.makedirs(self.history_dir, exist_ok=True)

        self.init_ui()
        self.load_history()

    # ----------------------------------------------------
    # UI
    # ----------------------------------------------------
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

        subtitle = QLabel(f"Local history for: {self.user_email}")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # White rounded box
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

        # Button Row
        button_row = QHBoxLayout()
        button_row.setSpacing(20)
        button_row.setAlignment(Qt.AlignCenter)

        # Refresh
        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_refresh.setCursor(Qt.PointingHandCursor)
        btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #64B5F6;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #1E88E5; }
        """)
        btn_refresh.clicked.connect(self.load_history)

        # Clear
        btn_clear = QPushButton("🗑 Clear History")
        btn_clear.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #E57373;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        btn_clear.clicked.connect(self.clear_history)

        # Back
        btn_back = QPushButton("⬅ Back")
        btn_back.setFont(QFont("Segoe UI", 12, QFont.Bold))
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #81C784;
                color: white;
                border-radius: 8px;
                padding: 8px 25px;
            }
            QPushButton:hover { background-color: #388E3C; }
        """)
        btn_back.clicked.connect(self.back_requested.emit)

        button_row.addWidget(btn_refresh)
        button_row.addWidget(btn_clear)
        button_row.addWidget(btn_back)

        box_layout.addLayout(button_row)
        layout.addWidget(box)

    # ----------------------------------------------------
    # HISTORY FUNCTIONS
    # ----------------------------------------------------
    def load_history(self):
        """Load the user's own local history"""
        self.history_list.clear()

        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as f:
                json.dump({"records": []}, f, indent=4)

            self.history_list.addItem("No history yet.")
            return

        with open(self.history_file, "r") as f:
            data = json.load(f)

        records = data.get("records", [])

        if not records:
            self.history_list.addItem("No history yet.")
            return

        for rec in records:
            msg = f"[{rec['timestamp']}] {rec['type'].upper()} | {rec['filename']} | to {rec.get('to', '')} | from {rec.get('from', '')}"
            self.history_list.addItem(msg)

    def add_entry(self, entry_type: str, filename: str, to: str = None, from_user: str = None):
        """Add a new record for the user"""
        entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": entry_type,
            "filename": filename,
            "to": to,
            "from": from_user
        }

        # Read or init
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                data = json.load(f)
        else:
            data = {"records": []}

        data["records"].append(entry)

        # Write back
        with open(self.history_file, "w") as f:
            json.dump(data, f, indent=4)

        self.load_history()

    def clear_history(self):
        """Delete user's local history"""
        if QMessageBox.question(self, "Clear", "Clear all history?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            with open(self.history_file, "w") as f:
                json.dump({"records": []}, f, indent=4)
            self.history_list.clear()
            self.history_list.addItem("History cleared.")
