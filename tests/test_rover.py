"""Unit tests for the Kestrel-1 rover.  Run:  python3 tests/test_rover.py"""
import os
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import controller  # noqa: E402
import detector  # noqa: E402
import limits  # noqa: E402
import sensor  # noqa: E402


class RoverTests(unittest.TestCase):
    def test_forward(self):
        self.assertEqual(controller.forward(100), ("FWD", 100))

    def test_distance(self):
        self.assertEqual(sensor.distance_cm(5800), 100.0)

    def test_echo_timeout_is_sensible(self):
        self.assertTrue(10 <= limits.SENSOR_TIMEOUT_MS <= 60)

    def test_limits_file_has_no_conflict_markers(self):
        with open(os.path.join(ROOT, "src", "limits.py"), encoding="utf-8") as handle:
            text = handle.read()
        for marker in ("<<<<<<<", "=======", ">>>>>>>"):
            self.assertNotIn(marker, text)
        self.assertEqual(text.count("SENSOR_TIMEOUT_MS ="), 1)

    def test_range(self):
        self.assertTrue(sensor.in_range(50))
        self.assertFalse(sensor.in_range(1000))

    def test_detector(self):
        self.assertEqual(detector.detect([0.1, 0.5, 0.9]), [1, 2])


if __name__ == "__main__":
    unittest.main()
