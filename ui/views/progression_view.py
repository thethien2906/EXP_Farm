# ui/views/progression_view.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QProgressBar, QPushButton, QFrame)
from PyQt6.QtCore import pyqtSignal, Qt


class ProgressionView(QWidget):
    """
    Top-right section of the UI
    """

    # --- Custom Signals ---
    # Emit when user clicks "Start" button
    startClicked = pyqtSignal()
    # Emit when user clicks "Stop" button
    stopClicked = pyqtSignal()

    def __init__(self):
        """
        Constructor for the ProgressionView
        """

        # Parent constructor
        super().__init__()

        # --- Create Widgets ---
        # Main container
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("ProgressionFrame")

        # Current level
        self.level_label = QLabel("Level 1")
        self.level_label.setObjectName("SubHeaderLabel")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Progress bar
        self.exp_progress_bar = QProgressBar()
        self.exp_progress_bar.setMinimum(0)
        self.exp_progress_bar.setMaximum(100)
        self.exp_progress_bar.setValue(0)
        self.exp_progress_bar.setTextVisible(True)
        self.exp_progress_bar.setFormat("%p% to Next level")
        self.exp_progress_bar.setMinimumHeight(30)

        # Action button
        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.setObjectName("StartButton")
        self.start_stop_button.setMinimumHeight(40)
        self.start_stop_button.setEnabled(False)

        # --- Set up Layout ---
        # Main layout
        main_layout = QVBoxLayout(self)

        # Row arrangement
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)

        # Add widgets
        controls_layout.addWidget(self.level_label, 1)
        controls_layout.addWidget(self.exp_progress_bar, 4)
        controls_layout.addWidget(self.start_stop_button, 1)

        # Add horizontal layout to bigger vertical layout
        frame_layout = QVBoxLayout(self.main_frame)
        frame_layout.addLayout(controls_layout)

        # Add main frame to main layout
        main_layout.addWidget(self.main_frame)
        self.setLayout(main_layout)

        # --- Configure Signals ---
        self.start_stop_button.clicked.connect(self._on_start_stop_clicked)

    def _on_start_stop_clicked(self):
        """
        Handles button click event (Start/Stop)
        :return: None
        """
        if self.start_stop_button.text() == "Start":
            self.startClicked.emit()
        else:
            self.stopClicked.emit()

    # --- Public Methods ---

    def update_view(self, subject):
        """
        Updates relevant widgets with provided data of processed subject
        :param subject: The subject object containing the data to display
        :return: None
        """
        if subject:
            # Level
            self.level_label.setText(f"Level {subject.get_current_level()}")
            # Progress
            progress_percentage = subject.get_progress_percentage()
            self.exp_progress_bar.setValue(int(progress_percentage))
            self.exp_progress_bar.setFormat(f"{progress_percentage:.1f}% to Next Level")
            # Enable Start button
            self.start_stop_button.setEnabled(True)
        else:
            self.level_label.setText("Level 1")
            self.exp_progress_bar.setValue(0)
            self.exp_progress_bar.setFormat("Select a Subject")
            self.start_stop_button.setEnabled(False)

    def set_session_active(self, active: bool):
        """
        Changes the state of view
        :param active: True if session is running, False if session is offline
        :return:
        """
        if active:
            self.start_stop_button.setText("Stop")
            self.start_stop_button.setObjectName("StopButton")
        else:
            self.start_stop_button.setText("Start")
            self.start_stop_button.setObjectName("StartButton")

        # Re-apply stylesheet for object name changes
        self.style().polish(self.start_stop_button)

    def update_session_progress(self, progress_data: dict):
        """
        Updates with new data from ongoing session
        :param progress_data: duration and current_exp
        :return: None
        """
        duration = progress_data.get('duration_human', '0s')
        exp = progress_data.get('current_exp', 0)
        self.exp_progress_bar.setFormat(f"{duration} | +{exp:,} EXP")
