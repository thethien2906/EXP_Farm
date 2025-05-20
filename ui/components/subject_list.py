from PyQt6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QLabel, QListWidget,
                             QListWidgetItem, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from core.subject_manager import SubjectManager
from ui.components.subject_dialog import AddSubjectDialog


class SubjectList(QListWidget):
    # Define a signal that will be emitted when a subject is selected
    subject_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Subject manager initialize
        self.subject_manager = SubjectManager()

        self.init_ui()

        self.load_subjects()

    def init_ui(self):
        """Initialize UI components"""
        layout = QVBoxLayout(self)

        # Header label
        header = QLabel("YOUR SKILLS")
        header.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(header)

        # Subject list widget
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.list_widget.itemClicked.connect(self.on_subject_selected)
        layout.addWidget(self.list_widget)

        # Add new subject button
        add_button = QPushButton("+ Add New Subject")
        add_button.clicked.connect(self.on_add_subject_clicked)
        layout.addWidget(add_button)

        self.setLayout(layout)

    def load_subjects(self):
        """Load all subjects from the database and display"""

        # Clear memory
        self.list_widget.clear()

        # Get subjects
        subjects = self.subject_manager.get_all_subjects()

        # Process items
        for subject in subjects:
            item = QListWidgetItem()
            display_text = f"{subject.icon} {subject.name}" if subject.icon else subject.name
            item.setText(display_text)
            item.setData(Qt.ItemDataRole.UserRole, subject.name)
            self.list_widget.addItem(item)

    def on_subject_selected(self, item):
        """Handle subject selection in the list"""
        subject_name = item.data(Qt.ItemDataRole.UserRole)
        self.subject_selected.emit(subject_name)

    def on_add_subject_clicked(self):
        """Handle add subject button click"""
        dialog = AddSubjectDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Get the data from the dialog
            subject_data = dialog.get_subject_data()

            # Validate the subject name
            if not subject_data["name"]:
                QMessageBox.warning(self, "Invalid Input", "Subject name cannot be empty!")
                return

            try:
                # Create the new subject
                new_subject = self.subject_manager.create_subject(
                    name=subject_data["name"],
                    icon=subject_data["icon"]
                )

                # Refresh the subject list
                self.load_subjects()

                # Select the new subject
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    if item.data(Qt.ItemDataRole.UserRole) == new_subject.name:
                        self.list_widget.setCurrentItem(item)
                        self.on_subject_selected(item)
                        break

            except ValueError as e:
                # Handle the case where the subject already exists
                QMessageBox.warning(self, "Error", str(e))

    def refresh(self):
        """Refresh the subject list from the database"""
        self.load_subjects()
