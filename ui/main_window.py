### Placeholder version ###

# ui/main_window.py

# from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
#                              QLabel, QListWidget, QListWidgetItem, QPushButton,
#                              QProgressBar, QFrame, QSplitter)
# from PyQt6.QtCore import Qt, QSize
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.setWindowTitle("EXP FARM")
#
#         self.resize(1024, 768)
#
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#
#         main_layout = QHBoxLayout(central_widget)
#
#         # Splitter
#         splitter = QSplitter(Qt.Orientation.Horizontal)
#         main_layout.addWidget(splitter)
#
#         # Left pane
#         subjects_list_widget = QWidget()
#         subjects_layout = QVBoxLayout(subjects_list_widget)
#
#         subjects_header = QLabel("KNOWLEDGE")
#         subjects_header.setStyleSheet("font-weight: bold; font-size: 16px;")
#         subjects_layout.addWidget(subjects_header)
#
#         self.subjects_list = QListWidget()
#         subjects_layout.addWidget(self.subjects_list)
#
#         # Add button
#         add_subject_btn = QPushButton("+ Add New Subject")
#         subjects_layout.addWidget(add_subject_btn)
#
#         splitter.addWidget(subjects_list_widget)
#
#         # Right pane
#         details_widget = QWidget()
#         details_layout = QVBoxLayout(details_widget)
#         details_layout.setSpacing(50)
#         subject_header = QLabel("📚 Study")
#         subject_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         subject_header.setStyleSheet("font-weight: bold; font-size: 24px;")
#         details_layout.addWidget(subject_header)
#
#         # Progress
#         progress_frame = QFrame()
#         progress_layout = QHBoxLayout(progress_frame)
#         progress_layout.setSpacing(2)
#
#         # Level
#         level_label = QLabel("Level 5")
#         level_label.setStyleSheet("font-weight: bold; font-size: 14px;")
#         progress_layout.addWidget(level_label)
#
#         # Spacing
#         bar_button_layout = QHBoxLayout()
#         bar_button_layout.setSpacing(10)
#
#         # EXP bar
#         exp_bar = QProgressBar()
#         exp_bar.setMinimum(0)
#         exp_bar.setMaximum(100)
#         exp_bar.setValue(75)
#         exp_bar.setTextVisible(True)
#         exp_bar.setFormat("75% to Next Level")  # Only show percentage text inside
#         exp_bar.setMinimumHeight(30)  # Make the bar taller
#         bar_button_layout.addWidget(exp_bar, 4)  # Take 80% of width
#
#         # Start button
#         start_button = QPushButton("Start")
#         start_button.setMinimumHeight(50)
#         bar_button_layout.addWidget(start_button, 1)
#
#         progress_layout.addLayout(bar_button_layout)
#         details_layout.addWidget(progress_frame)
#
#         # Stats
#         stats_frame = QFrame()
#         stats_layout = QHBoxLayout(stats_frame)
#
#         # Last session date
#         last_session = QLabel("Last session: Today")
#         stats_layout.addWidget(last_session)
#
#         # Current streak
#         streak = QLabel("Streak: 3 days 🔥")
#         stats_layout.addWidget(streak)
#
#         # Total hours
#         total_hours = QLabel("Total: 124.5 hours")
#         stats_layout.addWidget(total_hours)
#
#         details_layout.addWidget(stats_frame)
#
#         # Push top
#         details_layout.addStretch()
#
#         splitter.addWidget(details_widget)
#
#         # Set the initial sizes of the splitter
#         splitter.setSizes([200, 800])
#


from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QSplitter)
from PyQt6.QtCore import Qt

# Main UI components
from .views.subject_list_view import SubjectListView
from .views.progression_view import ProgressionView
from .views.statistics_view import StatisticsView

# Controller
from .app_logic import AppLogic


class MainWindow(QMainWindow):
    """
    Main UI
    Arrange view components
    Bridge between controller and UI
    """
    def __init__(self):
        # Parent constructor
        super().__init__()

        # Main window's title
        self.setWindowTitle("EXP FARM")

        # Initial size
        self.resize(1024, 768)

        # --- Central Widget ---
        # Central widget as main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        # Vertical split
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # --- Instantiate UI Views ---
        self.subject_list_view = SubjectListView()
        self.progression_view = ProgressionView()
        self.statistics_view = StatisticsView()

        # --- Instantiate the Controller ---
        self.app_logic = AppLogic(self.subject_list_view, self.progression_view, self.statistics_view)

        # --- Assemble Layout ---
        # 1. Left pane
        splitter.addWidget(self.subject_list_view)
        # 2. Right pane
        # Main container
        right_pane_container = QWidget()
        right_layout = QVBoxLayout(right_pane_container)

        # Add widgets to container
        right_layout.addWidget(self.progression_view)
        right_layout.addWidget(self.statistics_view)

        # Add container to splitter
        splitter.addWidget(right_pane_container)

        # 3. Final layout setup
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(splitter)

        # Initial size ratio of splitter panes
        splitter.setSizes([250, 750])
