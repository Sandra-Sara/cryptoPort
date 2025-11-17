"""
Welcome window for CryptPort
Displays app introduction + Register & Login buttons
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette, QPixmap


class WelcomeWindow(QWidget):
    """The first screen shown when launching the app"""
    go_register = pyqtSignal()
    go_login = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Welcome to CryptPort")
        self.setGeometry(200, 100, 1000, 700)

        # Background color (soft gradient blue)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(35)

        # --- Title ---
        title = QLabel("🚀 Welcome to cryptPort")
        title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Your Secure File Transfer & Encryption Hub 🔒")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray; font-weight: 500;")

        # --- Info Frame ---
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 2px solid #BBDEFB;
            }
        """)
        info_box.setFixedWidth(600)
        info_layout = QVBoxLayout(info_box)
        info_layout.setContentsMargins(40, 40, 40, 40)
        info_layout.setSpacing(15)

        description = QLabel(
            "cryptPort lets you securely share, encrypt, and decrypt your files over a trusted connection.\n\n"
            "Key Features:\n"
            "• Fast and secure file transfer\n"
            "• AES-based file encryption & decryption\n"
            "• Local file history management\n"
            "• Simple, clean, and modern interface"
        )
        description.setFont(QFont("Segoe UI", 12))
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        info_layout.addWidget(description)

        # --- Buttons ---
        register_btn = QPushButton("Create an Account")
        register_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border-radius: 12px;
                padding: 12px 25px;
            }
            QPushButton:hover { background-color: #1E88E5; }
            QPushButton:pressed { background-color: #1565C0; }
        """)
        register_btn.clicked.connect(self.go_register.emit)

        login_btn = QPushButton("Login to Account")
        login_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #1E88E5;
                border: 2px solid #42A5F5;
                border-radius: 12px;
                padding: 12px 25px;
            }
            QPushButton:hover { background-color: #E3F2FD; }
        """)
        login_btn.clicked.connect(self.go_login.emit)

        # Add widgets
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(info_box, alignment=Qt.AlignCenter)
        main_layout.addWidget(register_btn, alignment=Qt.AlignCenter)
        main_layout.addWidget(login_btn, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)
