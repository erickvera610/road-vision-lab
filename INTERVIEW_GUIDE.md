# Interview Guide

## 60-second explanation

I built a classical computer-vision pipeline for real road images using HSV color filtering, Canny edges, a road ROI, Hough line segments, seeded RANSAC, and geometry checks. I then stress-tested it under controlled brightness, blur, and noise conditions. A key design choice is that the project does not call a detected pair “accuracy”; without independent lane annotations, detection only means the pipeline found geometrically supported candidate lines. The adaptive illumination mode improves output availability in darkened images, but I also document the risk that normalization can amplify distractors.

## Questions I should be able to answer

- Why HSV instead of RGB thresholds?
- What does Canny contribute after the color mask?
- Why use an ROI?
- Why RANSAC after Hough segments?
- What failure cases do the geometry checks reject?
- Why is supported output not the same as lane accuracy or IoU?
- What would an annotated deep-learning lane-segmentation extension require?

## Strong limitation statement

The current real-image set is small and was used during development. There is no independent annotated lane benchmark in this repository, so I report robustness of output availability, not verified lane accuracy.

## 20-second recruiter version

Real-image OpenCV project with explainable geometry, robustness testing, negative controls, API validation, Docker, CI, and explicit failure reporting. It demonstrates computer-vision engineering and careful metric interpretation rather than overstating results.
