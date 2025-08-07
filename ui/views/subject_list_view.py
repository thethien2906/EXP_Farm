# ui/views/subject_list_view.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                             QListWidget, QPushButton)
from PyQt6.QtCore import pyqtSignal

class SubjectListView(QWidget):
    """
    Left pane
    Display subjects
    """

    # --- Custom Signal ---
    subjectSelected = pyqtSignal(str)

    def __init__(self):

        # Parent constructor
        super().__init__()

        # --- Create Widgets ---
        # Left Pane Header
        self.header_label = QLabel("KNOWLEDGE")
        self.header_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        # Subject List
        self.subjects_list = QListWidget()
        # Add Button
        self.add_subject_btn = QPushButton("Add New Subject")

        # --- Set up Layout ---
        # Vertical Layout
        main_layout = QVBoxLayout()
        # Stack Widgets
        main_layout.addWidget(self.header_label)
        main_layout.addWidget(self.subjects_list)
        main_layout.addWidget(self.add_subject_btn)
        # Apply Layout
        self.setLayout(main_layout)

        # --- Configure Signals ---
        self.subjects_list.currentTextChanged.connect(self._on_subject_selected)

    # Receive signal from subjects_list
    def _on_subject_selected(self, subject_name: str):
        """
        Handles the event when a subject is selected in the list
        :param subject_name: Name of selected subject
        :return: None
        """
        if subject_name:
            self.subjectSelected.emit(subject_name)


    # Public method for controller
    def populate_subjects(self,subjects: list):
        """
        AppLogic controller will call to fill the list with subject names
        :param subjects: Subject item list
        :return: None
        """
        # Clear list before adding new items
        self.subjects_list.clear()
        # Extract subject names to list
        subject_names = [subject.name for subject in subjects]
        self.subjects_list.addItems(subject_names)

