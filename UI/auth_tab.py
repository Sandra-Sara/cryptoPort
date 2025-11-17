"""
Authentication tab UI components with landing page design
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QGroupBox, 
                           QLineEdit, QPushButton, QLabel, QHBoxLayout, QProgressBar,
                           QStackedWidget, QFrame)
from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QFont, QPixmap
from .loading_spinner import LoadingSpinner
from config import AppConfig

class AuthTab(QWidget):
    """Authentication tab widget with landing page design"""
    
    registration_requested = pyqtSignal(str, str, str, str)
    login_requested = pyqtSignal(str, str)
    logout_requested = pyqtSignal()
    api_host_changed = pyqtSignal(str)  # New signal for API host changes
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_animations()
    
    def setup_ui(self):
        """Setup the authentication UI with stacked pages"""
        layout = QVBoxLayout(self)
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Create pages
        self.landing_page = self.create_landing_page()
        self.login_page = self.create_login_page()
        self.registration_page = self.create_registration_page()
        self.authenticated_page = self.create_authenticated_page()
        
        # Add pages to stack
        self.stacked_widget.addWidget(self.landing_page)
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.registration_page)
        self.stacked_widget.addWidget(self.authenticated_page)
        
        # Start with landing page
        self.stacked_widget.setCurrentWidget(self.landing_page)
    
    def setup_animations(self):
        """Setup loading animations"""
        # Progress bar animation timer
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_value = 0
    
    def create_landing_page(self):
        """Create the landing/welcome page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        
        # Welcome section
        welcome_frame = QFrame()
        welcome_frame.setFrameStyle(QFrame.Box)
        welcome_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        welcome_layout = QVBoxLayout(welcome_frame)
        welcome_layout.setAlignment(Qt.AlignCenter)
        welcome_layout.setSpacing(20)
        
        # App title - Updated with SecureFile branding
        title_label = QLabel("SecureFile")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        welcome_layout.addWidget(title_label)
        
        # Subtitle - Updated with locker reference
        subtitle_label = QLabel("Your Digital Locker • Secure File Transfer")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; margin-bottom: 20px;")
        welcome_layout.addWidget(subtitle_label)
        
        layout.addWidget(welcome_frame)
        
        # Server Configuration section
        config_group = QGroupBox("Server Configuration")
        config_group.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
                padding-top: 15px;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #2c3e50;
            }
        """)
        config_layout = QFormLayout(config_group)
        config_layout.setSpacing(15)
        
        # API Host input
        self.api_host_input = QLineEdit()
        self.api_host_input.setText(AppConfig.API_HOST)
        self.api_host_input.setPlaceholderText("Enter API server hostname or IP")
        self.api_host_input.setMinimumHeight(35)
        self.api_host_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
        """)
        # Connect to update API config when changed
        self.api_host_input.textChanged.connect(self.on_api_host_changed)
        config_layout.addRow("API Host:", self.api_host_input)
        
        # API Port input
        self.api_port_input = QLineEdit()
        self.api_port_input.setText(AppConfig.API_PORT)
        self.api_port_input.setPlaceholderText("Enter API server port")
        self.api_port_input.setMinimumHeight(35)
        self.api_port_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                outline: none;
            }
        """)
        # Connect to update API config when changed
        self.api_port_input.textChanged.connect(self.on_api_port_changed)
        config_layout.addRow("API Port:", self.api_port_input)
        
        # Current API URL display
        self.api_url_label = QLabel(f"API URL: {AppConfig.get_api_url()}")
        self.api_url_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12px;
                padding: 5px;
                background-color: #ecf0f1;
                border-radius: 4px;
            }
        """)
        config_layout.addRow("Current URL:", self.api_url_label)
        
        layout.addWidget(config_group)
        
        # Action buttons section
        actions_frame = QFrame()
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setAlignment(Qt.AlignCenter)
        actions_layout.setSpacing(15)
        
        # Login button
        self.landing_login_btn = QPushButton("Login to Existing Account")
        self.landing_login_btn.setMinimumHeight(50)
        self.landing_login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        self.landing_login_btn.clicked.connect(self.show_login_page)
        actions_layout.addWidget(self.landing_login_btn)
        
        # Signup button
        self.landing_signup_btn = QPushButton("Create New Account")
        self.landing_signup_btn.setMinimumHeight(50)
        self.landing_signup_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.landing_signup_btn.clicked.connect(self.show_registration_page)
        actions_layout.addWidget(self.landing_signup_btn)
        
        layout.addWidget(actions_frame)
        layout.addStretch()
        
        return page
    
    def on_api_host_changed(self, text):
        """Handle API host input change"""
        # Update the AppConfig
        AppConfig.API_HOST = text.strip() or 'localhost'
        self.update_api_url_display()
        # Emit signal to notify other components
        self.api_host_changed.emit(AppConfig.API_HOST)
    
    def on_api_port_changed(self, text):
        """Handle API port input change"""
        # Update the AppConfig
        try:
            port = int(text.strip()) if text.strip().isdigit() else 8000
            AppConfig.API_PORT = str(port)
        except ValueError:
            AppConfig.API_PORT = '8000'
        self.update_api_url_display()
    
    def update_api_url_display(self):
        """Update the API URL display label"""
        # Rebuild the API_BASE_URL
        AppConfig.API_BASE_URL = f"http://{AppConfig.API_HOST}:{AppConfig.API_PORT}"
        self.api_url_label.setText(f"API URL: {AppConfig.get_api_url()}")
    
    def get_current_api_config(self):
        """Get current API configuration"""
        return {
            'host': self.api_host_input.text().strip() or 'localhost',
            'port': self.api_port_input.text().strip() or '8000',
            'url': AppConfig.get_api_url()
        }
    
    def create_login_page(self):
        """Create the login page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        
        # Header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.show_landing_page)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Current API URL info
        api_info_label = QLabel(f"Connecting to: {AppConfig.get_api_url()}")
        api_info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12px;
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 4px;
                border-left: 3px solid #3498db;
            }
        """)
        layout.addWidget(api_info_label)
        
        # Login form
        login_group = QGroupBox("Login to Your Account")
        login_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        login_layout = QFormLayout(login_group)
        login_layout.setSpacing(15)
        
        self.login_email_input = QLineEdit()
        self.login_email_input.setPlaceholderText("Enter your email address")
        self.login_email_input.setMinimumHeight(35)
        login_layout.addRow("Email:", self.login_email_input)
        
        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.Password)
        self.login_password_input.setPlaceholderText("Enter your password")
        self.login_password_input.setMinimumHeight(35)
        self.login_password_input.returnPressed.connect(self.on_login_clicked)
        login_layout.addRow("Password:", self.login_password_input)
        
        # Login button with loading state
        login_button_layout = QHBoxLayout()
        self.login_btn = QPushButton("Login")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 25px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.login_btn.clicked.connect(self.on_login_clicked)
        
        self.login_spinner = LoadingSpinner()
        self.login_spinner.hide()
        
        login_button_layout.addWidget(self.login_btn)
        login_button_layout.addWidget(self.login_spinner)
        login_button_layout.addStretch()
        
        login_layout.addRow(login_button_layout)
        
        layout.addWidget(login_group)
        layout.addStretch()
        
        return page
    
    def create_registration_page(self):
        """Create the registration page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(20)
        
        # Header with back button
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.clicked.connect(self.show_landing_page)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        header_layout.addWidget(back_btn)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Current API URL info
        api_info_label = QLabel(f"Connecting to: {AppConfig.get_api_url()}")
        api_info_label.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 12px;
                padding: 8px;
                background-color: #ecf0f1;
                border-radius: 4px;
                border-left: 3px solid #27ae60;
            }
        """)
        layout.addWidget(api_info_label)
        
        # Registration form
        register_group = QGroupBox("Create Your Account")
        register_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        register_layout = QFormLayout(register_group)
        register_layout.setSpacing(15)
        
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText("Choose a username")
        self.reg_username_input.setMinimumHeight(35)
        register_layout.addRow("Username:", self.reg_username_input)
        
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText("Enter your email address")
        self.reg_email_input.setMinimumHeight(35)
        register_layout.addRow("Email:", self.reg_email_input)
        
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        self.reg_password_input.setPlaceholderText("Create a strong password (min 6 characters)")
        self.reg_password_input.setMinimumHeight(35)
        register_layout.addRow("Password:", self.reg_password_input)
        
        self.reg_confirm_password_input = QLineEdit()
        self.reg_confirm_password_input.setEchoMode(QLineEdit.Password)
        self.reg_confirm_password_input.setPlaceholderText("Confirm your password")
        self.reg_confirm_password_input.setMinimumHeight(35)
        register_layout.addRow("Confirm Password:", self.reg_confirm_password_input)
        
        # Registration button with loading state
        reg_button_layout = QHBoxLayout()
        self.register_btn = QPushButton("Create Account")
        self.register_btn.setMinimumHeight(40)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 25px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.register_btn.clicked.connect(self.on_register_clicked)
        
        self.reg_spinner = LoadingSpinner()
        self.reg_spinner.hide()
        
        reg_button_layout.addWidget(self.register_btn)
        reg_button_layout.addWidget(self.reg_spinner)
        reg_button_layout.addStretch()
        
        register_layout.addRow(reg_button_layout)
        
        # Registration progress bar
        self.reg_progress = QProgressBar()
        self.reg_progress.setRange(0, 100)
        self.reg_progress.hide()
        self.reg_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #27ae60;
                border-radius: 3px;
            }
        """)
        register_layout.addRow("Progress:", self.reg_progress)
        
        layout.addWidget(register_group)
        layout.addStretch()
        
        return page
    
    def create_authenticated_page(self):
        """Create the authenticated status page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        
        # Status section
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Box)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #d5f4e6;
                border: 2px solid #27ae60;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        status_layout = QVBoxLayout(status_frame)
        status_layout.setAlignment(Qt.AlignCenter)
        status_layout.setSpacing(15)
        
        # Success icon/text
        success_label = QLabel("✓ Authentication Successful")
        success_font = QFont()
        success_font.setPointSize(18)
        success_font.setBold(True)
        success_label.setFont(success_font)
        success_label.setAlignment(Qt.AlignCenter)
        success_label.setStyleSheet("color: #27ae60; margin: 10px;")
        status_layout.addWidget(success_label)
        
        # Current user info
        self.current_user_label = QLabel("Logged in as: user@example.com")
        user_font = QFont()
        user_font.setPointSize(14)
        self.current_user_label.setFont(user_font)
        self.current_user_label.setAlignment(Qt.AlignCenter)
        self.current_user_label.setStyleSheet("color: #2c3e50; margin: 5px;")
        status_layout.addWidget(self.current_user_label)
        
        # Status message
        status_message = QLabel("You can now connect to the file server")
        status_message.setAlignment(Qt.AlignCenter)
        status_message.setStyleSheet("color: #7f8c8d; margin: 5px;")
        status_layout.addWidget(status_message)
        
        layout.addWidget(status_frame)
        
        # Logout button
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setMinimumHeight(40)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px 25px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.logout_btn.clicked.connect(self.logout_requested.emit)
        layout.addWidget(self.logout_btn, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        return page
    
    # Page navigation methods
    def show_landing_page(self):
        """Show the landing page"""
        self.stacked_widget.setCurrentWidget(self.landing_page)
    
    def show_login_page(self):
        """Show the login page"""
        self.stacked_widget.setCurrentWidget(self.login_page)
        self.login_email_input.setFocus()
    
    def show_registration_page(self):
        """Show the registration page"""
        self.stacked_widget.setCurrentWidget(self.registration_page)
        self.reg_username_input.setFocus()
    
    def show_authenticated_page(self):
        """Show the authenticated page"""
        self.stacked_widget.setCurrentWidget(self.authenticated_page)
    
    # Button click handlers
    def on_register_clicked(self):
        """Handle register button click with loading state"""
        self.set_registration_loading(True)
        
        username = self.reg_username_input.text().strip()
        email = self.reg_email_input.text().strip()
        password = self.reg_password_input.text()
        confirm_password = self.reg_confirm_password_input.text()
        
        self.registration_requested.emit(username, email, password, confirm_password)
    
    def on_login_clicked(self):
        """Handle login button click with loading state"""
        self.set_login_loading(True)
        
        email = self.login_email_input.text().strip()
        password = self.login_password_input.text()
        
        self.login_requested.emit(email, password)
    
    # Loading state methods
    def set_registration_loading(self, loading=True):
        """Set registration loading state"""
        if loading:
            self.register_btn.setText("Creating Account...")
            self.register_btn.setEnabled(False)
            self.reg_spinner.start()
            self.reg_progress.show()
            self.start_progress_animation(self.reg_progress)
        else:
            self.register_btn.setText("Create Account")
            self.register_btn.setEnabled(True)
            self.reg_spinner.stop()
            self.reg_progress.hide()
            self.stop_progress_animation()
    
    def set_login_loading(self, loading=True):
        """Set login loading state"""
        if loading:
            self.login_btn.setText("Logging in...")
            self.login_btn.setEnabled(False)
            self.login_spinner.start()
            
            # Disable input fields during login
            self.login_email_input.setEnabled(False)
            self.login_password_input.setEnabled(False)
        else:
            self.login_btn.setText("Login")
            self.login_btn.setEnabled(True)
            self.login_spinner.stop()
            
            # Re-enable input fields
            self.login_email_input.setEnabled(True)
            self.login_password_input.setEnabled(True)
    
    # Progress animation methods
    def start_progress_animation(self, progress_bar):
        """Start progress bar animation"""
        self.current_progress_bar = progress_bar
        self.progress_value = 0
        self.progress_timer.start(50)  # Update every 50ms
    
    def stop_progress_animation(self):
        """Stop progress bar animation"""
        self.progress_timer.stop()
        if hasattr(self, 'current_progress_bar'):
            self.current_progress_bar.setValue(0)
    
    def update_progress(self):
        """Update progress bar animation"""
        if hasattr(self, 'current_progress_bar'):
            self.progress_value = (self.progress_value + 2) % 100
            self.current_progress_bar.setValue(self.progress_value)
    
    # Utility methods
    def clear_registration_fields(self):
        """Clear registration input fields and reset loading state"""
        self.reg_username_input.clear()
        self.reg_email_input.clear()
        self.reg_password_input.clear()
        self.reg_confirm_password_input.clear()
        self.set_registration_loading(False)
    
    def set_login_email(self, email: str):
        """Pre-fill login email"""
        self.login_email_input.setText(email)
    
    def update_auth_status(self, authenticated: bool, username: str = ""):
        """Update authentication status and show appropriate page"""
        # Reset loading states
        self.set_login_loading(False)
        self.set_registration_loading(False)
        
        if authenticated:
            self.current_user_label.setText(f"Logged in as: {username}")
            self.show_authenticated_page()
        else:
            self.show_landing_page()
    
    def handle_auth_error(self):
        """Handle authentication error and reset loading states"""
        self.set_login_loading(False)
        self.set_registration_loading(False)