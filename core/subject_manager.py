from datetime import datetime
from typing import Optional, List, Dict, Any


def calculate_exp_for_level(level):
    """Calculate total EXP required to reach a specific level"""
    return 50000 + (level-1) * 5000


def calculate_level_from_exp(total_exp):
    """Calculate current level based on total EXP"""
    if total_exp == 0:
        return 1

    level = 1
    while total_exp >= calculate_exp_for_level(level):
        level += 1
    return level - 1


def calculate_exp_to_next_level(total_exp):
    """Calculate how much EXP needed to level up"""
    return calculate_exp_for_level(calculate_level_from_exp(total_exp) + 1) - total_exp


class Subject:
    def __init__(self, name: str, icon: Optional[str] = None, image_path: Optional[str] = None):
        self.name = name
        self.icon = icon
        self.image_path = image_path
        self.total_exp = 0
        self.total_hours = 0
        self.last_session_date = None
        self.current_streak = 0

    def get_current_level(self) -> int:
        """Return current level"""
        return calculate_level_from_exp(self.total_exp)

    def get_exp_for_next_level(self) -> int:
        """Return EXP needed to reach next level"""
        return calculate_exp_to_next_level(self.total_exp)


    def get_progress_percentage(self) -> float:
        """Return progress percentage to next level (0-100)"""
        current_level = self.get_current_level()
        current_level_exp = calculate_exp_for_level(current_level)
        next_level_exp = calculate_exp_to_next_level(current_level_exp + 1)

        progress_exp = self.total_exp - current_level_exp
        total_needed = next_level_exp - current_level_exp

        return (progress_exp / total_needed) * 100

    def add_exp(self, amount: int) -> None:
        """Add EXP to this subject"""
        self.total_exp += amount

    def to_dict(self) -> Dict[str, Any]:
        """Convert subject to dictionary for saving/loading"""
        return {
            'name': self.name,
            'icon': self.icon,
            'image_path': self.image_path,
            'total_exp': self.total_exp,
            'total_hours': self.total_hours,
            'last_session_date': self.last_session_date,
            'current_streak': self.current_streak,
        }


class SubjectManager:
    def __init__(self):
        self.subjects: List[Subject] = []

    def create_subject(self, name: str, icon: Optional[str] = None, image_path: Optional[str] = None) -> Subject:
        """Create a new subject and add it to the manager"""
        if self.get_subject_by_name(name) is not None:
            raise ValueError(f"Subject '{name}' already exists")

            # Create new subject and add to list
        new_subject = Subject(name, icon, image_path)
        self.subjects.append(new_subject)
        return new_subject

    def get_all_subjects(self) -> List[Subject]:
        """Return list of all subjects"""
        return self.subjects

    def get_subject_by_name(self, name: str) -> Optional[Subject]:
        """Find and return subject by name, or None if not found"""
        for subject in self.subjects:
            if subject.name == name:
                return subject
        return None


    def delete_subject(self, name: str) -> bool:
        """Remove subject by name. Return True if found and deleted, False otherwise"""
        subject = self.get_subject_by_name(name)
        if subject:
            self.subjects.remove(subject)
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
            return True
        return False