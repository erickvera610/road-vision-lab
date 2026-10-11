import unittest
import numpy as np,cv2
from pathlib import Path
from real_pipeline import decode,detect
class LightingTests(unittest.TestCase):
    def test_dark_scene_has_adaptive_support(self):
        image=decode((Path(__file__).parent/'data/real/solidWhiteRight.jpg').read_bytes());dark=cv2.convertScaleAbs(image,alpha=.55)
        self.assertFalse(detect(dark,'fixed')['detected'])
        self.assertTrue(detect(dark,'adaptive')['detected'])
    def test_uniform_controls_and_invalid_mode(self):
        for value in [0,230]:
            self.assertFalse(detect(np.full((180,320,3),value,np.uint8),'adaptive')['detected'])
        with self.assertRaises(ValueError):detect(np.zeros((180,320,3),np.uint8),'bad')
