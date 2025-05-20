from PyQt6.QtCore import Qt

# Dark theme color palette inspired by Steam
COLORS = {
    "background_dark": "#171a21",
    "background_medium": "#1b2838",
    "background_light": "#2a3f5a",
    "text_normal": "#c7d5e0",
    "text_bright": "#ffffff",
    "accent_blue": "#1a9fff",
    "accent_blue_hover": "#66c0f4",
    "accent_green": "#5c7e10",
    "accent_green_hover": "#a4d007",
    "border_color": "#2a3f5a",
    "progress_bar_empty": "#1f3347",
    "progress_bar_filled": "#66c0f4",
    "progress_bar_border": "#4c5b6a",
    "button_normal": "#2a3f5a",
    "button_hover": "#3b5e86",
    "button_pressed": "#1a9fff",
}

# Main stylesheet that will be applied to the entire application
STEAM_STYLESHEET = f"""
/* Global Application Styles */
QWidget {{
    background-color: {COLORS["background_medium"]};
    color: {COLORS["text_normal"]};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 10pt;
}}

QMainWindow, QDialog {{
    background-color: {COLORS["background_dark"]};
}}

/* Frames */
QFrame {{
    border-radius: 4px;
}}

/* Group Box */
QGroupBox {{
    border: 1px solid {COLORS["border_color"]};
    border-radius: 4px;
    margin-top: 1em;
    padding-top: 10px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 3px;
}}

/* Labels */
QLabel {{
    color: {COLORS["text_normal"]};
}}

QLabel#HeaderLabel {{
    color: {COLORS["text_bright"]};
    font-size: 14pt;
    font-weight: bold;
}}

QLabel#SubHeaderLabel {{
    color: {COLORS["text_bright"]};
    font-size: 12pt;
    font-weight: bold;
}}

/* Push Buttons */
QPushButton {{
    background-color: {COLORS["button_normal"]};
    color: {COLORS["text_normal"]};
    border: 1px solid {COLORS["border_color"]};
    border-radius: 2px;
    padding: 5px 15px;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {COLORS["button_hover"]};
    color: {COLORS["text_bright"]};
}}

QPushButton:pressed {{
    background-color: {COLORS["button_pressed"]};
}}

QPushButton:disabled {{
    background-color: {COLORS["background_medium"]};
    color: #4c5b6a;
    border: 1px solid #1f2b3b;
}}

/* Primary Action Button */
QPushButton#PrimaryButton {{
    background-color: {COLORS["accent_blue"]};
    color: {COLORS["text_bright"]};
    font-weight: bold;
}}

QPushButton#PrimaryButton:hover {{
    background-color: {COLORS["accent_blue_hover"]};
}}

/* Start Session Button */
QPushButton#StartButton {{
    background-color: {COLORS["accent_green"]};
    color: {COLORS["text_bright"]};
    font-weight: bold;
}}

QPushButton#StartButton:hover {{
    background-color: {COLORS["accent_green_hover"]};
}}

/* Line Edit */
QLineEdit {{
    background-color: {COLORS["background_light"]};
    color: {COLORS["text_bright"]};
    border: 1px solid {COLORS["border_color"]};
    border-radius: 2px;
    padding: 3px;
}}

/* Progress Bar */
QProgressBar {{
    background-color: {COLORS["progress_bar_empty"]};
    color: {COLORS["text_bright"]};
    border: 1px solid {COLORS["progress_bar_border"]};
    border-radius: 2px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS["progress_bar_filled"]};
    border-radius: 2px;
}}

/* Scroll Areas */
QScrollArea {{
    border: none;
}}

/* List Widget */
QListWidget {{
    background-color: {COLORS["background_dark"]};
    alternate-background-color: {COLORS["background_medium"]};
    border: 1px solid {COLORS["border_color"]};
    border-radius: 2px;
}}

QListWidget::item {{
    padding: 5px;
    border-bottom: 1px solid {COLORS["border_color"]};
}}

QListWidget::item:selected {{
    background-color: {COLORS["accent_blue"]};
    color: {COLORS["text_bright"]};
}}

/* Tab Widget */
QTabWidget::pane {{
    border: 1px solid {COLORS["border_color"]};
    background-color: {COLORS["background_medium"]};
}}

QTabBar::tab {{
    background-color: {COLORS["background_dark"]};
    color: {COLORS["text_normal"]};
    padding: 8px 12px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    border: 1px solid {COLORS["border_color"]};
    border-bottom: none;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS["background_medium"]};
    color: {COLORS["text_bright"]};
}}

QTabBar::tab:hover {{
    background-color: {COLORS["background_light"]};
}}

/* Menu Bar */
QMenuBar {{
    background-color: {COLORS["background_dark"]};
    color: {COLORS["text_normal"]};
}}

QMenuBar::item {{
    background: transparent;
    padding: 5px 10px;
}}

QMenuBar::item:selected {{
    background-color: {COLORS["background_light"]};
    color: {COLORS["text_bright"]};
}}

/* Status Bar */
QStatusBar {{
    background-color: {COLORS["background_dark"]};
    color: {COLORS["text_normal"]};
    border-top: 1px solid {COLORS["border_color"]};
}}

/* Scroll Bar */
QScrollBar:vertical {{
    background: {COLORS["background_dark"]};
    width: 12px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: {COLORS["background_light"]};
    min-height: 20px;
    border-radius: 6px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS["accent_blue"]};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {COLORS["background_dark"]};
    height: 12px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background: {COLORS["background_light"]};
    min-width: 20px;
    border-radius: 6px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {COLORS["accent_blue"]};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""


def apply_steam_theme(app):
    """Apply Steam-like dark theme to the entire application"""
    app.setStyle("Fusion")  # Use Fusion style as a base
    app.setStyleSheet(STEAM_STYLESHEET)