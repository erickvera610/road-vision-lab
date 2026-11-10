import unittest
from geometry_audit import compare


def result(detected=True, shift=0, width=100):
    return {'detected': detected, 'width': width, 'height': 50,
            'left': {'slope': -.5, 'intercept': 40+shift},
            'right': {'slope': .5, 'intercept': 60+shift}}


class GeometryAuditTests(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(compare(result(), result())['max_endpoint_drift_px'], 0)

    def test_known_translation(self):
        pair = compare(result(), result(shift=7))
        self.assertEqual(pair['max_endpoint_drift_px'], 7)
        self.assertEqual(pair['max_endpoint_drift_fraction_width'], .07)
        self.assertEqual(pair['reference_endpoints_px'], [25, 15.5, 75, 84.5])

    def test_missing_pairs_are_not_zero_error(self):
        for a, b, state in [(True,False,'lost_support'), (False,True,'gained_support'),
                            (False,False,'neither_supported')]:
            pair = compare(result(a), result(b))
            self.assertEqual(pair['transition'], state)
            self.assertIsNone(pair['max_endpoint_drift_px'])
            self.assertIsNone(pair['max_endpoint_drift_fraction_width'])

    def test_frame_mismatch(self):
        with self.assertRaises(ValueError):
            compare(result(), result(width=200))
