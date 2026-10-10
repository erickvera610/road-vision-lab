# Case study: real-road image processing

## Problem

Inspect candidate straight-lane geometry in a real photograph and expose intermediate evidence. The earlier coordinate generator and synthetic pixel demo did not establish real-camera behavior.

## Implementation and decisions

The connected frontend uses the Python `/api/detect` endpoint for both bundled photos and user uploads. Color selection includes white and yellow markings. Blur/Canny detect edges; a fixed trapezoidal ROI removes sky and much background. Hough provides segments and seeded RANSAC fits a line per side. Pair geometry rejects crossing or out-of-frame bottom coordinates.

The real-photo slope filter permits a larger perspective range than the synthetic demo. Images retain their aspect ratio and are analyzed at at most 640 × 360. Candidate status and intermediate masks remain visible so users can inspect errors.

## Data and evaluation

Six attributed Udacity JPEGs, with source revision, upstream license and checksums. No official annotations were supplied. These known development images are an exploratory collection, not an independent test set.

Original supported pairs: 6/6. After 0.55 brightness scaling: 0/6. After 15 × 15 Gaussian blur: 5/6. See real-results.json for every case. These are output-availability counts, not lane correctness or accuracy. The poor darkened-image result exposes the fixed color thresholds.

## Validation

18 Python behavior tests, including sample/upload equivalence through HTTP, malformed/oversized inputs, no-lane negative control, API recovery and preserved synthetic behavior. Separate JavaScript checks preserve the public legacy exercise. HTTP paths and payloads are tested against an actual Python server. A DOM integration check also executed the frontend with real API requests: sample analysis, file upload, invalid-file feedback and recovery passed. Headless visual browser verification was unavailable in the build environment; responsive layout uses a single-column breakpoint.

## Remaining gaps

A separately annotated dataset is required for endpoint errors or lane precision/recall. Fixed ROI, illumination thresholds and straight-line models may fail on changed camera positions, shadows and curvature. There is no neural training, tracking, object detection or driving control.

## Execution surfaces

Local Python and GitHub Codespaces run the connected app. Docker configuration is included. GitHub Pages remains static; it does not execute Python. No always-on public Python backend has been deployed.
