APP_STYLES = """
QMainWindow {
    background-color: qlineargradient(
        spread:pad,
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #b7dcf8,
        stop:1 #e8f3fc
    );
    color: #333;
    font-family: 'Segoe UI', sans-serif;
}

/* --- Tabs --- */
QTabWidget::pane {
    border: none;
    background: transparent;
}

QTabBar::tab {
    background: transparent;
    color: #555;
    padding: 10px 22px;
    font-weight: 600;
    border: none;
}

QTabBar::tab:selected {
    color: #7AC70C;
    border-bottom: 3px solid #7AC70C;
}

/* --- Group Boxes (Panels) --- */
QGroupBox {
    background-color: #ffffff;
    border: 1px solid #dfe4ea;
    border-radius: 12px;
    margin: 10px;
    padding: 18px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #333;
    font-weight: bold;
}

/* --- Buttons --- */
QPushButton {
    background-color: #7AC70C;
    color: white;
    border: none;
    padding: 10px 28px;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #6ab000;
}

QPushButton:disabled {
    background-color: #cdebb0;
    color: #eee;
}

/* --- Inputs --- */
QLineEdit, QComboBox, QTextEdit {
    padding: 8px;
    border: 1px solid #dcdcdc;
    border-radius: 6px;
    background-color: #ffffff;
    color: #333;
}

QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
    border: 1px solid #7AC70C;
}

/* --- Text Areas --- */
QTextEdit {
    font-family: 'Consolas', monospace;
    font-size: 10pt;
}

/* --- Progress Bar --- */
QProgressBar {
    border: 1px solid #dfe4ea;
    border-radius: 6px;
    height: 20px;
    text-align: center;
    background-color: #f1f5f9;
    color: #333;
}

QProgressBar::chunk {
    background-color: #7AC70C;
    border-radius: 6px;
}
"""