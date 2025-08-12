# core/session_manager.py
import time
from .exp_engine import calculate_base_exp, apply_streak_bonus
from utils.time_helpers import seconds_to_human_readable
from .database import save_session, update_subject_after_session, load_all_subjects, calculate_current_streak


class SessionManager:
    def __init__(self):
        """Initialize the session manager with no active session"""
        self.current_session = None
        self.is_running = False

    def start_session(self, subject_name):
        """Start a new session for the given subject"""
        if self.is_running:
            raise RuntimeError("You need to stop your current session to start a new one")

        # Check if subject exists
        subjects = load_all_subjects()
        if not any(s.name == subject_name for s in subjects):
            raise ValueError(f"Subject '{subject_name}' does not exist")

        # Calculate the actual current streak
        streak_days = calculate_current_streak(subject_name)

        # Start the session
        start_time = time.time()
        self.current_session = {
            'subject': subject_name,
            'start_time': start_time,
            'streak_days': streak_days
        }
        self.is_running = True

        return {
            'status': 'started',
            'subject': subject_name,
            'streak_days': streak_days,
            'start_time': start_time
        }

    def stop_session(self, notes=""):
        """Stop the current session, calculate EXP, and save to database"""
        if not self.is_running:
            raise RuntimeError("No session is currently running")

        # Calculate session duration
        end_time = time.time()
        session_seconds = int(end_time - self.current_session['start_time'])

        # Calculate EXP
        base_exp = calculate_base_exp(session_seconds)
        total_exp = apply_streak_bonus(base_exp, self.current_session['streak_days'])
        bonus_exp = total_exp - base_exp
        bonus_percentage = round((bonus_exp / base_exp * 100)) if base_exp > 0 else 0

        # Streak logic - only increment if this is a new day
        # streak_before = self.current_session['streak_days']
        # if self.session_is_on_new_day():
        #     new_streak = streak_before + 1
        # else:
        #     new_streak = streak_before
        new_streak = self.current_session['streak_days']

        # Prepare results
        results = {
            'subject': self.current_session['subject'],
            'start_time': self.current_session['start_time'],
            'end_time': end_time,
            'duration_seconds': session_seconds,
            'duration_human': seconds_to_human_readable(session_seconds),
            'base_exp': base_exp,
            'bonus_exp': bonus_exp,
            'bonus_percentage': bonus_percentage,
            'total_exp': total_exp,
            'streak_days': new_streak,  # Use the updated streak
            'notes': notes
        }

        # Save session to database
        save_session(results)

        # Update subject's total EXP and hours with the new streak
        update_subject_after_session(
            self.current_session['subject'],
            total_exp,
            session_seconds / 3600,
            new_streak  # Pass the updated streak
        )

        # Reset session state
        self.current_session = None
        self.is_running = False

        return results

    def session_is_on_new_day(self):
        """Check if this session is happening on a new day compared to last session"""
        from datetime import datetime

        # Load the subject to get its last session date
        subjects = load_all_subjects()
        current_subject = None
        for subject in subjects:
            if subject.name == self.current_session['subject']:
                current_subject = subject
                break

        if not current_subject or not current_subject.last_session_date:
            # No previous session, so this counts as a new day
            return True
        try:
            timestamp = float(current_subject.last_session_date)
        except (ValueError, TypeError):
            # If the date is invalid, treat it as the first session.
            return True
        # Compare session start date with last session date
        session_start_date = datetime.fromtimestamp(self.current_session['start_time']).date()
        last_session_date = datetime.fromtimestamp(timestamp).date()

        return session_start_date > last_session_date

    def get_session_progress(self):
        """Get current session progress without stopping it"""
        if not self.is_running:
            return None

        current_duration = int(time.time() - self.current_session['start_time'])
        return {
            'subject': self.current_session['subject'],
            'duration_seconds': current_duration,
            'duration_human': seconds_to_human_readable(current_duration),
            'current_exp': calculate_base_exp(current_duration),
            'streak_days': self.current_session['streak_days']
        }



