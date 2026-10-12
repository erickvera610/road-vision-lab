# Recruiter Quick View

## What this project proves

This repository demonstrates a real-image computer-vision pipeline with explicit failure handling, reproducible perturbation tests, API validation, and careful separation between geometric output availability and true lane accuracy.

## Best evidence to inspect first

1. `evidence.html` — visual evidence page for real-image outputs.
2. `lighting-results.json` — paired fixed-vs-adaptive illumination comparison.
3. `robustness_matrix.py` — expanded brightness, blur, and noise stress matrix.
4. `real_pipeline.py` — HSV mask, Canny edges, ROI, Hough segments, seeded RANSAC, and pair checks.
5. `real-results.json` — per-image diagnostics and failures.
6. GitHub Actions — automated tests.

## Skills shown

Python, OpenCV, classical computer vision, image preprocessing, robustness testing, RANSAC, geometry validation, API design, input validation, negative controls, Docker/Codespaces, unit tests, and CI.

## Important interpretation

The six attributed road images do not include independent official lane annotations. A `detected` result means the pipeline found a geometrically supported pair; it does not equal lane accuracy, IoU, recall, or safe-driving performance.

## Recommended interview demo

Run:

```bash
python robustness_matrix.py
python -m unittest discover -v
python app.py
```

Show the same image under original, dark, blur, and noise conditions and explain why adaptive illumination can recover output while also creating a risk of amplified distractors.

## Screenshot/result checklist

Capture:

- original image + overlay,
- edge image + color mask,
- one successful perturbation comparison,
- one failure case with the explicit rejection reason,
- the robustness-matrix summary.

A strong portfolio screenshot should include both success and failure evidence rather than only favorable outputs.
