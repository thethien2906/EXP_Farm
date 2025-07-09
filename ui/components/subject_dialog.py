# ui/components/subject_dialog.py
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QComboBox, QDialogButtonBox)
from PyQt6.QtCore import Qt


class AddSubjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Add New Subject")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        # Name input
        name_layout = QHBoxLayout()
        name_label = QLabel("Subject Name:")
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Icon selection
        icon_layout = QHBoxLayout()
        icon_label = QLabel("Icon:")
        self.icon_combo = QComboBox()

        # Add common emoji icons
        icons = [
            ("📚", "Books/Study"),
            ("🎨", "Art/Drawing"),
            ("🎸", "Guitar/Music"),
            ("💻", "Programming"),
            ("🏃", "Exercise"),
            ("📝", "Writing"),
            ("🧠", "Learning"),
            ("🌎", "Languages"),
            ("🔬", "Science"),
            ("🔢", "Math"),
            ("🎮", "Gaming"),
            ("📱", "App Development"),
            ("🍳", "Cooking"),
            ("🏋️", "Fitness")
        ]

        for icon, description in icons:
            self.icon_combo.addItem(f"{icon} {description}", icon)

        icon_layout.addWidget(icon_label)
        icon_layout.addWidget(self.icon_combo)
        layout.addLayout(icon_layout)

        # Button box for OK/Cancel
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                      QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_subject_data(self):
        """Return the data for the new subject"""
        name = self.name_input.text().strip()
        icon = self.icon_combo.currentData()

        return {
            "name": name,
            "icon": icon
        }