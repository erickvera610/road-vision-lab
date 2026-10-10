import unittest
from core import fit,robust_fit,run
class Tests(unittest.TestCase):
    def test_line(self):a,b=fit([(3,1),(5,2),(7,3)]);self.assertAlmostEqual(a,2);self.assertAlmostEqual(b,1)
    def test_degenerate(self):
        with self.assertRaises(ValueError):fit([(1,2),(3,2)])
    def test_geometry(self):self.assertGreater(run({'noise':0})['width_bottom'],100)
    def test_noise(self):
        with self.assertRaises(ValueError):run({'noise':99})
    def test_seed(self):self.assertEqual(run({}),run({}))
