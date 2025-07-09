# core/exp_engine.py
TIER_1_DURATION = 1800  # 30 minutes in seconds
TIER_2_DURATION = 3600  # 60 minutes in seconds

TIER_1_RATE = 10  # EXP per second
TIER_2_RATE = 20  # EXP per second
TIER_3_RATE = 30  # EXP per second

STREAK_BONUS_RATE = 0.05  # 5% per day
def calculate_base_exp(session_seconds):
    """
    Calculate base EXP earned from a session using the tier system

    Tiers:
    - 0-30 min (0-1800s): 10 EXP per second
    - 30-60 min (1800-3600s): 20 EXP per second
    - 60+ min (3600s+): 30 EXP per second

    Args:
        session_seconds (int): Total session duration in seconds

    Returns:
        int: Total base EXP earned
    """
    # Input validation
    if not isinstance(session_seconds, (int, float)):
        raise TypeError("session_seconds must be a number")
    if session_seconds < 0:
        raise ValueError("session_seconds cannot be negative")
    if session_seconds == 0:
        return 0

    # Logic Implementation
    if session_seconds <= TIER_1_DURATION:
        return session_seconds * TIER_1_RATE
    elif session_seconds <= TIER_2_DURATION:
        return (TIER_1_DURATION * TIER_1_RATE +
                (session_seconds - TIER_1_DURATION) * TIER_2_RATE)
    else:
        return (TIER_1_DURATION * TIER_1_RATE +
                TIER_1_DURATION * TIER_2_RATE +
                (session_seconds - TIER_2_DURATION) * TIER_3_RATE)


def apply_streak_bonus(base_exp, streak_days):
    """
    Apply streak bonus to base EXP

    Bonus: +5% per consecutive day (multiplicative)
    Example: 3-day streak = 15% bonus total

    Args:
        base_exp (int): Base EXP before bonuses
        streak_days (int): Current streak length

    Returns:
        int: EXP with streak bonus applied
    """
    bonus = 1 + 0.05 * streak_days
    return round(base_exp * bonus)


def calculate_total_exp(session_seconds, streak_days=0):
    """
    Calculate total EXP including streak bonuses

    Args:
        session_seconds (int): Session duration in seconds
        streak_days (int): Current streak length (default: 0)

    Returns:
        int: Total EXP earned
    """
    base_exp = calculate_base_exp(session_seconds)
    return apply_streak_bonus(base_exp, streak_days)