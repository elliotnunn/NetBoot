#!/usr/bin/env python3

import sys
import argparse
import struct

args = argparse.ArgumentParser(description='32x32 BMP to assembly icon (non-B&W becomes transparent)')
args.add_argument('bmp', help='BMP file')
args = args.parse_args()

bmp = open(args.bmp, 'rb').read()

sig, fsize, pixoffset, w, h = struct.unpack_from('<HLxxxxLxxxxLl', bmp)
h = abs(h)

if w != 32: sys.exit('width must be 32')

pixels = []
mask = []

for row in range(h):
    row_pix = ''
    row_mask = ''

    for col in range(w):
        px, = struct.unpack_from('<L', bmp, pixoffset + row*w*4 + col*4)

        white = bool(px & 0x00FFFFFF)
        opaque = bool(px & 0xFF000000)

        row_pix += str(int(opaque and not white))
        row_mask += str(int(opaque))

    pixels.append(row_pix)
    mask.append(row_mask)

for i in pixels+mask:
    print('            dc.l    %' + i)
