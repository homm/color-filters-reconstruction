# Accurate Color Transformations Capture

This repository includes tools which could be used for semi-automatically
and very accurate reconstruction of color filters used
in image processing software.
A vivid example of such filters is Instagram filters.

This is the first and only attempt to accurately reconstruct
color filters using robust methods instead of manual color correction.
For clarity, one of this images obtained using one of Instagram filters
and second using applying accurate reconstruction.
Try to guess which one is which.

<img src="./static/reconstruction.jpg" width="400" alt="reconstruction"> <img src="./static/inst.jpg" width="400" alt="inst">

To compare, this is the result of the **filter with same name** from
a commercial set of Instagram-like filters.

<img src="./static/foreign.jpg" width="400" alt="foreign">

[Source image](./static/source.jpg)

## How it works

This method based on [three-dimensional lookup tables][wiki-luts]
and their two-dimensional representation: [hald images][hald-image].
The idea is very simple: a sample hald image with uniform color distribution
is processed using target software with unknown color transformation algorithm.
After processing such hald image could be used as a filter
for a very accurate approximation for the target color transformation.

A resulting hald image could be used in various software such as
GraphicsMagick and Adobe Photoshop (with plugins) and converted to
3D LUT cube file format, which is common for a great number
of video editing software.

## Limitation

This method can restore only color transformations where
no other variables are used for manipulations.
For example, vignetting, scratches, gradients, watermarks can't be captured.
It also captures wrong if different filters are used for transformations
in different parts.

## Requirements

To generate and process sample image Python interpreter with pip is required.

```bash
$ pip install -r ./requirements.txt 
```

You can apply resulting hald images using GraphicsMagick.

## Operating principle

1. You need to create 

  <img src="./raw/0.original.png" width="400" alt="original"> <img src="./res/pineapple.hefe.jpeg" width="400" alt="filtered">



  [wiki-luts]: https://en.wikipedia.org/wiki/3D_lookup_table
  [hald-image]: http://www.quelsolaar.com/technology/clut.html