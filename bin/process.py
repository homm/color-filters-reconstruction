#!/usr/bin/env python

import sys
import os.path

import numpy
from PIL import Image

size = 5
if len(sys.argv) > 3:
    size = int(sys.argv[3])
imsize = size**3
cropsize = imsize*8*2

dirname = './'
if len(sys.argv) > 2:
    dirname = sys.argv[2]
outfile = os.path.splitext(os.path.basename(sys.argv[1]))[0]

im = Image.open(sys.argv[1])
assert im.width >= cropsize + 4, "image is too small"
assert im.height >= cropsize + 4, "image is too small"
padding = (im.width - cropsize) // 2
im = im.crop((padding-2, padding-2, padding+cropsize+2, padding+cropsize+2))
im = im.resize((im.width // 4, im.height // 4), Image.BOX)
im = im.resize((imsize * 2, imsize * 2), Image.NEAREST)

rgb = numpy.array(im)
arr = numpy.stack([
    rgb[0:imsize, 0:imsize], rgb[0:imsize, imsize:imsize*2],
    rgb[imsize:imsize*2, 0:imsize], rgb[imsize:imsize*2, imsize:imsize*2]
], axis=-1)
rgb = numpy.median(arr, axis=-1).astype(numpy.uint8)

im = Image.fromarray(rgb)
im.save(os.path.join(dirname, outfile + '.png'))
