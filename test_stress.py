import unittest
from pipeline import validate_image, ransac
from stress_benchmark import benchmark
class StressTests(unittest.TestCase):
    def test_invalid_row_has_clear_error(self):
        with self.assertRaises(ValueError): validate_image([None]*24)
    def test_short_cluster_is_not_lane(self):
        self.assertIsNone(ransac([(128-.35*y,y) for y in range(70,85)],42,-1))
    def test_negative_controls_and_retained_failures(self):
        report=benchmark()
        self.assertFalse(any(report["negative_controls"].values()))
        self.assertEqual(len(report["conditions"]),45)
        self.assertTrue(any(not r["detected"] for r in report["conditions"]))
