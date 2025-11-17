"""
Login window for existing users (CryptPort)
Styled consistently with Register & Server Configuration pages
Uses built-in emoji icons (no external image assets)
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton,
    QMessageBox, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette


class LoginWindow(QWidget):
    login_success = pyqtSignal(str)  # emits email on success
    go_register = pyqtSignal()       # emits when user clicks register

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Setup UI (same style as Register window)"""
        self.setWindowTitle("Login - CryptPort")
        self.setGeometry(200, 100, 1000, 700)

        # Background color (soft blue gradient)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)

        # --- Title ---
        title = QLabel("🔐 Welcome Back to CryptPort")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Secure access to your file sharing system")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray; font-weight: 500;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # --- Centered White Box ---
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 18px;
                border: 2px solid #BBDEFB;
            }
        """)
        box.setFixedWidth(550)
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(60, 50, 60, 50)
        box_layout.setSpacing(25)

        input_font = QFont("Segoe UI", 12)
        label_font = QFont("Segoe UI", 13, QFont.Bold)

        # ✅ Helper for consistent input rows
        def create_input_row(label_text, placeholder, echo=False):
            layout = QHBoxLayout()
            layout.setSpacing(15)

            label = QLabel(label_text)
            label.setFont(label_font)
            label.setAlignment(Qt.AlignRight)

            field = QLineEdit()
            field.setPlaceholderText(placeholder)
            field.setFont(input_font)
            field.setStyleSheet("""
                QLineEdit {
                    border: 1.5px solid #90CAF9;
                    border-radius: 10px;
                    padding: 10px 12px;
                    background-color: #FAFAFA;
                }
                QLineEdit:focus {
                    border: 2px solid #42A5F5;
                    background-color: white;
                }
            """)
            if echo:
                field.setEchoMode(QLineEdit.Password)

            layout.addWidget(label)
            layout.addWidget(field)
            return layout, field

        # --- Input Fields ---
        email_layout, self.email_input = create_input_row("📧 Email:", "Enter your email")
        pass_layout, self.password_input = create_input_row("🔑 Password:", "Enter password", echo=True)

        # --- Login Button ---
        self.login_button = QPushButton("Sign In")
        self.login_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)

        # --- Register Link ---
        self.register_button = QPushButton("Create a New Account")
        self.register_button.setFont(QFont("Segoe UI", 11))
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setStyleSheet("""
            QPushButton {
                color: #1E88E5;
                background: transparent;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #1565C0;
            }
        """)
        self.register_button.clicked.connect(self.go_register.emit)

        # --- Add Everything ---
        box_layout.addLayout(email_layout)
        box_layout.addLayout(pass_layout)
        box_layout.addSpacing(10)
        box_layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        box_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(box, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

    # =============================
    # ✅ Login Logic
    # =============================
    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Missing Info", "Please enter both email and password.")
            return

        if "@" not in email or len(password) < 3:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")
            return

        QMessageBox.information(self, "Login Successful", f"Welcome back, {email}!")
        self.login_success.emit(email)
        self.close()
