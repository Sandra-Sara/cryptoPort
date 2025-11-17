"""
ConnectionTab for CryptPort
Handles:
 - Login (email + password)
 - Registration
 - RSA key generation
 - Server connection test (TCP raw socket)
 - Saving user config info for other tabs
"""

import os
import json
import socket
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


class ConnectionTab(QWidget):
    def __init__(self, config_data):
        super().__init__()
        self.config_data = config_data  
        self.config_path = "user_config.json"

        self.server_ip = ""
        self.server_port = ""

        self.init_ui()
        self.load_saved_config()

    # ---------------------------------------------------------
    # UI SETUP
    # ---------------------------------------------------------
    def init_ui(self):
        # BLUE background (same as File Tab)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)

        title = QLabel("🔐 CryptPort — Login & Connection")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # ---------------- LOGIN FIELDS ----------------
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.style_input(self.email_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.style_input(self.password_input)

        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)

        # ---------------- SERVER FIELDS ----------------
        self.server_ip_input = QLineEdit()
        self.server_ip_input.setPlaceholderText("Server IP (e.g., 192.168.1.5)")
        self.style_input(self.server_ip_input)

        self.server_port_input = QLineEdit()
        self.server_port_input.setPlaceholderText("Server Port (e.g., 5000)")
        self.style_input(self.server_port_input)

        layout.addWidget(self.server_ip_input)
        layout.addWidget(self.server_port_input)

        # Buttons row
        row = QHBoxLayout()

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login_user)

        self.register_btn = QPushButton("Register")
        self.register_btn.clicked.connect(self.register_user)

        self.connect_btn = QPushButton("Test Connection")
        self.connect_btn.clicked.connect(self.test_connection)

        # Styled buttons
        self.style_button(self.login_btn, "#42A5F5")     # Blue
        self.style_button(self.register_btn, "#66BB6A")  # Green
        self.style_button(self.connect_btn, "#E53935")   # 🔴 RED (your request)

        row.addWidget(self.login_btn)
        row.addWidget(self.register_btn)
        row.addWidget(self.connect_btn)

        layout.addLayout(row)

    # ---------------------------------------------------------
    # UI HELPERS
    # ---------------------------------------------------------
    def style_input(self, widget):
        widget.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #90CAF9;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
        """)

    def style_button(self, button, color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #0D47A1;
            }}
        """)

    # ---------------------------------------------------------
    # CONFIG LOADING / SAVING
    # ---------------------------------------------------------
    def load_saved_config(self):
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, "r") as f:
            saved = json.load(f)

        self.email_input.setText(saved.get("email", ""))
        self.server_ip_input.setText(saved.get("server_ip", ""))
        self.server_port_input.setText(str(saved.get("server_port", "")))

        self.config_data["private_key_path"] = saved.get("private_key_path", "")
        self.config_data["public_key_path"] = saved.get("public_key_path", "")

    def save_config(self):
        data = {
            "email": self.email_input.text(),
            "server_ip": self.server_ip_input.text(),
            "server_port": int(self.server_port_input.text()),
            "private_key_path": self.config_data.get("private_key_path", ""),
            "public_key_path": self.config_data.get("public_key_path", "")
        }

        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=4)

    # ---------------------------------------------------------
    # USER ACTIONS
    # ---------------------------------------------------------
    def register_user(self):
        email = self.email_input.text().strip()
        pw = self.password_input.text().strip()

        if not email or not pw:
            self.alert("Missing Fields", "Email and password required.")
            return

        private_key_path = f"keys/{email}_private.pem"
        public_key_path = f"keys/{email}_public.pem"

        os.makedirs("keys", exist_ok=True)

        if not os.path.exists(private_key_path):
            self.generate_rsa_keys(private_key_path, public_key_path)

        self.config_data["email"] = email
        self.config_data["private_key_path"] = private_key_path
        self.config_data["public_key_path"] = public_key_path

        self.save_config()
        self.alert("Success", "Registration completed and RSA keys generated.")

    def login_user(self):
        email = self.email_input.text().strip()
        pw = self.password_input.text().strip()

        if not email or not pw:
            self.alert("Login Failed", "Enter both email and password.")
            return

        private_key_path = f"keys/{email}_private.pem"

        if not os.path.exists(private_key_path):
            self.alert("Missing Keys", "No keys found. Register first.")
            return

        self.config_data["email"] = email
        self.config_data["private_key_path"] = private_key_path
        self.config_data["public_key_path"] = f"keys/{email}_public.pem"

        self.save_config()
        self.alert("Login Successful", f"Welcome back, {email}!")

    # ---------------------------------------------------------
    # CONNECTION TEST
    # ---------------------------------------------------------
    def test_connection(self):
        ip = self.server_ip_input.text().strip()
        port = self.server_port_input.text().strip()

        if not ip or not port:
            self.alert("Missing Data", "Enter server IP and port.")
            return

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, int(port)))
            sock.close()

            self.config_data["server_ip"] = ip
            self.config_data["server_port"] = int(port)

            self.save_config()
            self.alert("Connection Success", "Connected to the server!")

        except Exception as e:
            self.alert("Connection Error", str(e))

    # ---------------------------------------------------------
    # RSA KEYS
    # ---------------------------------------------------------
    def generate_rsa_keys(self, private_path, public_path):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        private_bytes = private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption()
        )

        public_key = private_key.public_key()
        public_bytes = public_key.public_bytes(
            serialization.Encoding.PEM,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(private_path, "wb") as f:
            f.write(private_bytes)

        with open(public_path, "wb") as f:
            f.write(public_bytes)

    # ---------------------------------------------------------
    # MISC
    # ---------------------------------------------------------
    def alert(self, title, msg):
        QMessageBox.information(self, title, msg)
