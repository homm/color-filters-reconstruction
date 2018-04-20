#!/usr/bin/env python

import sys
import os.path

from PIL import Image
from pillow_lut import load_hald_image

dirname = './'
if len(sys.argv) > 3:
    dirname = sys.argv[3]
outfile = os.path.splitext(os.path.basename(sys.argv[2]))[0]

hald = load_hald_image(sys.argv[2])
im = Image.open(sys.argv[1])
im.filter(hald).save(os.path.join(dirname, outfile + '.jpg'))
