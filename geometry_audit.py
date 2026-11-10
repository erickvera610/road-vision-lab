"""Paired geometry stability, not accuracy against annotated lanes."""
from pathlib import Path
import hashlib
import json
import platform
import cv2
import numpy as np
from real_pipeline import detect
from robustness_matrix import perturb

ROOT = Path(__file__).parent
CONDITIONS = ('original', 'dark_55', 'dark_35', 'bright_125', 'blur_15', 'noise_sigma_12')


def geometry(result):
    """Four x coordinates in resized-image pixels, or None for abstention."""
    if not result['detected']:
        return None
    ys = (int(result['height'] * .60), result['height'] - 1)
    return [float(result[side]['slope'] * y + result[side]['intercept'])
            for side in ('left', 'right') for y in ys]


def compare(reference, changed):
    if (reference['width'], reference['height']) != (changed['width'], changed['height']):
        raise ValueError('Paired results must use the same coordinate frame')
    a, b = geometry(reference), geometry(changed)
    state = ('both_supported' if a is not None and b is not None else
             'lost_support' if a is not None else
             'gained_support' if b is not None else 'neither_supported')
    drift = max(abs(x-y) for x, y in zip(a, b)) if state == 'both_supported' else None
    return {'transition': state, 'reference_endpoints_px': a, 'perturbed_endpoints_px': b,
            'max_endpoint_drift_px': drift,
            'max_endpoint_drift_fraction_width': drift/reference['width'] if drift is not None else None}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    manifest = json.loads((ROOT/'data/real/manifest.json').read_text())
    rows = []
    for item in manifest['images']:
        path = ROOT/'data/real'/item['filename']
        if sha(path) != item['sha256']:
            raise ValueError('Source checksum mismatch: ' + item['filename'])
        image = cv2.imread(str(path))
        for mode in ('fixed', 'adaptive'):
            reference = detect(image, mode)
            for condition in CONDITIONS:
                changed = detect(perturb(image, condition), mode)
                rows.append({'image': item['filename'], 'source_sha256': item['sha256'],
                             'condition': condition, 'lighting': mode,
                             'width': reference['width'], 'height': reference['height'],
                             **compare(reference, changed)})
    return {'interpretation': 'Stability relative to the original prediction, NOT lane accuracy. Null drift is an unavailable comparison, never zero error.',
            'limitations': manifest['labels'],
            'endpoint_order': ['left_top', 'left_bottom', 'right_top', 'right_bottom'],
            'versions': {'python': platform.python_version(), 'numpy': np.__version__, 'opencv': cv2.__version__},
            'code_sha256': {name: sha(ROOT/name) for name in ('geometry_audit.py','real_pipeline.py','pipeline.py','robustness_matrix.py')},
            'rows': rows}


if __name__ == '__main__':
    report = run()
    (ROOT/'geometry-results.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    for mode in ('fixed', 'adaptive'):
        subset = [r for r in report['rows'] if r['lighting'] == mode and r['condition'] != 'original']
        states = {s: sum(r['transition'] == s for r in subset) for s in
                  ('both_supported','lost_support','gained_support','neither_supported')}
        print(mode, states)
        valid = [r for r in subset if r['max_endpoint_drift_px'] is not None]
        print('Largest drift:', max(valid, key=lambda r: r['max_endpoint_drift_px']))
