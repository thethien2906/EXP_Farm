# ui/views/statistics_view.py

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt
from data.models import Subject # Import the Subject class for type hinting
import datetime


class StatisticsView(QWidget):
    """
    Bottom-right section, display key stats of selected subject
    """
    def __init__(self):
        # Parent constructor
        super().__init__()

        # --- Create Widgets ---

        # Main container
        self.main_frame = QFrame(self)
        self.main_frame.setObjectName("StatisticsFrame")

        # Date label
        self.last_session_label = QLabel("Last session: N/A")
        self.last_session_label.setObjectName("StatLabel")

        # Streak label
        self.streak_label = QLabel("Streak: 0 days")
        self.streak_label.setObjectName("StatLabel")

        # Total hour label
        self.total_hours_label = QLabel("Total: 0.0 hours")
        self.total_hours_label.setObjectName("StatLabel")

        # --- Set Up Layout ---
        # Horizontal Box
        main_layout = QHBoxLayout(self.main_frame)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add labels
        main_layout.addWidget(self.last_session_label)
        main_layout.addWidget(self.streak_label)
        main_layout.addWidget(self.total_hours_label)

        # Main frame layout
        self_layout = QHBoxLayout(self)
        self_layout.addWidget(self.main_frame)
        self.setLayout(self_layout)

    # --- Public Methods ---
    def update_view(self, subject: Subject):
        """
        Update view with provided subject data
        :param subject: Subject object that containing needed data
        :return: None
        """
        if subject:
            # Update last session date
            if subject.last_session_date:
                # Convert to different format
                last_date = datetime.date.fromtimestamp(float(subject.last_session_date))
                today = datetime.date.today()
                yesterday = today - datetime.timedelta(days=1)

                # Display in human format
                if last_date == today:
                    date_str = "Today"
                elif last_date == yesterday:
                    date_str = "Yesterday"
                else:
                    date_str = last_date.strftime("%Y-%m-%d")
                self.last_session_label.setText(f"Last session: {date_str}")
            else:
                self.last_session_label.setText("Last Session: N/A")

            # Update Streak
            self.streak_label.setText(f"Streak: {subject.current_streak} days")

            # Update total hours
            self.total_hours_label.setText(f"Total hours: {round(subject.total_hours,1)}")

        else:
            self.last_session_label.setText("Last session: N/A")
            self.streak_label.setText("Streak: 0 days 🔥")
            self.total_hours_label.setText("Total: 0.0 hours")

