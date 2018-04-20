#!/usr/bin/env python

import sys

import numpy
from PIL import Image

size = 5
if len(sys.argv) > 1:
    size = int(sys.argv[1])

b, g, r = numpy.mgrid[
    0 : 255 : size**2*1j,
    0 : 255 : size**2*1j,
    0 : 255 : size**2*1j
].astype(numpy.uint8)


imsize = size**3
rgb = numpy.stack((r, g, b), axis=-1).reshape(imsize, imsize, 3)

imsize = imsize*8
im = (Image.fromarray(rgb)
      .resize((imsize, imsize), Image.NEAREST))
padding = int(imsize*0.4 / 16) * 16
bg = Image.new('RGB', ((imsize+padding)*2, (imsize+padding)*2), 'gray')
bg.paste(im, (padding, padding))
bg.paste(im, (padding, imsize+padding))
bg.paste(im, (imsize+padding, padding))
bg.paste(im, (imsize+padding, imsize+padding))
bg.save('hald.{}.png'.format(size))
