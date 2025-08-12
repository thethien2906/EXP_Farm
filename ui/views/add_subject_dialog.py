# ui/views/add_subject_dialog.py

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QDialogButtonBox)


class AddSubjectDialog(QDialog):
    """
    Dialog window for adding new subject
    """
    def __init__(self):
        # Parent constructor
        super().__init__()

        # --- Dialog Configuration ---
        self.setWindowTitle("Add New Subject")
        self.setFixedSize(350, 350)

        # --- Create Widgets ---
        # Name
        self.name_label = QLabel("Subject Name:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., Python Programming")

        # Icon
        self.icon_label = QLabel("Icon (optional):")
        self.icon_input = QLineEdit()

        # Button
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)

        # --- Layout ---
        dialog_layout = QVBoxLayout()

        # Create layout for name fields
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.name_label)
        name_layout.addWidget(self.name_input)

        # Create layout for icon fields
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_label)
        icon_layout.addWidget(self.icon_input)

        # Add name and icon layout to main layout
        dialog_layout.addLayout(name_layout)
        dialog_layout.addLayout(icon_layout)

        # Add button to the bottom
        dialog_layout.addWidget(self.button_box)

        # Set main layout
        self.setLayout(dialog_layout)

        # --- Connect Signals ---
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def get_subject_data(self):
        """
        Helper method for retrieving data
        :return: A tuple containing subject name and icon
        """
        return self.name_input.text().strip(), self.icon_input.text().strip()
