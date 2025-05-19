import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.exp_engine import calculate_base_exp, apply_streak_bonus, calculate_total_exp


class TestEXPEngine(unittest.TestCase):

    def test_tier_1_only(self):
        """Test sessions that stay in Tier 1 (0-30 min)"""
        # 25-minute session from docs
        self.assertEqual(calculate_base_exp(25 * 60), 15000)

        # Edge case: exactly 30 minutes
        self.assertEqual(calculate_base_exp(30 * 60), 18000)

        # Very short session
        self.assertEqual(calculate_base_exp(60), 600)  # 1 minute

    def test_tier_1_and_2(self):
        """Test sessions spanning Tier 1 and 2 (30-60 min)"""
        # 45-minute session from docs
        self.assertEqual(calculate_base_exp(45 * 60), 36000)

        # Edge case: exactly 60 minutes
        self.assertEqual(calculate_base_exp(60 * 60), 54000)

        # 31 minutes (just over Tier 1)
        expected = 1800 * 10 + 60 * 20  # 18000 + 1200 = 19200
        self.assertEqual(calculate_base_exp(31 * 60), 19200)

    def test_all_three_tiers(self):
        """Test sessions spanning all tiers (60+ min)"""
        # 2-hour session from docs
        self.assertEqual(calculate_base_exp(120 * 60), 162000)

        # 90-minute session
        expected = 1800 * 10 + 1800 * 20 + 1800 * 30  # 18000 + 36000 + 54000 = 108000
        self.assertEqual(calculate_base_exp(90 * 60), 108000)

    def test_edge_cases(self):
        """Test edge cases"""
        # Zero seconds
        self.assertEqual(calculate_base_exp(0), 0)

        # One second
        self.assertEqual(calculate_base_exp(1), 10)

    def test_streak_bonus_calculation(self):
        """Test streak bonus calculations"""
        base_exp = 10000

        # No streak
        self.assertEqual(apply_streak_bonus(base_exp, 0), 10000)

        # 1-day streak (+5%)
        self.assertEqual(apply_streak_bonus(base_exp, 1), 10500)

        # 3-day streak (+15%)
        self.assertEqual(apply_streak_bonus(base_exp, 3), 11500)

        # 10-day streak (+50%)
        self.assertEqual(apply_streak_bonus(base_exp, 10), 15000)

    def test_complete_exp_calculation(self):
        """Test the full EXP calculation with streaks"""
        # 45-minute session with 3-day streak
        # Base: 36,000 EXP, with 15% bonus = 41,400 EXP
        total_exp = calculate_total_exp(45 * 60, 3)
        self.assertEqual(total_exp, 41400)

        # 25-minute session with no streak
        total_exp = calculate_total_exp(25 * 60, 0)
        self.assertEqual(total_exp, 15000)


if __name__ == '__main__':
    unittest.main()