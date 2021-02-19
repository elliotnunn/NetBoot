#!/usr/bin/env python3

import sys
import argparse
import struct

args = argparse.ArgumentParser(description='32x32 BMP to assembly icon (non-B&W becomes transparent)')
args.add_argument('bmp', help='BMP file')
args = args.parse_args()

bmp = open(args.bmp, 'rb').read()

sig, fsize, pixoffset = struct.unpack_from('<HLxxxxL', bmp)

pixels = [0] * 32 * 32
mask = [0] * 32 * 32

for i in range(32*32):
    px, = struct.unpack_from('<L', bmp, pixoffset+i*4)
    white = int((px & 0x00FFFFFF) == 0x00FFFFFF)
    clear = int((px & 0xFF000000) == 00)

    pixels[i] = int(0 if clear else not white)
    mask[i] = int(not clear)

as_str = ''.join(str(x) for x in (pixels + mask))

for i in range(0, 32*32*2, 32):
    print('            dc.l    %' + as_str[i:i+32])
