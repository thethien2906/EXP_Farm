# core/database.py
from datetime import datetime, timedelta, time
import sqlite3
import os
from pathlib import Path
from data.models import Subject
import time

def get_database_path():
    """Return the path where the database should be stored"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir / "exp_farm.db"


def get_connection():
    """Get a connection to the SQLite database"""
    db_path = get_database_path()
    connection = sqlite3.connect(db_path)
    # Enable foreign key constraints
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_database():
    """Create database tables if they don't exist"""
    conn = get_connection()
    cursor = conn.cursor()

    # Create subjects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            name TEXT PRIMARY KEY,
            icon TEXT,
            image_path TEXT,
            total_exp REAL DEFAULT 0,
            total_hours REAL DEFAULT 0.0,
            last_session_date REAL,
            current_streak INTEGER DEFAULT 0,
            created_at REAL DEFAULT (strftime('%s', 'now'))
        )
    """)

    # Create sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            start_time REAL NOT NULL,
            end_time REAL NOT NULL,
            duration_seconds INTEGER NOT NULL,
            base_exp INTEGER NOT NULL,
            bonus_exp INTEGER DEFAULT 0,
            total_exp INTEGER NOT NULL,
            streak_days INTEGER DEFAULT 0,
            notes TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (subject_name) REFERENCES subjects (name)
        )
    """)

    conn.commit()
    conn.close()


def save_subject(subject):
    """Save or update a subject in the database"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO subjects 
        (name, icon, image_path, total_exp, total_hours, last_session_date, current_streak)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        subject.name,
        subject.icon,
        subject.image_path,
        subject.total_exp,
        subject.total_hours,
        subject.last_session_date,
        subject.current_streak
    ))

    conn.commit()
    conn.close()


def load_all_subjects():
    """Load all subjects from database and return as Subject objects"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")
    rows = cursor.fetchall()
    conn.close()

    subjects = []
    for row in rows:
        subject = Subject(name=row[0], icon=row[1], image_path=row[2])
        subject.total_exp = row[3]
        subject.total_hours = row[4]
        subject.last_session_date = row[5]
        subject.current_streak = row[6]
        subjects.append(subject)

    return subjects


def delete_subject(subject_name):
    """Delete a subject and all its sessions from database"""
    conn = get_connection()
    cursor = conn.cursor()

    # Delete associated sessions first (foreign key constraint)
    cursor.execute("DELETE FROM sessions WHERE subject_name = ?", (subject_name,))

    # Delete the subject
    cursor.execute("DELETE FROM subjects WHERE name = ?", (subject_name,))

    conn.commit()
    conn.close()


def save_session(session_result):
    """Save a completed session to the database"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sessions 
        (subject_name, start_time, end_time, duration_seconds, base_exp, bonus_exp, total_exp, streak_days, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_result['subject'],
        session_result.get('start_time'),  # You'll need to add this to session_result
        session_result.get('end_time'),  # You'll need to add this to session_result
        session_result['duration_seconds'],
        session_result['base_exp'],
        session_result['bonus_exp'],
        session_result['total_exp'],
        session_result['streak_days'],
        session_result.get('notes', '')  # Optional notes
    ))

    conn.commit()
    conn.close()


def get_session_history(subject_name=None, limit=10):
    """Get recent session history, optionally filtered by subject"""
    conn = get_connection()
    cursor = conn.cursor()

    if subject_name:
        cursor.execute("""
            SELECT * FROM sessions 
            WHERE subject_name = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (subject_name, limit))
    else:
        cursor.execute("""
            SELECT * FROM sessions 
            ORDER BY created_at DESC 
            LIMIT ?
        """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_total_stats():
    """Get overall statistics across all subjects"""
    conn = get_connection()
    cursor = conn.cursor()

    # Total sessions count
    cursor.execute("SELECT COUNT(*) FROM sessions")
    total_sessions = cursor.fetchone()[0]

    # Total hours (sum of all session durations)
    cursor.execute("SELECT SUM(duration_seconds) FROM sessions")
    total_seconds = cursor.fetchone()[0] or 0
    total_hours = total_seconds / 3600

    # Current longest streak (this is simplified - you might want more complex streak logic)
    cursor.execute("SELECT MAX(current_streak) FROM subjects")
    current_streak = cursor.fetchone()[0] or 0

    conn.close()

    return {
        'total_sessions': total_sessions,
        'total_hours': round(total_hours, 1),
        'current_streak': current_streak
    }


def update_subject_after_session(subject_name, exp_gained, duration_hours, new_streak):
    """Update subject's total EXP, hours, and streak after a session"""
    conn = get_connection()
    cursor = conn.cursor()

    # Use timestamp for last_session_date (consistent with your schema)
    current_timestamp = time.time()

    cursor.execute("""
        UPDATE subjects 
        SET total_exp = total_exp + ?,
            total_hours = total_hours + ?,
            last_session_date = ?,
            current_streak = ?
        WHERE name = ?
    """, (exp_gained, duration_hours, current_timestamp, new_streak, subject_name))

    conn.commit()
    conn.close()


def calculate_current_streak(subject_name):
    """
    Calculate the current streak for a subject based on session history

    Returns:
        int: Current streak days (0 if no sessions, 1+ for active streaks)
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Get the subject's current data
    cursor.execute("SELECT last_session_date, current_streak FROM subjects WHERE name = ?", (subject_name,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return 0

    last_session_date, stored_streak = result

    # If no previous session, this will be day 1
    if not last_session_date:
        conn.close()
        return 1

    try:
        timestamp = float(last_session_date)
    except (ValueError, TypeError):
        # If the date is invalid, we can't calculate a streak. Reset to 1.
        conn.close()
        return 1

    # Convert stored timestamp to date
    last_session_datetime = datetime.fromtimestamp(timestamp)
    last_session_day = last_session_datetime.date()
    today = datetime.now().date()

    # Calculate days between last session and today
    days_diff = (today - last_session_day).days

    conn.close()

    # Streak logic:
    if days_diff == 0:
        # Same day - return existing streak (no change)
        return stored_streak
    elif days_diff == 1:
        # Yesterday - continue streak
        return stored_streak + 1
    else:
        # More than 1 day gap - reset streak
        return 1

