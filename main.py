import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.styles.steam_theme import apply_steam_theme


def main():
    """Main entry point for the application"""
    # Create application
    app = QApplication(sys.argv)
    
    # Apply Steam theme
    apply_steam_theme(app)
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
