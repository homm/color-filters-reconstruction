# Accurate Instagram Filters Reconstruction

This repository includes tools which could be used for semi-automatically
and very accurate reconstruction of color filters used
in image processing software.
A vivid example of such filters is Instagram filters.

People like Instagram filters. They are trying to
[reproduce](https://github.com/girliemac/Filterous)
them [again](https://github.com/girliemac/filterous-2)
and [again](https://github.com/acoomans/instagram-filters).
And [again](https://github.com/lukexyz/CV-Instagram-Filters)
and [again](https://www.practicepython.org/blog/2016/12/20/instagram-filters-python.html).
And [again](https://code.tutsplus.com/tutorials/create-instagram-filters-with-php--net-24504)
and [again](https://picturepan2.github.io/instagram.css/).
The problem is most of this attempts based on manual color correction.

This is the only accurate reconstruction of color filters using a robust method.
For illustration, one of the following images obtained using Instagram filter
and second using applying accurate reconstruction.
Try to guess which one is which.

<img src="./static/reconstruction.jpg" width="400" alt="reconstruction"> <img src="./static/inst.jpg" width="400" alt="inst">

To compare, this is the result of applying **the same filter** from
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

This method can capture color transformations only where
no other variables are used for manipulations.
For example, vignetting, scratches, gradients and watermarks can't be captured.
It also captures wrong if different filters are used for transformations
in different parts of an image.


## Requirements

To generate and convert hald images you will need git
and a Python interpreter with pip.

```bash
$ git clone https://github.com/homm/color-transformations-reconstruction.git
$ cd color-transformations-reconstruction
$ pip install -r requirements.txt 
```

Prepared hald images coud be applyed to any image in your application
using GraphicsMagick bindings for Python, Ruby, PHP, Javascript™
and other programming languages or using command line interface.
No software from this repository is required.


## Guide

1. You need to create the identity image. For this simple run:

    ```bash
    $ ./bin/generate.py
    ```

    This will create `hald.5.png` file.
    The number in filename is square root of 3D table size.
    For example, 5 means 25×25×25 lookup table.

    <img src="./raw/0.original.png" width="400" alt="original">

    This file doesn't look like other hald images.
    This image is specially designed to oppose distortions
    which may occur during transformation, such as vignetting,
    scratches, gradients and JPEG artifacts.

2. Process the identity image with target software.
    Speaking of Instagram, you need to transfer identity image
    to the phone and post the image with one of the filters applied.
    After that, you'll see identity image with a filter in your camera roll.
    Then you need to transfer it back.

    <img src="./raw/1.Clarendon.jpg" width="400" alt="Clarendon">

    Before continuing, make sure that identity image with a filter
    has exactly the same resolution as source identity image.

3. Convert identity image with a filter to the true hald image:

    ```bash
    $ ./bin/convert.py raw/1.Clarendon.jpg halds/
    ```

    Where `halds/` is output folder.

    <img src="./halds/1.Clarendon.png" alt="Clarendon">

4. That is it!
    Now you can apply resulting hald image to any image.

    ```bash
    $ gm convert sample.jpg -hald-clut halds/1.Clarendon.png out.jpeg
    ```

    <img src="./static/sample.jpg" width="400" alt="sample"> <img src="./static/sample.1.jpg" width="400" alt="Clarendon">


## Advanced tips

While default parameters give high-quality hald filters,
there are some cases where it is not enough.
If the target filter haves heavy distortion on the local level
or significant gradients in the center of an image,
some undesired effects may occur.
The most noticeable is color banding.
This is an original image and image processed with the Hudson filter,
one of the most problematic from this point of view.

```bash
# Create hald image from processed by Instagram identity hald image
$ ./bin/convert.py raw/15.Hudson.jpg halds/
# Apply hald image to the sample image
$ gm convert girl.jpg -hald-clut halds/15.Hudson.png girl.15.jpg
```

<img src="./static/girl.jpg" width="400" alt="original"> <img src="./static/girl.15.jpg" width="400" alt="hudson">

On the processed image many objects look flat and posterized:
face, hair, chairs in the background.
While posterization is one of the common image filters,
it is not a part of the Hudson filter.

If you look closely at the [image with Hudson filter](./raw/15.Hudson.jpg),
you'll see that it looks noise and this is the root of the problem.

<img src="./static/hudson.jpg" width="400" alt="hudson">

Fortunately, you can ask `convert.py` to apply a gaussian blur
on the three-dimensional lookup table to reduce the noise.
You'll need to install [scipy][scipy] to continue.

```bash
# This needs only once
$ pip install scipy
$ ./bin/convert.py raw/15.Hudson.jpg halds/ --smooth 1.5
$ gm convert girl.jpg -hald-clut halds/15.Hudson.png girl.15.fixed.jpg
```

<img src="./static/girl.15.jpg" width="400" alt="hudson"> <img src="./static/girl.15.fix.jpg" width="400" alt="fixed hudson">

You can find additional options for `convert.py` with
`./bin/convert.py --help`.

Have fun with reverse engineering!

  [wiki-luts]: https://en.wikipedia.org/wiki/3D_lookup_table
  [hald-image]: http://www.quelsolaar.com/technology/clut.html
  [scipy]: https://www.scipy.org