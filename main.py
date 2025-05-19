#!/usr/bin/env python3
"""
EXP FARM - Main Application Entry Point
This file demonstrates the core EXP calculation system.
"""

# Modules
from utils.time_helpers import seconds_to_human_readable, minutes_to_seconds
from core.exp_engine import calculate_base_exp, apply_streak_bonus, calculate_total_exp


# Demonstration
def demo_exp_calculations():
    """Demonstrate EXP calculations with example scenarios"""
    print("\n📊 EXP Calculation Examples:")
    print("-" * 30)

    # Test cases
    test_sessions = [
        (25, 0),  # 25 minutes, no streak
        (45, 0),  # 45 minutes, no streak
        (120, 0),  # 2 hours, no streak
        (45, 3),  # 45 minutes, 3-day streak
        (90, 7),  # 90 minutes, 1-week streak
    ]
    for minutes, streak in test_sessions:
        seconds = minutes_to_seconds(minutes)
        base_exp = calculate_base_exp(seconds)
        total_exp = calculate_total_exp(seconds, streak)

        duration_str = seconds_to_human_readable(seconds)
        streak_str = f" (Streak: {streak} day(s)" if streak > 0 else ""

        print(f"{duration_str:<8} → {total_exp:>6,} EXP{streak_str}")

        # Show breakdown
        if streak > 0:
            streak_bonus = total_exp - base_exp
            print(f"         ├─ Base: {base_exp:,} EXP")
            print(f"         └─ Bonus: +{streak_bonus:,} EXP ({streak*5}%)")


def test_realistic_sessions():
    """Test with realistic EXP FARM usage scenarios"""
    print("\n🎯 Realistic Usage Scenarios:")
    print("-" * 35)

    scenarios = [
        # (description, minutes, streak_days)
        ("Quick study session", 15, 0),
        ("Standard focus block", 25, 0),
        ("Deep work session", 90, 0),
        ("Daily guitar practice", 30, 5),
        ("Weekend marathon", 180, 10),
        ("Consistent learner", 45, 21),  # 3-week streak!
    ]

    for description, minutes, streak in scenarios:
        seconds = minutes_to_seconds(minutes)
        total_exp = calculate_total_exp(seconds, streak)
        duration_str = seconds_to_human_readable(seconds)

        # Calculate EXP per minute for comparison
        exp_per_minute = total_exp / minutes

        print(f"{description:<20} | {duration_str:<8} | {total_exp:>6,} EXP")

        # Add insights
        if minutes >= 90:
            print(f"{'':>21} | {'':>8} | ⭐ Deep focus bonus!")
        if streak >= 10:
            print(f"{'':>21} | {'':>8} | 🔥 Amazing streak!")


if __name__ == "__main__":
    # Run your demonstrations
    print("🎮 EXP FARM - Core System Demo")
    print("=" * 50)

    demo_exp_calculations()
    test_realistic_sessions()
