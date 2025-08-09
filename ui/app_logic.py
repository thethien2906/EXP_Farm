# ui/app_logic.py
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from core.subject_manager import SubjectManager
from core.session_manager import SessionManager
from ui.views.subject_list_view import SubjectListView
from ui.views.progression_view import ProgressionView
from ui.views.statistics_view import StatisticsView

class AppLogic(QObject):
    """
    The main controller of the application.
    Connects UI to backend
    """

    # --- Custom Signals ---
    # Update subject with new subject data
    subjectUpdated = pyqtSignal(object)

    def __init__(self, subject_list_view: SubjectListView, progression_view: ProgressionView,
                 statistics_view: StatisticsView):
        """
        :param subject_list_view: view for list of subjects
        :param progression_view: view for session progression
        :param statistics_view: view for subject stats
        """
        super().__init__()

        # --- Backend Managers ---
        self.subject_manager = SubjectManager()
        self.session_manager = SessionManager()

        # --- UI Views ---
        self.subject_list_view = subject_list_view
        self.progression_view = progression_view
        self.statistics_view = statistics_view

        # --- Timers ---
        self.session_timer = QTimer(self)
        self.session_timer.setInterval(1000)
        self.session_timer.timeout.connect(self._update_session_progress)

        # --- Connect Signals ---
        self.subject_list_view.subjectSelected.connect(self._on_subject_selected)
        self.progression_view.startClicked.connect(self._on_start_session)
        self.progression_view.stopClicked.connect(self._on_stop_session)
        self.subjectUpdated.connect(self.progression_view.update_view)
        self.subjectUpdated.connect(self.statistics_view.update_view)

        # --- Initial Data Load ---
        self.load_initial_data()

    def load_initial_data(self):
        """
        Loads initial data for application
        :return:
        """
        # Get all subjects
        subjects = self.subject_manager.get_all_subjects()
        # Populate subject list view with retrieved subjects
        self.subject_list_view.populate_subjects(subjects)

    def _on_subject_selected(self, subject_name: str):
        """
        Handles the event of selection of a subject in the list
        :param subject_name: Name of selected subject
        :return:
        """
        # Get selected subject
        subject = self.subject_manager.get_subject_by_name(subject_name)
        # Emit subjectUpdated signal to update UI
        self.subjectUpdated.emit(subject)

    def _on_start_session(self):
        """
        Handles the event when the start button is clicked
        :return:
        """
        selected_subject_name = self.subject_list_view.subjects_list.currentItem()
        if selected_subject_name:
            # Start new session
            self.session_manager.start_session(selected_subject_name)
            # Set session with "Active" status
            self.progression_view.set_session_active(True)
            # Start timer
            self.session_timer.start()

    def _on_stop_session(self):
        """
        Handles the event when the start button is clicked
        :return:
        """
        # Stop current session
        self.session_manager.stop_session()
        # Set session with "Inactive" status
        self.progression_view.set_session_active(False)
        # Stop timer
        self.session_timer.stop()
        # Hot reload subjects
        self.subject_manager.refresh_subjects()
        # Get current selected subject
        selected_subject_name = self.subject_list_view.subjects_list.currentItem()
        if selected_subject_name:
            # Retrieve subject
            subject = self.subject_manager.get_subject_by_name(selected_subject_name)
            # Emit subjectUpdated signal
            self.subjectUpdated.emit(subject)

    def _update_session_progress(self):
        """
        Update session in progression view
        :return:
        """
        progress_data = self.session_manager.get_session_progress()
        if progress_data:
            self.progression_view.update_session_progress(progress_data)
