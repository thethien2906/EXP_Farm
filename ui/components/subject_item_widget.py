from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, pyqtSignal, QSize

class SubjectItemWidget(QWidget):
    """Custom widget for display subject"""
    def __init__(self, subject, parent=None):
        super().__init__(parent)
        self.subject = subject
        self.setup_ui()

    def setup_ui(self):
        """Subject Item component"""

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)

        # Icon
        self.icon_label = QLabel(self.subject.icon or "")
        self.icon_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.icon_label)

        # Name
        self.name_label = QLabel(self.subject.name)
        self.name_label.setStyleSheet("font-weight: bold; font-size: 14;")
        layout.addWidget(self.name_label)

        # Stretch
        layout.addStretch()

        # Background
        self.setStyleSheet("background-color: transparent;")

    @staticmethod
    def get_size_hint():
        """Return the suggested size for list items"""
        return QSize(0, 40)
