from typing import Optional, Dict, Any


def calculate_exp_for_level(level, base_exp=50000, exponent=1.25):
    """
    Calculate total EXP required to reach a specific level using exponential growth

    Formula: base_exp * exponent^(level-1)

    Args:
        level (int): Target level
        base_exp (int): Base EXP needed for level 1
        exponent (float): Growth rate (1.5 = 50% increase per level)

    Returns:
        int: Total EXP needed to reach this level
    """
    if level <= 1:
        return 0
    return int(base_exp * (exponent ** (level - 1)))


def calculate_level_from_exp(total_exp, base_exp=50000, exponent=1.25):
    """
    Calculate current level based on total EXP

    Args:
        total_exp (int): Total EXP accumulated
        base_exp (int): Base EXP for level 1
        exponent (float): Growth exponent

    Returns:
        int: Current level
    """
    if total_exp == 0:
        return 1

    level = 1
    while total_exp >= calculate_exp_for_level(level + 1, base_exp, exponent):
        level += 1
    return level


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
        next_level_exp = calculate_exp_for_level(current_level + 1)

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