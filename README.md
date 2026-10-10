# Road Vision Lab

The original demo fitted coordinates supplied by the generator. This version extracts candidate pixels from a grayscale image and estimates lines with RANSAC. A synthetic road scene supplies known geometry; visitors can also upload a local PNG/JPEG/WebP photograph.

**[Open the live demo](https://erickvera610.github.io/road-vision-lab/)** · [Spanish tutorial](TUTORIAL_ES.md) · [Case study](CASE_STUDY.md) · [Measured results](benchmark-results.json)

## Understand it in one minute

Image pixels → grayscale ROI → gradients → RANSAC → line overlay

A fixed lower-image ROI, bright-pixel threshold and horizontal gradient reject much of the background. RANSAC tolerates some bright distractors, then least-squares refits the inliers. A fixed seed makes the exercise reproducible. No neural detector is claimed.

## Measured evidence

Reproduced with Python by `python benchmark.py`. Execution timestamp is recorded in the JSON report. Synthetic JavaScript values may differ because the random generator differs.

| Measurement | Result |
|---|---|
| detected scenes | 10 |
| scene count | 10 |
| mean width error px | 1.5178 |
| blank image detected | False |

## Run locally

Python 3.11 or 3.12, standard library only. No API keys.

```bash
git clone https://github.com/erickvera610/road-vision-lab.git
cd road-vision-lab
python app.py
```

Open http://127.0.0.1:8000. Stop with Ctrl+C. The public browser demo requires no installation.

## Reproduce and inspect

```bash
python -m unittest discover -v
node test_enhanced.cjs
python benchmark.py
python daily_exercise.py
```

Use `core.run({"mode":"pixels","seed":42,"noise":10})`. Use `core.run({"image": grayscale_array})` for your own image. The public upload runs entirely on your device.

## Read the source

- `core.py`: public algorithm entry point and preserved original exercise.
- `pipeline.py`: featured implementation.
- `enhanced.js`: browser implementation, readable without a build system.
- `app.py`: localhost HTTP API.
- `test_*.py` and `test_enhanced.cjs`: behavior and edge cases.
- `benchmark.py`: evidence generator.

## Limitations

Only straight bright lanes are supported. Curves, night, occlusions, poor contrast and arbitrary photographs can fail. A false pair of lines can be returned. Inlier ratio is geometric agreement, not a calibrated probability. The synthetic benchmark does not measure road-image accuracy.

## Daily practical exercises

One dated fictional scenario runs daily through GitHub Actions. `exercises/YYYY-MM-DD/result.json` preserves inputs and outputs; `samples/latest.json` holds the latest input. Bot-authored report commits document script execution, not manual daily development. [Daily Spanish guide](EJERCICIOS_DIARIOS_ES.md).

## Authorship and relevance

Independent AI-assisted learning project in Erik Vera's portfolio. No affiliation with FOX, Tesla or BCG. The documentation distinguishes supplied implementation from improvements the learner actually makes. Code is MIT licensed; third-party data provenance is documented separately.

## Featured portfolio

- [Road Vision Lab](https://github.com/erickvera610/road-vision-lab)
- [Demand Forecasting Lab](https://github.com/erickvera610/consulting-demand-lab)
- [Media Prediction Lab](https://github.com/erickvera610/media-content-lab)
- [Classification Evaluation Lab](https://github.com/erickvera610/ml-model-lab)
- [Incident Workflow Lab](https://github.com/erickvera610/incident-response-lab)
