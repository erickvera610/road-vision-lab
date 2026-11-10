# Paired geometry stability audit

The earlier lighting ablation counted supported lane pairs. This audit asks whether the *positions* remain stable when the same image is perturbed. It adds evaluation tooling without changing the detector or claiming an accuracy gain.

## Reproduce

```bash
python -m pip install -r requirements.txt
python geometry_audit.py
python -m unittest discover -v
node test_demo.cjs
node test_enhanced.cjs
```

The checked-in [raw report](geometry-results.json) contains 72 rows: six existing Udacity development images × six conditions (including identity) × two lighting modes. Source hashes are checked before processing. Code hashes and Python, NumPy and OpenCV versions are recorded. The existing perturbation recipes are reused unchanged; noise uses seed 20261012.

## Metric and missing outputs

For each supported pair, evaluate left/right x coordinates at y=floor(0.60×height) and y=height−1 in the resized image. Report the maximum absolute displacement across those four endpoints against the same mode's original-image prediction, both in pixels and divided by image width. All endpoints are retained for inspection. Inputs must share a coordinate frame. Lost, gained and absent support are explicit states: missing geometry has null drift, never zero error. Summaries exclude the identity condition.

## Measured results — 2026-11-10

| Lighting | Both supported after perturbation | Lost support | Perturbed pairs |
|---|---:|---:|---:|
| Fixed | 17 | 13 | 30 |
| Adaptive | 29 | 1 | 30 |

Concrete example: `solidWhiteRight.jpg`, adaptive mode, Gaussian blur with a 15×15 kernel. Both images produce supported pairs, but the left bottom endpoint moves from **90.63 to 141.38 pixels** in the 640×360 processing frame. Maximum endpoint displacement is **50.75 px**, or **7.93% of image width**. The original prediction is a reference, not ground truth.

All **24 Python tests passed locally**, including four new tests covering identity, a known 7-pixel translation, unavailable comparisons and incompatible coordinate frames. Both JavaScript suites passed. CI now reproduces this audit and retains the report; this local run does not claim a completed remote CI run.

## Limits

These six images were already used for development and are not independently annotated. Stability is not correctness: a stable line can be wrong, and displacement does not identify which prediction is better. This is a classical OpenCV prototype, not neural lane detection or a driving-control system. Independent annotated scenes remain necessary for accuracy evaluation. The project and this extension were developed with AI assistance.
