"""Pixel pipeline: grayscale image → ROI gradients → RANSAC → lane geometry."""
import random, math
from core import fit

def synthetic_image(seed=42, noise=4, width=256, height=144):
    rng = random.Random(seed)
    image = [[max(0, min(255, 20 + rng.gauss(0, noise))) for x in range(width)] for y in range(height)]
    for y in range(int(height * 0.4), height):
        for x in [round(width / 2 - 0.35 * y), round(width / 2 + 0.35 * y)]:
            for dx in range(-2, 3):
                image[y][x + dx] = 230
    for y in range(70, 82):
        for x in range(110, 140):
            image[y][x] = 210
    return image

def validate_image(image):
    if not isinstance(image, list) or not 24 <= len(image) <= 360:
        raise ValueError('Image height must be 24–360')
    if not isinstance(image[0], list):
        raise ValueError('Rows must be lists')
    w = len(image[0])
    if not 32 <= w <= 640 or any((not isinstance(row, list) or len(row) != w for row in image)):
        raise ValueError('Rectangular width 32–640 required')
    if any((not isinstance(v, (int, float)) or not math.isfinite(v) or (not 0 <= v <= 255) for row in image for v in row)):
        raise ValueError('Finite grayscale pixels 0–255 required')
    return (w, len(image))

def candidates(image):
    w, h = validate_image(image)
    left = []
    right = []
    for y in range(int(h * 0.4), h - 1):
        for x in range(1, w - 1):
            gx = sum((image[y + j][x + 1] - image[y + j][x - 1] for j in [-1, 0, 1]))
            if image[y][x] > 150 and abs(gx) > 160:
                (left if x < w / 2 else right).append((x, y))
    return (left, right)

def ransac(points, seed, expected_sign, iterations=120, tolerance=3):
    if len(points) < 8:
        return None
    rng = random.Random(seed)
    best = []
    for _ in range(iterations):
        p, q = rng.sample(points, 2)
        if abs(p[1] - q[1]) < 10:
            continue
        a = (p[0] - q[0]) / (p[1] - q[1])
        b = p[0] - a * p[1]
        if not 0.05 < expected_sign * a < 1.5:
            continue
        kept = [(x, y) for x, y in points if abs(x - a * y - b) <= tolerance]
        if len(kept) > len(best):
            best = kept
    if len(best) < 8 or max(y for x, y in best) - min(y for x, y in best) < 20:
        return None
    a, b = fit(best)
    return {'slope': a, 'intercept': b, 'inliers': len(best), 'candidate_count': len(points), 'inlier_ratio': len(best) / len(points), 'rmse': math.sqrt(sum(((x - a * y - b) ** 2 for x, y in best)) / len(best)), 'points': best}

def run_image(p):
    noise = float(p.get('noise', 4))
    seed = int(p.get('seed', 42))
    if not 0 <= noise <= 30:
        raise ValueError('Noise must be 0–30')
    uploaded = 'image' in p
    image = p.get('image') if uploaded else synthetic_image(seed, noise)
    w, h = validate_image(image)
    l, r = candidates(image)
    left = ransac(l, seed, -1)
    right = ransac(r, seed + 1, 1)
    width = right['slope'] * (h - 1) + right['intercept'] - (left['slope'] * (h - 1) + left['intercept']) if left and right else None
    error = abs(width - 0.7 * (h - 1)) if width is not None and (not uploaded) else None
    return {'image': image, 'width': w, 'height': h, 'left': left, 'right': right, 'width_bottom': width, 'synthetic_width_error_px': error, 'detected': bool(left and right), 'data_kind': 'uploaded image' if uploaded else 'synthetic image', 'note': 'Pixel-level grayscale ROI/gradient/RANSAC prototype. Straight bright lanes only; not vehicle control. No ground truth for uploads.'}
