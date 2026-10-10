# Case study: Road Vision Lab

## 1. Problem and intended user

The original demo fitted coordinates supplied by the generator. This version extracts candidate pixels from a grayscale image and estimates lines with RANSAC. A synthetic road scene supplies known geometry; visitors can also upload a local PNG/JPEG/WebP photograph.

## 2. Data and information flow

Image pixels → grayscale ROI → gradients → RANSAC → line overlay

## 3. Why these choices

A fixed lower-image ROI, bright-pixel threshold and horizontal gradient reject much of the background. RANSAC tolerates some bright distractors, then least-squares refits the inliers. A fixed seed makes the exercise reproducible. No neural detector is claimed.

## 4. Reproducible evidence

| Measurement | Result |
|---|---|
| detected scenes | 10 |
| scene count | 10 |
| mean width error px | 1.5178 |
| blank image detected | False |

Generated at 2026-10-10T18:37:09.311034+00:00 by the Python benchmark. Read every run in [benchmark-results.json](benchmark-results.json). These results apply only to the documented benchmark. No production performance claim is made.

## 5. What could go wrong

Only straight bright lanes are supported. Curves, night, occlusions, poor contrast and arbitrary photographs can fail. A false pair of lines can be returned. Inlier ratio is geometric agreement, not a calibrated probability. The synthetic benchmark does not measure road-image accuracy.

## 6. Next substantive improvement

Añade escenas con sombras y curvas; registra cuándo falla en lugar de cambiar las imágenes para ocultarlo. Luego añade un dataset de imágenes con licencia y anotaciones, separando escenas de entrenamiento y prueba.

Open an issue, create a branch, implement the improvement, run the checks, and explain the change in a pull request. Do not describe automated report commits as personal code development.
