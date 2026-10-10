import unittest
from pipeline import run_image

class PixelTests(unittest.TestCase):

    def test_detects_from_pixels(self):
        r = run_image({'noise': 4})
        self.assertTrue(r['detected'])
        self.assertLess(r['synthetic_width_error_px'], 5)

    def test_blank_image_reports_no_detection(self):
        self.assertFalse(run_image({'image': [[0] * 64 for _ in range(48)]})['detected'])

    def test_malformed_image(self):
        with self.assertRaises(ValueError):
            run_image({'image': [[float('nan')] * 64 for _ in range(48)]})

    def test_multiple_seeds(self):
        for seed in range(5):
            self.assertLess(run_image({'seed': seed, 'noise': 10})['synthetic_width_error_px'], 5)
