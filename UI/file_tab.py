import os
import requests
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QMessageBox, QListWidget, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal


class FileTab(QWidget):
    # Required signals for main.py
    disconnect_requested = pyqtSignal()
    open_encryption_requested = pyqtSignal()
    open_history_requested = pyqtSignal()

    def __init__(self, user_email="", private_key="", parent=None):
        super().__init__(parent)

        self.user_email = user_email
        self.private_key = private_key
        self.server_url = "http://127.0.0.1:5000"

        self.selected_file = None

        # UI SETUP ----------------------------------------------------
        self.setStyleSheet("background-color: #d6eaff;")
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 20, 40, 40)
        layout.setSpacing(20)

        # Title
        title = QLabel(f"📁 File Transfer Panel")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Receiver name/email (not IP)
        ip_frame = QFrame()
        ip_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #e0e0e0;
            }
        """)
        ip_layout = QVBoxLayout()

        lbl_ip = QLabel("Receiver Email:")
        lbl_ip.setFont(QFont("Segoe UI", 12))

        self.receiver_box = QLineEdit()
        self.receiver_box.setPlaceholderText("example@gmail.com")
        self.receiver_box.setFont(QFont("Segoe UI", 12))
        self.receiver_box.setStyleSheet(
            "padding: 8px; border-radius: 10px; border: 1px solid gray;"
        )

        ip_layout.addWidget(lbl_ip)
        ip_layout.addWidget(self.receiver_box)
        ip_frame.setLayout(ip_layout)
        layout.addWidget(ip_frame)

        # File Selection + Upload
        send_frame = QFrame()
        send_frame.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 15px;
                padding: 20px;
                border: 2px solid #e0e0e0;
            }
        """)
        send_layout = QVBoxLayout()

        self.choose_file_btn = QPushButton("📂 Choose File")
        self.choose_file_btn.setFont(QFont("Segoe UI", 14))
        self.choose_file_btn.setStyleSheet(
            "background-color: #2196F3; color: white; padding: 10px; border-radius: 10px;"
        )
        self.choose_file_btn.clicked.connect(self.select_file)
        send_layout.addWidget(self.choose_file_btn)

        self.selected_file_label = QLabel("No file selected")
        self.selected_file_label.setFont(QFont("Segoe UI", 12))
        send_layout.addWidget(self.selected_file_label)

        send_btn = QPushButton("📤 Upload File")
        send_btn.setFont(QFont("Segoe UI", 14))
        send_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; padding: 10px; border-radius: 10px;"
        )
        send_btn.clicked.connect(self.upload_file)
        send_layout.addWidget(send_btn)

        send_frame.setLayout(send_layout)
        layout.addWidget(send_frame)

        # -------------------------------
        # File History List
        # -------------------------------
        history_label = QLabel("📜 Received File History")
        history_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("padding: 10px; border-radius: 8px;")
        layout.addWidget(self.history_list)

        # Load history data
        self.load_history()

        # Bottom buttons ---------------------------------------------------
        actions = QHBoxLayout()

        btn_history = QPushButton("📜 Open History")
        btn_history.setFont(QFont("Segoe UI", 13))
        btn_history.clicked.connect(lambda: self.open_history_requested.emit())
        actions.addWidget(btn_history)

        btn_encrypt = QPushButton("🔐 Open Encryption Panel")
        btn_encrypt.setFont(QFont("Segoe UI", 13))
        btn_encrypt.clicked.connect(lambda: self.open_encryption_requested.emit())
        actions.addWidget(btn_encrypt)

        btn_disconnect = QPushButton("⬅ Disconnect")
        btn_disconnect.setFont(QFont("Segoe UI", 13, QFont.Bold))
        btn_disconnect.clicked.connect(lambda: self.disconnect_requested.emit())
        actions.addWidget(btn_disconnect)

        layout.addLayout(actions)

        self.setLayout(layout)

    # ---------------------------------------------------------------------
    # Select a file
    # ---------------------------------------------------------------------
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.selected_file = file_path
            self.selected_file_label.setText(os.path.basename(file_path))

    # ---------------------------------------------------------------------
    # Upload file → Flask server
    # ---------------------------------------------------------------------
    def upload_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file first.")
            return

        receiver = self.receiver_box.text().strip()
        if receiver == "":
            QMessageBox.warning(self, "Error", "Receiver email is required.")
            return

        try:
            files = {"file": open(self.selected_file, "rb")}
            data = {"receiver": receiver, "sender": self.user_email}

            res = requests.post(f"{self.server_url}/upload", files=files, data=data)

            if res.status_code == 200:
                QMessageBox.information(self, "Success", "File uploaded successfully!")
                self.load_history()
            else:
                QMessageBox.critical(self, "Upload Failed", res.text)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ---------------------------------------------------------------------
    # Load history = list files stored for this email
    # ---------------------------------------------------------------------
    def load_history(self):
        self.history_list.clear()

        try:
            res = requests.get(f"{self.server_url}/list/{self.user_email}")

            if res.status_code == 200:
                files = res.json().get("files", [])
                for f in files:
                    self.history_list.addItem(f)

        except:
            pass
