import unittest
import sys
import os

# Add the parent directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.time_helpers import seconds_to_human_readable, minutes_to_seconds


class TestTimeHelpers(unittest.TestCase):
    """Test cases for time utility functions"""

    def test_seconds_to_human_readable_basic_cases(self):
        # Test exact hour
        self.assertEqual(seconds_to_human_readable(3600), "1h")

        # Test exact minutes
        self.assertEqual(seconds_to_human_readable(300), "5m")

        # Test only seconds
        self.assertEqual(seconds_to_human_readable(45), "45s")

        # Test combination
        self.assertEqual(seconds_to_human_readable(3661), "1h 1m 1s")

    def test_seconds_to_human_readable_edge_cases(self):
        # Test zero seconds
        self.assertEqual(seconds_to_human_readable(0), "0s")

        # Test no minutes (hour + seconds)
        self.assertEqual(seconds_to_human_readable(3605), "1h 5s")

        # Test no seconds (hour + minutes)
        self.assertEqual(seconds_to_human_readable(3660), "1h 1m")

        # Test large numbers
        self.assertEqual(seconds_to_human_readable(25200), "7h")  # Exactly 7 hours

    def test_minutes_to_seconds(self):
        # Basic conversions
        self.assertEqual(minutes_to_seconds(1), 60)
        self.assertEqual(minutes_to_seconds(45), 2700)
        self.assertEqual(minutes_to_seconds(90), 5400)
        # Zero minutes
        self.assertEqual(minutes_to_seconds(0), 0)

    def test_exp_farm_specific_scenarios(self):
        # Test tier boundaries from your EXP system
        # 25-minute session (Tier 1)
        self.assertEqual(seconds_to_human_readable(25 * 60), "25m")

        # 30-minute session (Tier 1-2 boundary)
        self.assertEqual(seconds_to_human_readable(30 * 60), "30m")

        # 45-minute session (example from your docs)
        self.assertEqual(seconds_to_human_readable(45 * 60), "45m")

        # 90-minute session (spans all tiers)
        self.assertEqual(seconds_to_human_readable(90 * 60), "1h 30m")

        # 2-hour session (example from your docs)
        self.assertEqual(seconds_to_human_readable(120 * 60), "2h")


if __name__ == '__main__':
    unittest.main()