import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog,
    QMessageBox, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class EncryptionTab(QWidget):

    back_requested = pyqtSignal()

    def __init__(self, user_email="", parent=None):
        super().__init__(parent)

        self.user_email = user_email
        self.keys_dir = "keys"
        os.makedirs(self.keys_dir, exist_ok=True)

        self.private_key_path = os.path.join(self.keys_dir, f"{self.user_email}_private.pem")
        self.public_key_path = os.path.join(self.keys_dir, f"{self.user_email}_public.pem")

        # ----------------------------------------------------------
        self.setStyleSheet("background-color: #d6eaff;")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 20, 40, 40)
        main_layout.setSpacing(20)

        # ----------------------------------------------------------
        title = QLabel("🔐 Encryption / Decryption Panel")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # ----------------------------------------------------------
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border-radius: 18px;
                padding: 25px;
                border: 2px solid #e0e0e0;
            }
        """)
        card_layout = QVBoxLayout()
        card_layout.setSpacing(25)

        # ----------------------------------------------------------
        btn_encrypt = QPushButton("🟢 Encrypt a File")
        btn_encrypt.setFont(QFont("Segoe UI", 14))
        btn_encrypt.setCursor(Qt.PointingHandCursor)
        btn_encrypt.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 12px;
                padding: 14px;
            }
            QPushButton:hover { background-color: #43A047; }
        """)
        btn_encrypt.clicked.connect(self.encrypt_file)
        card_layout.addWidget(btn_encrypt)

        # ----------------------------------------------------------
        btn_decrypt = QPushButton("🔵 Decrypt Received File")
        btn_decrypt.setFont(QFont("Segoe UI", 14))
        btn_decrypt.setCursor(Qt.PointingHandCursor)
        btn_decrypt.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 12px;
                padding: 14px;
            }
            QPushButton:hover { background-color: #1E88E5; }
        """)
        btn_decrypt.clicked.connect(self.decrypt_file)
        card_layout.addWidget(btn_decrypt)

        # ----------------------------------------------------------
        # NEW BUTTON — open public key folder
        btn_open_key = QPushButton("📂 Open My Public Key Folder")
        btn_open_key.setFont(QFont("Segoe UI", 14))
        btn_open_key.setCursor(Qt.PointingHandCursor)
        btn_open_key.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border-radius: 12px;
                padding: 14px;
            }
            QPushButton:hover { background-color: #7B1FA2; }
        """)
        btn_open_key.clicked.connect(self.open_key_folder)
        card_layout.addWidget(btn_open_key)

        card.setLayout(card_layout)
        main_layout.addWidget(card)

        # ----------------------------------------------------------
        btn_back = QPushButton("⬅ Back")
        btn_back.setFont(QFont("Segoe UI", 14, QFont.Bold))
        btn_back.setCursor(Qt.PointingHandCursor)
        btn_back.setStyleSheet("""
            QPushButton {
                background-color: #E57373;
                color: white;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        btn_back.clicked.connect(self.back_requested.emit)
        main_layout.addWidget(btn_back)

        self.setLayout(main_layout)

        self.ensure_keys_exist()

    # ----------------------------------------------------------
    # NEW: Open folder containing keys
    # ----------------------------------------------------------
    def open_key_folder(self):
        os.startfile(self.keys_dir)

    # ----------------------------------------------------------
    def ensure_keys_exist(self):
        def generate():
            key = RSA.generate(2048)
            with open(self.private_key_path, "wb") as f:
                f.write(key.export_key())
            with open(self.public_key_path, "wb") as f:
                f.write(key.publickey().export_key())

        if not os.path.exists(self.private_key_path) or not os.path.exists(self.public_key_path):
            generate()
            return

        try:
            RSA.import_key(open(self.private_key_path, "rb").read())
            RSA.import_key(open(self.public_key_path, "rb").read())
        except:
            generate()

    # ----------------------------------------------------------
    def encrypt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
        if not file_path:
            return

        receiver_key_path, _ = QFileDialog.getOpenFileName(self, "Select Receiver PUBLIC Key (.pem)")
        if not receiver_key_path:
            QMessageBox.warning(self, "Error", "Receiver public key required.")
            return

        try:
            receiver_public_key = RSA.import_key(open(receiver_key_path, "rb").read())
        except:
            QMessageBox.critical(self, "Invalid Key", "Selected key is not a valid RSA public key.")
            return

        cipher = PKCS1_OAEP.new(receiver_public_key)
        data = open(file_path, "rb").read()

        chunk_size = 214
        encrypted = b""

        for i in range(0, len(data), chunk_size):
            encrypted += cipher.encrypt(data[i:i + chunk_size])

        out_path = file_path + ".enc"
        open(out_path, "wb").write(encrypted)

        QMessageBox.information(self, "Success", f"Encrypted file saved:\n{out_path}")

    # ----------------------------------------------------------
    def decrypt_file(self):
        enc_path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted File (.enc)")
        if not enc_path:
            return

        private_key = RSA.import_key(open(self.private_key_path, "rb").read())
        cipher = PKCS1_OAEP.new(private_key)

        data = open(enc_path, "rb").read()
        decrypted = b""

        chunk_size = 256
        for i in range(0, len(data), chunk_size):
            decrypted += cipher.decrypt(data[i:i + chunk_size])

        out = enc_path.replace(".enc", "_DECRYPTED")
        open(out, "wb").write(decrypted)

        QMessageBox.information(self, "Success", f"Decrypted file saved:\n{out}")
