from PyQt6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QLabel, QListWidget,
                             QListWidgetItem, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from core.subject_manager import SubjectManager
from .subject_item_widget import SubjectItemWidget


class SubjectList(QListWidget):
    # Define a signal that will be emitted when a subject is selected
    subject_selected = pyqtSignal(str)
    add_subject_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Subject manager initialize
        self.subject_manager = SubjectManager()

        self.setup_ui()

        self.load_subjects()

    def setup_ui(self):
        """Set up List"""
        layout = QVBoxLayout(self)

        # Header
        header = QLabel("SKILLS")
        header.setStyleSheet("font-weight: bold; font-size: 16px;")
        layout.addWidget(header)

        # Subject list
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.list_widget.setStyleSheet("""
                    QListWidget {
                        border: none;
                        background-color: #2b2b2b;
                    }
                    QListWidget::item {
                        border-bottom: 1px solid #3a3a3a;
                        padding: 2px;
                    }
                    QListWidget::item:selected {
                        background-color: #3a3a3a;
                    }
                """)

        # Signal hearing
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)

        # Add button
        self.add_button = QPushButton("+ Add New Subject")
        self.add_button.setStyleSheet("""
                    QPushButton {
                        background-color: #4a4a4a;
                        color: white;
                        border: none;
                        padding: 8px;
                        border-radius: 2px;
                    }
                    QPushButton:hover {
                        background-color: #5a5a5a;
                    }
                """)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        layout.addWidget(self.add_button)

    def load_subjects(self):
        """Load data"""
        self.list_widget.clear()

        subjects = self.subject_manager.get_all_subjects()

        # Add each subject to list
        for subject in subjects:
            item = QListWidgetItem()
            item.setSizeHint(SubjectItemWidget.get_size_hint())
            self.list_widget.addItem(item)
            widget = SubjectItemWidget(subject)
            self.list_widget.setItemWidget(item, widget)

    def on_item_clicked(self, item):
        """Handle item selection"""
        widget = self.list_widget.itemWidget(item)
        # Emit subject selected signal
        self.subject_selected.emit(widget.subject.name)

    def on_add_button_clicked(self):
        """handle add button click"""
        # Emit the signal only
        self.add_subject_clicked.emit()

    def refresh(self):
        """Refresh the list"""
        self.load_subjects()

    def select_subject(self, subject_name):
        """Choose the given subject by name"""
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(1)
            widget = self.list_widget.itemWidget(item)

            if widget.subject.name == subject_name:
                # Select this item
                self.list_widget.setCurrentItem(item)
                # Emit signal
                self.subject_selected.emit(subject_name)
                break