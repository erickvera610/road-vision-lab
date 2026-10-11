# Road Vision Lab — real images, Python backend

![Tests](https://github.com/erickvera610/road-vision-lab/actions/workflows/tests.yml/badge.svg)

## New: paired illumination ablation

**[Reviewer evidence](RECRUITER_GUIDE.md)** · [Paired report](lighting-results.json) · [Public evidence page](https://erickvera610.github.io/road-vision-lab/evidence.html) · [CI tests](https://github.com/erickvera610/road-vision-lab/actions/workflows/tests.yml)

Compare the preserved fixed-threshold detector with ROI percentile illumination normalization. The Python demo now defaults to adaptive illumination and lets you choose the fixed baseline.

| Known development images | Fixed supported pairs | Adaptive supported pairs |
|---|---:|---:|
| Original daylight | 6/6 | 6/6 |
| Brightness × 0.55 | 0/6 | 6/6 |
| Brightness × 0.35 | 0/6 | 6/6 |
| Blur 15 × 15 | 5/6 | 5/6 |

Blank and bright-wall controls have no supported pair in either mode. This ablation shows output availability under controlled perturbations, **not lane accuracy**. All six source images were previously used for development. Normalization can amplify distractors; independent annotated evaluation remains a gap. Existing `real-results.json` describes the fixed baseline; `lighting-results.json` compares both methods.

```bash
python lighting_benchmark.py
python -m unittest discover -v
```

The road pipeline remains classical computer vision, without a trained lane neural network. Neural training is demonstrated in ML Model Lab separately.


An interactive classical computer-vision prototype for inspecting real road photographs. Upload a PNG/JPEG or choose one of six attributed Udacity samples. The application sends the image to Python and displays the original, color mask, road edges and estimated lane geometry.

**[Launch in GitHub Codespaces](https://codespaces.new/erickvera610/road-vision-lab)** · [Public browser exercise](https://erickvera610.github.io/road-vision-lab/) · [Real-image report](real-results.json) · [Guía en español](GUIA_PORTAFOLIO_ES.md)

Codespaces requires your GitHub account and available quota. It installs dependencies and opens port 8000 automatically. The Python demo is runnable locally or in your Codespace; no public always-on Python endpoint has been deployed. GitHub Pages serves the legacy JavaScript exercise and a real-output gallery, not the Python API.

## Run locally

Python 3.11 or 3.12:

```bash
git clone https://github.com/erickvera610/road-vision-lab.git
cd road-vision-lab
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:8000. The same application runs in Codespaces with port 8000 forwarded. If it does not open automatically, use the Ports tab and select “Open in Browser”.

Optional container:

```bash
docker build -t road-vision-lab .
docker run --rm -p 8000:8000 road-vision-lab
```

## What the Python pipeline does

HSV white/yellow mask → Gaussian blur and Canny edges → trapezoidal road region → Hough line segments → seeded RANSAC → pair geometry checks.

Color filtering retains yellow as well as white markings. Preserved aspect ratio avoids stretching road geometry. RANSAC requires spatial support, while pair checks reject crossing lines and impossible bottom-image positions. The UI explicitly reports insufficient evidence instead of inventing a width.

The perspective slope range was widened for the real-image pipeline after exploratory inspection. The original synthetic exercise retains its defaults. This is classical image processing, not a trained neural network.

## Real-image diagnostics

| Condition | Supported pairs | Images |
|---|---:|---:|
| Original daylight photographs | 6 | 6 |
| Brightness multiplied by 0.55 | 0 | 6 |
| Gaussian blur, 15 × 15 kernel | 5 | 6 |

These counts mean geometrically supported outputs, **not accuracy**. The six known convenience images were used during development and have no official lane annotations here. They are not a held-out test set. A straight-line overlay can approximate a curve incorrectly. Darkening exposes the fixed-brightness threshold's sensitivity.

[Inspect every result](real-results.json), including failures, source revision and protocol. No lane-width distance in meters, calibrated confidence, recall or IoU is claimed. The next evaluation milestone is a separately annotated road-image dataset with scene-level separation.

## Reproduce

```bash
python -m unittest discover -v
node test_demo.cjs
node test_enhanced.cjs
python real_benchmark.py
python stress_benchmark.py
python benchmark.py
```

18 Python tests cover legacy behavior, real-photo processing, sample/upload equivalence, malformed inputs, oversized images, negative controls and API recovery. The legacy browser exercise has separate JavaScript checks. CI installs the declared dependencies and reproduces both real and synthetic reports.

## API

- `GET /health`: backend availability.
- `GET /api/samples`: the fixed sample list.
- `POST /api/detect`: JSON with `sample` (known sample filename) or `image_base64` (PNG/JPEG bytes encoded in base64).
- `POST /api/run`: preserved synthetic exercise API.

Responses contain candidate geometry, a reason, elapsed processing time and four PNG data URLs. Uploads are processed in server memory, never written to disk. Image limits: 5 MB compressed, 16 megapixels decoded, maximum dimension 8,000 px. The API does not fetch arbitrary URLs or accept filesystem paths.

## Source map

- `real_pipeline.py`: real-photo processing.
- `image_header.py`: pre-decode PNG/JPEG dimension checks.
- `app.py` and `index.html`: Python HTTP API and connected UI.
- `real_benchmark.py`: real-photo sensitivity report.
- `pipeline.py`: retained grayscale/synthetic RANSAC exercise.
- `test_real_api.py`: HTTP and decoder behavior tests.
- `.devcontainer/`: runnable GitHub Codespaces configuration.

## Data provenance and limitations

Six JPEGs copied unchanged from [Udacity CarND-LaneLines-P1](https://github.com/udacity/CarND-LaneLines-P1), revision `ce5681be7ef8140560c0e464ef2da611e40b4fc9`. Source URLs and SHA-256 checksums are in [data/real/manifest.json](data/real/manifest.json). The upstream MIT license is retained in [data/real/LICENSE.udacity](data/real/LICENSE.udacity).

Daylight bias, a fixed camera ROI, straight-line approximation, no temporal tracking, no object recognition and no official annotations limit this prototype. Shadows, curves, worn markings and camera changes may fail. Geometric agreement is not correctness. This is an independent AI-assisted learning project in Erik Vera's portfolio, with no employer affiliation or driving-control claim.

## Three featured portfolio projects

- [ML Model Lab](https://github.com/erickvera610/ml-model-lab)
- [Road Vision Lab](https://github.com/erickvera610/road-vision-lab)
- [Media Content Lab](https://github.com/erickvera610/media-content-lab)
