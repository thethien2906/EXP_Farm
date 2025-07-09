# subject_manager.py
from datetime import datetime
from typing import Optional, List, Dict, Any
from .database import save_subject, load_all_subjects, delete_subject as db_delete_subject
from data.models import Subject


class SubjectManager:
    def __init__(self):
        self.subjects = load_all_subjects()

    def create_subject(self, name: str, icon: Optional[str] = None, image_path: Optional[str] = None) -> Subject:
        """Create a new subject and save it to database"""
        if self.get_subject_by_name(name) is not None:
            raise ValueError(f"Subject '{name}' already exists")

        # Create new subject and add to list
        new_subject = Subject(name, icon, image_path)
        self.subjects.append(new_subject)

        # Save to database
        save_subject(new_subject)

        self.refresh_subjects()

        return new_subject

    def get_all_subjects(self) -> List[Subject]:
        """Return list of all subjects with fresh data"""
        self.refresh_subjects()
        return self.subjects

    def get_subject_by_name(self, name: str) -> Optional[Subject]:
        """Find and return subject by name, or None if not found"""
        for subject in self.subjects:
            if subject.name == name:
                return subject
        return None

    def delete_subject(self, name: str) -> bool:
        """Remove subject by name from memory and database"""
        subject = self.get_subject_by_name(name)
        if subject:
            self.subjects.remove(subject)
            db_delete_subject(name)  # Remove from database
            return True
        return False

    def update_subject(self, name: str, **kwargs) -> bool:
        """Update subject properties. Return True if found and updated, False otherwise"""
        subject = self.get_subject_by_name(name)
        if subject:
            # Update only the properties that were passed
            for key, value in kwargs.items():
                if hasattr(subject, key):
                    setattr(subject, key, value)
            save_subject(subject)
            self.refresh_subjects()
            return True
        return False

    def refresh_subjects(self):
        """Reload all subjects from database to get latest data"""
        self.subjects = load_all_subjects()

