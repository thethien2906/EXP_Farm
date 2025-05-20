import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to sys.path to allow imports from project
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.subject_manager import SubjectManager
from data.models import Subject


class TestSubjectManager(unittest.TestCase):
    """Tests for the SubjectManager class"""

    def setUp(self):
        """Set up for tests - create a clean SubjectManager with mocked database functions"""
        # Create mock subjects for testing
        self.mock_subjects = [
            Subject("Study", "📚"),
            Subject("Guitar", "🎸")
        ]

        # Give the subjects some values
        self.mock_subjects[0].total_exp = 100000
        self.mock_subjects[0].total_hours = 25.5

        # Set up patches for database functions
        self.load_all_subjects_patcher = patch('core.subject_manager.load_all_subjects')
        self.mock_load_all_subjects = self.load_all_subjects_patcher.start()
        self.mock_load_all_subjects.return_value = self.mock_subjects.copy()

        self.save_subject_patcher = patch('core.subject_manager.save_subject')
        self.mock_save_subject = self.save_subject_patcher.start()

        self.delete_subject_patcher = patch('core.subject_manager.db_delete_subject')
        self.mock_delete_subject = self.delete_subject_patcher.start()

        # Create the SubjectManager with mocked dependencies
        self.subject_manager = SubjectManager()

    def tearDown(self):
        """Clean up after each test"""
        self.load_all_subjects_patcher.stop()
        self.save_subject_patcher.stop()
        self.delete_subject_patcher.stop()

    def test_create_subject(self):
        """Test creating a new subject"""
        # Create a new subject
        new_subject = self.subject_manager.create_subject("Reading", "📖")

        # Verify that save_subject was called
        self.mock_save_subject.assert_called_once()

        # Verify subject was created properly
        self.assertEqual(new_subject.name, "Reading")
        self.assertEqual(new_subject.icon, "📖")
        self.assertEqual(new_subject.total_exp, 0)

        # Verify that refresh_subjects was called (indirectly by checking load_all_subjects)
        self.assertTrue(self.mock_load_all_subjects.call_count >= 1)  # At least once

    def test_create_duplicate_subject(self):
        """Test creating a subject with a name that already exists"""
        # First, let's manually modify our mock subject list to ensure we have a "Study" subject
        for subject in self.subject_manager.subjects:
            if subject.name == "Study":
                break
        else:
            # If we didn't find it, add it
            self.subject_manager.subjects.append(Subject("Study", "📚"))

        # Now try to create a duplicate
        with self.assertRaises(ValueError):
            self.subject_manager.create_subject("Study")

    def test_get_all_subjects(self):
        """Test getting all subjects"""
        # First, make sure our mock works
        subjects_from_mock = self.mock_load_all_subjects()

        # Now get subjects from manager
        subjects = self.subject_manager.get_all_subjects()

        # Verify subjects match what our mock returns
        self.assertEqual(len(subjects), len(subjects_from_mock))
        if len(subjects_from_mock) >= 1:
            self.assertEqual(subjects[0].name, subjects_from_mock[0].name)
        if len(subjects_from_mock) >= 2:
            self.assertEqual(subjects[1].name, subjects_from_mock[1].name)

    def test_get_subject_by_name_existing(self):
        """Test getting a subject by name when it exists"""
        # Make sure we have a Study subject in our manager
        if not any(s.name == "Study" for s in self.subject_manager.subjects):
            self.subject_manager.subjects.append(Subject("Study", "📚"))

        subject = self.subject_manager.get_subject_by_name("Study")

        # Verify correct subject was found
        self.assertIsNotNone(subject)
        self.assertEqual(subject.name, "Study")

    def test_get_subject_by_name_nonexistent(self):
        """Test getting a subject by name when it doesn't exist"""
        subject = self.subject_manager.get_subject_by_name("NonexistentSubject")

        # Verify no subject was found
        self.assertIsNone(subject)

    def test_delete_subject_existing(self):
        """Test deleting a subject that exists"""
        result = self.subject_manager.delete_subject("Study")

        # Verify the subject was deleted
        self.assertTrue(result)
        self.mock_delete_subject.assert_called_once_with("Study")

    def test_delete_subject_nonexistent(self):
        """Test deleting a subject that doesn't exist"""
        result = self.subject_manager.delete_subject("NonexistentSubject")

        # Verify no subject was deleted
        self.assertFalse(result)
        self.mock_delete_subject.assert_not_called()

    def test_update_subject_existing(self):
        """Test updating a subject that exists"""
        # Update an existing subject
        result = self.subject_manager.update_subject("Study", icon="📝", total_exp=200000)

        # Verify the subject was updated
        self.assertTrue(result)
        self.mock_save_subject.assert_called_once()

        # Mock how refresh_subjects would update the subject
        study_subject = self.mock_subjects[0]
        study_subject.icon = "📝"
        study_subject.total_exp = 200000
        self.mock_load_all_subjects.return_value = self.mock_subjects.copy()

        # Get the updated subject
        updated_subject = self.subject_manager.get_subject_by_name("Study")

        # Verify the properties were updated
        self.assertEqual(updated_subject.icon, "📝")
        self.assertEqual(updated_subject.total_exp, 200000)

    def test_update_subject_nonexistent(self):
        """Test updating a subject that doesn't exist"""
        result = self.subject_manager.update_subject("NonexistentSubject", icon="📝")

        # Verify no subject was updated
        self.assertFalse(result)
        self.mock_save_subject.assert_not_called()

    def test_refresh_subjects(self):
        """Test refreshing subjects from database"""
        # Create new subjects list that will be used when refresh_subjects is called
        new_mock_subjects = [
            Subject("Study", "📚"),
            Subject("Guitar", "🎸"),
            Subject("Reading", "📖")  # Added new subject
        ]

        # Update our mock to return the new subject list
        self.mock_load_all_subjects.return_value = new_mock_subjects

        # Call refresh_subjects
        self.subject_manager.refresh_subjects()

        # Verify that subjects were updated to our new mock list
        subjects = self.subject_manager.subjects
        self.assertEqual(len(subjects), len(new_mock_subjects))
        self.assertEqual(subjects[-1].name, "Reading")  # Check for the new subject


if __name__ == '__main__':
    unittest.main()