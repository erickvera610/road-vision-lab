# Portfolio Evidence

This page separates measured evidence from claims. Every result below is tied to reproducible artifacts already present in this repository.

## Real data

- Six real road photographs from Udacity CarND-LaneLines-P1.
- Source revision, URLs, SHA-256 checksums, and upstream license are documented in `data/real/manifest.json` and `data/real/LICENSE.udacity`.
- The project evaluates a classical computer-vision pipeline rather than a trained lane neural network.

## Pipeline

HSV white/yellow masking → Gaussian blur → Canny edges → trapezoidal road ROI → Hough line segments → seeded RANSAC → lane-pair geometry checks.

The implementation preserves image aspect ratio, validates candidate geometry, and returns an explicit insufficient-evidence result rather than inventing a lane estimate when support is weak.

## Measured robustness evidence

Paired illumination ablation on the six known development images:

| Condition | Fixed threshold | Adaptive illumination |
|---|---:|---:|
| Original daylight | 6/6 supported pairs | 6/6 supported pairs |
| Brightness × 0.55 | 0/6 | 6/6 |
| Brightness × 0.35 | 0/6 | 6/6 |
| Gaussian blur 15×15 | 5/6 | 5/6 |

Blank and bright-wall negative controls produce no supported pair in either mode.

These counts measure output availability under controlled perturbations. They are **not lane-detection accuracy**, IoU, recall, or calibrated confidence. The six images were used during development and therefore are not an independent test set.

## Evidence a recruiter can inspect

1. `real_pipeline.py` — real-image computer-vision pipeline.
2. `lighting_benchmark.py` — paired robustness experiment.
3. `lighting-results.json` — fixed-vs-adaptive perturbation results.
4. `real_benchmark.py` and `real-results.json` — real-image diagnostics.
5. `test_real_api.py` and the Python test suite — image, API, failure, and recovery checks.
6. `app.py` — validated local inference API.
7. `.devcontainer/` and `Dockerfile` — reproducible runnable environment.
8. GitHub Actions — automated dependency installation and test/report reproduction.

## Engineering skills demonstrated

Python, OpenCV-style classical computer vision, image preprocessing, HSV segmentation, Canny edge detection, Hough geometry, RANSAC, robustness testing, negative controls, API validation, defensive image handling, unit testing, CI, Docker, Codespaces, data provenance, checksum verification, and explicit failure analysis.

## Why this matters for internships

This project provides concrete evidence for computer-vision and software-engineering discussions because a reviewer can inspect the actual image pipeline, run it against real photographs, reproduce controlled perturbation tests, and see documented failure behavior instead of only a polished success example.

## Important limitations

- Only six real source images are currently included.
- They were used during development, so they are not a held-out evaluation set.
- No official lane annotations are available in the current benchmark.
- The model approximates lanes with straight geometry and can fail on curves, shadows, worn markings, changing camera viewpoints, or unusual road scenes.
- No temporal tracking, object detection, neural lane model, metric lane width, IoU, recall, or production driving claim is made.

## Next evidence milestone

The highest-value next step is an **independent annotated evaluation dataset** with scene-level separation. Freeze the current detector before evaluation, then report lane-level precision/recall or an appropriate geometric metric on unseen scenes. Keep failure examples and compare fixed versus adaptive illumination without tuning on the final test set.

That upgrade would move this project from a strong real-image prototype and robustness study toward a more rigorous computer-vision evaluation project.
