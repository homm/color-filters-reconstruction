#!/usr/bin/env python

import argparse

import numpy
from PIL import Image


def generate_hald(size):
    b, g, r = numpy.mgrid[
        0 : 255 : size**2*1j,
        0 : 255 : size**2*1j,
        0 : 255 : size**2*1j
    ].astype(numpy.uint8)

    rgb = numpy.stack((r, g, b), axis=-1)
    return Image.fromarray(rgb.reshape(size**3, size**3, 3))


def fortify_hald(hald, scale=8, padding=0.4):
    hald = hald.resize((hald.width*scale, hald.height*scale), Image.NEAREST)
    w, h = hald.size
    wpad = int(w * padding / 16) * 16
    hpad = int(h * padding / 16) * 16

    bg = Image.new('RGB', ((w + wpad)*2, (h + hpad)*2), 'gray')
    bg.paste(hald, (wpad, hpad))
    bg.paste(hald, (wpad, hpad + h))
    bg.paste(hald, (wpad + w, hpad))
    bg.paste(hald, (wpad + w, hpad + h))
    return bg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates identity hald image.')
    parser.add_argument('-s', '--size' type=int, default=5)
    parser.add_argument('-x', '--scale', type=int, default=8)
    parser.add_argument('-p', '--padding', type=float, default=0.4)
    parser.add_argument('-o', '--out', default='hald.{}.png')
    args = parser.parse_args()

    hald = generate_hald(args.size)
    bg = fortify_hald(hald, scale=args.scale, padding=args.padding)
    bg.save(args.out.format(args.size), format='png')
