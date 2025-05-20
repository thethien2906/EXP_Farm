import unittest
from unittest.mock import patch, MagicMock
import time
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to sys.path to allow imports from project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.session_manager import SessionManager
from core.exp_engine import calculate_base_exp, apply_streak_bonus
from utils.time_helpers import seconds_to_human_readable
from data.models import Subject


class TestSessionManager(unittest.TestCase):
    """Tests for the SessionManager class"""

    def setUp(self):
        """Set up for tests - create a clean SessionManager instance"""
        self.session_manager = SessionManager()

        # Mock subjects for testing
        self.mock_subjects = [
            Subject("Study"),
            Subject("Guitar")
        ]
        # Add some values to the mock subjects
        self.mock_subjects[0].last_session_date = time.time() - 86400  # Yesterday
        self.mock_subjects[0].current_streak = 2

        # Use patchers to avoid actual database calls
        self.load_all_subjects_patcher = patch('core.session_manager.load_all_subjects')
        self.mock_load_all_subjects = self.load_all_subjects_patcher.start()
        self.mock_load_all_subjects.return_value = self.mock_subjects

        self.save_session_patcher = patch('core.session_manager.save_session')
        self.mock_save_session = self.save_session_patcher.start()

        self.update_subject_patcher = patch('core.session_manager.update_subject_after_session')
        self.mock_update_subject = self.update_subject_patcher.start()

        self.calculate_streak_patcher = patch('core.session_manager.calculate_current_streak')
        self.mock_calculate_streak = self.calculate_streak_patcher.start()
        self.mock_calculate_streak.return_value = 2  # Default streak value for tests

    def tearDown(self):
        """Clean up after each test - stop all patchers"""
        self.load_all_subjects_patcher.stop()
        self.save_session_patcher.stop()
        self.update_subject_patcher.stop()
        self.calculate_streak_patcher.stop()

    def test_start_session(self):
        """Test starting a new session"""
        result = self.session_manager.start_session("Study")

        # Assertions
        self.assertTrue(self.session_manager.is_running)
        self.assertEqual(result['status'], 'started')
        self.assertEqual(result['subject'], 'Study')
        self.assertEqual(result['streak_days'], 2)
        self.assertIsNotNone(result['start_time'])

    def test_start_session_invalid_subject(self):
        """Test starting a session with an invalid subject name"""
        with self.assertRaises(ValueError):
            self.session_manager.start_session("InvalidSubject")

    def test_start_session_already_running(self):
        """Test attempting to start a session when one is already running"""
        self.session_manager.start_session("Study")

        with self.assertRaises(RuntimeError):
            self.session_manager.start_session("Guitar")

    def test_stop_session(self):
        """Test stopping a session and calculating results"""
        # Start a session with a mocked start time
        with patch('time.time') as mock_time:
            # First call to time.time() for start_time (10 seconds ago)
            mock_time.return_value = 1000
            self.session_manager.start_session("Study")

            # Second call to time.time() for end_time (current time)
            mock_time.return_value = 1010  # 10 seconds later

            # Mock the session_is_on_new_day method
            with patch.object(self.session_manager, 'session_is_on_new_day', return_value=True):
                result = self.session_manager.stop_session("Test notes")

        # Assertions
        self.assertFalse(self.session_manager.is_running)
        self.assertIsNone(self.session_manager.current_session)

        # Check result content
        self.assertEqual(result['subject'], 'Study')
        self.assertEqual(result['duration_seconds'], 10)  # Explicitly check for 10 seconds
        self.assertEqual(result['notes'], 'Test notes')

        # Verify that save_session was called
        self.mock_save_session.assert_called_once()

        # Verify that update_subject_after_session was called
        self.mock_update_subject.assert_called_once()

    def test_stop_session_no_session(self):
        """Test stopping when no session is running"""
        with self.assertRaises(RuntimeError):
            self.session_manager.stop_session()

    def test_get_session_progress(self):
        """Test getting progress of current session"""
        # Start a session with a mocked start time
        with patch('time.time') as mock_time:
            # First call to time.time() for start_time (15 seconds ago)
            mock_time.return_value = 1000
            self.session_manager.start_session("Study")

            # Second call to time.time() for current time when getting progress
            mock_time.return_value = 1015  # 15 seconds later

            progress = self.session_manager.get_session_progress()

        # Assertions
        self.assertEqual(progress['subject'], 'Study')
        self.assertEqual(progress['duration_seconds'], 15)  # Should be exactly 15 seconds
        self.assertEqual(progress['streak_days'], 2)
        self.assertIsNotNone(progress['duration_human'])
        self.assertIsNotNone(progress['current_exp'])

    def test_get_session_progress_no_session(self):
        """Test getting progress when no session is running"""
        progress = self.session_manager.get_session_progress()
        self.assertIsNone(progress)

    def test_session_is_on_new_day_true(self):
        """Test the session_is_on_new_day method when it's a new day"""
        self.session_manager.start_session("Study")

        # Mock subjects[0].last_session_date to be yesterday
        yesterday = time.time() - 86400  # 24 hours ago
        self.mock_subjects[0].last_session_date = yesterday

        # Should return True because the current session is today and last session was yesterday
        self.assertTrue(self.session_manager.session_is_on_new_day())

    def test_session_is_on_new_day_false(self):
        """Test the session_is_on_new_day method when it's the same day"""
        self.session_manager.start_session("Study")

        # Mock subjects[0].last_session_date to be today
        today = time.time() - 3600  # 1 hour ago (same day)
        self.mock_subjects[0].last_session_date = today

        # Should return False because both sessions are on the same day
        self.assertFalse(self.session_manager.session_is_on_new_day())

    def test_session_is_on_new_day_no_previous_session(self):
        """Test session_is_on_new_day when there's no previous session date"""
        self.session_manager.start_session("Study")

        # Set last_session_date to None to simulate no previous session
        self.mock_subjects[0].last_session_date = None

        # Should return True because there's no previous session
        self.assertTrue(self.session_manager.session_is_on_new_day())


if __name__ == '__main__':
    unittest.main()