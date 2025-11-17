"""
Main controller for CryptPort App
Handles:
 - Welcome → Register → Login → Config → Connection
 - Connection → FileTab → EncryptionTab / HistoryTab
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from ui.welcome_window import WelcomeWindow
from ui.register_window import RegisterWindow
from ui.login_window import LoginWindow
from ui.config_window import ConfigWindow
from ui.connection_tab import ConnectionTab


class ConnectionWindow(QMainWindow):
    """Main window holding ConnectionTab"""

    def __init__(self, controller, config_data=None):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("CryptPort - Server Connection")
        self.setGeometry(200, 100, 1000, 700)

        self.config_data = config_data or {}

        # MAIN UI HOLDER
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Inject config_data into ConnectionTab
        self.connection_tab = ConnectionTab(self.config_data)
        layout.addWidget(self.connection_tab)

        self.setCentralWidget(central_widget)

        # When connect button is clicked
        self.connection_tab.connect_btn.clicked.connect(self.try_open_file_tab)

        self.file_tab = None
        self.encryption_tab = None
        self.history_tab = None

    # -------------------------------------------------------------------
    # When connection is successful → open FileTab
    # -------------------------------------------------------------------
    def try_open_file_tab(self):
        if "server_ip" in self.config_data and "server_port" in self.config_data:
            self.open_file_tab()

    def open_file_tab(self):
        from ui.file_tab import FileTab

        user_email = self.config_data.get("email")
        private_key = self.config_data.get("private_key")  # ✔ Important

        self.file_tab = FileTab(user_email, private_key)  # ✔ Correct signature
        self.setCentralWidget(self.file_tab)

        # Correct signal connections
        self.file_tab.disconnect_requested.connect(self.return_to_config_window)
        self.file_tab.open_encryption_requested.connect(self.open_encryption_tab)
        self.file_tab.open_history_requested.connect(self.open_history_tab)

    # -------------------------------------------------------------------
    # ENCRYPTION TAB
    # -------------------------------------------------------------------
    def open_encryption_tab(self):
        from ui.encryption_tab import EncryptionTab

        user_email = self.config_data.get("email")
        private_key = self.config_data.get("private_key")

        self.encryption_tab = EncryptionTab(user_email, private_key)
        self.setCentralWidget(self.encryption_tab)

        self.encryption_tab.back_requested.connect(self.open_file_tab)

    # -------------------------------------------------------------------
    # HISTORY TAB
    # -------------------------------------------------------------------
    def open_history_tab(self):
        from ui.history_tab import HistoryTab

        user_email = self.config_data.get("email")

        self.history_tab = HistoryTab(user_email)
        self.setCentralWidget(self.history_tab)

        self.history_tab.back_requested.connect(self.open_file_tab)

    # -------------------------------------------------------------------
    # Return to config window
    # -------------------------------------------------------------------
    def return_to_config_window(self):
        self.close()
        self.controller.show_config_window()


# ======================================================================
# APP CONTROLLER (Controls all transitions)
# ======================================================================

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.welcome_window = None
        self.register_window = None
        self.login_window = None
        self.config_window = None
        self.connection_window = None

        self.config_data = {}  # Global shared app data

        self.show_welcome_window()

    # ------------------- 0. WELCOME -------------------
    def show_welcome_window(self):
        if self.welcome_window:
            self.welcome_window.close()

        self.welcome_window = WelcomeWindow()
        self.welcome_window.go_register.connect(self.show_register_window)
        self.welcome_window.go_login.connect(self.show_login_window)
        self.welcome_window.show()

    # ------------------- 1. REGISTER -------------------
    def show_register_window(self):
        if self.welcome_window:
            self.welcome_window.close()
        if self.register_window:
            self.register_window.close()

        self.register_window = RegisterWindow()
        self.register_window.register_success.connect(self.show_login_window)
        self.register_window.show()

    # ------------------- 2. LOGIN -------------------
    def show_login_window(self):
        if self.welcome_window:
            self.welcome_window.close()
        if self.login_window:
            self.login_window.close()

        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self._login_complete)
        self.login_window.go_register.connect(self.show_register_window)
        self.login_window.show()

    def _login_complete(self, email):
        """Store login email globally"""
        self.config_data["email"] = email
        self.show_config_window()

    # ------------------- 3. CONFIG -------------------
    def show_config_window(self):
        if self.login_window:
            self.login_window.close()
        if self.config_window:
            self.config_window.close()
        if self.connection_window:
            self.connection_window.close()

        self.config_window = ConfigWindow()
        self.config_window.config_complete.connect(self.show_connection_window)
        self.config_window.show()

    # ------------------- 4. CONNECTION -------------------
    def show_connection_window(self, config_data=None):
        if self.config_window:
            self.config_window.close()

        if config_data:
            # Merge config but keep stored email
            config_data["email"] = self.config_data.get("email")

            # ✔ PRIVATE KEY STORED GLOBALLY
            if "private_key" in config_data:
                self.config_data["private_key"] = config_data["private_key"]

            self.config_data = config_data

        self.connection_window = ConnectionWindow(self, self.config_data)
        self.connection_window.show()

    # ------------------- RUN APP -------------------
    def run(self):
        sys.exit(self.app.exec_())


# ======================================================================
# ENTRY
# ======================================================================
if __name__ == "__main__":
    controller = AppController()
    controller.run()
