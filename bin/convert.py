#!/usr/bin/env python

import argparse
import os.path

import numpy
from PIL import Image


def normalize_raw(im, imsize, scale=8):
    cropsize = imsize * scale * 2
    assert im.width >= cropsize, "image is too small"
    assert im.height >= cropsize, "image is too small"

    wpad = (im.width - cropsize) // 2
    hpad = (im.height - cropsize) // 2
    if scale == 8:
        im = im.crop((wpad-2, hpad-2, wpad+2 + cropsize, hpad+2 + cropsize))
        im = im.resize((im.width // 4, im.height // 4), Image.BOX)
        im = im.resize((imsize * 2, imsize * 2), Image.NEAREST)
    else:
        im = im.crop((wpad, hpad, wpad + cropsize, hpad + cropsize))
        im = im.resize((imsize * 2, imsize * 2), Image.BOX)
    return im


def combine_raw(im, method='median', smooth=0):
    wsize, hsize = im.width // 2, im.height // 2
    rgb = numpy.array(im)
    rgb = numpy.stack([
        rgb[0    :hsize,   0    :wsize],
        rgb[0    :hsize,   wsize:wsize*2],
        rgb[hsize:hsize*2, 0    :wsize],
        rgb[hsize:hsize*2, wsize:wsize*2],
    ], axis=-1)
    rgb = getattr(numpy, method)(rgb, axis=-1)
    if smooth:
        rgb = smooth_rgb(rgb, smooth)
    return Image.fromarray(rgb.astype(numpy.uint8))


def smooth_rgb(rgb, sigma):
    try:
        import scipy.ndimage
    except ImportError:
        print("WARNING: scipy is required for smoothing.\n"
              "Try the following first:\n\n$ pip install scipy\n")
        return rgb
    shape = rgb.shape
    size = int(round((shape[0] * shape[1]) ** (1.0/3)))
    assert size**3 == shape[0] * shape[1], "Wrong cube size"
    rgb = rgb.reshape((size, size, size, 3))
    r = rgb[:, :, :, 0]
    g = rgb[:, :, :, 1]
    b = rgb[:, :, :, 2]
    r = scipy.ndimage.gaussian_filter(r, sigma, mode='nearest')
    g = scipy.ndimage.gaussian_filter(g, sigma, mode='nearest')
    b = scipy.ndimage.gaussian_filter(b, sigma, mode='nearest')
    rgb = numpy.stack((r, g, b), axis=-1).reshape(shape)
    return rgb


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert raw hald image to actual hald.')
    parser.add_argument('raw')
    parser.add_argument('dir', default='./', nargs='?')
    parser.add_argument('-s', '--size', type=int, default=5, nargs='?')
    parser.add_argument('-x', '--scale', type=int, default=8)
    parser.add_argument('-o', '--out')
    parser.add_argument('-m', '--method', choices=('mean', 'median'),
                        default='median')
    parser.add_argument('--smooth', type=float, default=0)
    args = parser.parse_args()

    im = Image.open(args.raw)
    im = normalize_raw(im, args.size**3, scale=args.scale)
    im = combine_raw(im, method=args.method, smooth=args.smooth)

    outfile = args.out
    if not outfile:
        outfile = os.path.splitext(os.path.basename(args.raw))[0]
        outfile = os.path.join(args.dir, outfile + '.png')
    im.save(outfile, format='png')
