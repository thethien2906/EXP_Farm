import time
from .exp_engine import calculate_base_exp, apply_streak_bonus
from utils.time_helpers import seconds_to_human_readable


class SessionManager:
    def __init__(self):
        """Initialize the session manager with no active session"""
        self.current_session = None
        self.is_running = False

    def start_session(self, subject_name, streak_days=0):
        """
        Start a new session for the given subject

        Args:
            subject_name (str): Name of the subject (e.g., "Study", "Guitar")
            streak_days (int): Current streak for bonus calculation (default: 0)

        Returns:
            dict: Session info with start confirmation

        Raises:
            RuntimeError: If a session is already running
        """
        if self.is_running:
            raise RuntimeError("You need to stop your current session to start a new one")

        # Start the session
        self.current_session = {
            'subject': subject_name,
            'start_time': time.time(),
            'streak_days': streak_days
        }
        self.is_running = True

        return {
            'status': 'started',
            'subject': subject_name,
            'streak_days': streak_days,
            'start_time': self.current_session['start_time']
        }

    def stop_session(self):
        """
        Stop the current session and calculate EXP earned

        Returns:
            dict: Detailed breakdown of the session results

        Raises:
            RuntimeError: If no session is currently running
        """
        if not self.is_running:
            raise RuntimeError("No session is currently running")

        # Calculate session duration
        end_time = time.time()
        session_seconds = int(end_time-self.current_session['start_time'])

        # Calculate EXP
        base_exp = calculate_base_exp(session_seconds)
        total_exp = apply_streak_bonus(base_exp, self.current_session['streak_days'])
        bonus_exp = total_exp - base_exp
        bonus_percentage = round((bonus_exp / base_exp * 100)) if base_exp > 0 else 0

        # Prepare results
        results = {
            'subject': self.current_session['subject'],
            'duration_seconds': session_seconds,
            'duration_human': seconds_to_human_readable(session_seconds),
            'base_exp': base_exp,
            'bonus_exp': bonus_exp,
            'bonus_percentage': bonus_percentage,
            'total_exp': total_exp,
            'streak_days': self.current_session['streak_days']
        }

        # Reset session state
        self.current_session = None
        self.is_running = False

        return results

