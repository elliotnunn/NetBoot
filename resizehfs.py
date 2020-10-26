#!/usr/bin/env python3

# MIT License

# Copyright (c) 2018 Elliot Nunn

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import struct


def alignment(num):
    # count trailing zero bits to a max of 32
    for i in reversed(range(33)):
        if num & ((1 << i) - 1) == 0: return i


def bitmap_len(drNmAlBlks):
    # how many bytes occupied by the 512b blocks required to make up n bits?
    num_512s = (drNmAlBlks + 4095) // 4096
    return num_512s * 512


def resize(img, freespace):
    drVBMSt, = struct.unpack_from('>H', img, 0x40E)
    drNmAlBlks, = struct.unpack_from('>H', img, 0x412)
    drAlBlkSiz, = struct.unpack_from('>L', img, 0x414)
    drAlBlSt, = struct.unpack_from('>H', img, 0x41C)
    drFreeBks, = struct.unpack_from('>H', img, 0x422)

    align = alignment(drAlBlSt)

    header = bytearray(img[:0x600])
    bitmap = img[drVBMSt*512:drVBMSt*512+bitmap_len(drNmAlBlks)]
    guts = img[drAlBlSt*512:drAlBlSt*512+drNmAlBlks*drAlBlkSiz]

    # Decide how much to shrink
    drFreeBks -= drNmAlBlks
    for drNmAlBlks in range(drNmAlBlks, 0, -1):
        byte = bitmap[(drNmAlBlks-1) >> 3]
        mask = 0x80 >> ((drNmAlBlks-1) & 7)
        if byte & mask: break
    drFreeBks += drNmAlBlks

    # Decide how much to expand
    while drNmAlBlks < 0xffff and drFreeBks * drAlBlkSiz < freespace:
        drFreeBks += 1
        drNmAlBlks += 1

    # Resize components
    bitmap = bitmap[:bitmap_len(drNmAlBlks)].ljust(bitmap_len(drNmAlBlks), b'\0')
    guts = guts[:drNmAlBlks*drAlBlkSiz].ljust(drNmAlBlks*drAlBlkSiz, b'\0')

    # Reposition the guts after the bitmap, preserving original alignment
    drAlBlSt = 3 + len(bitmap)//512
    while alignment(drAlBlSt) < align: drAlBlSt += 1

    struct.pack_into('>H', header, 0x40E, len(header)//512) # drVBMSt
    struct.pack_into('>H', header, 0x412, drNmAlBlks)
    struct.pack_into('>H', header, 0x41C, drAlBlSt)
    struct.pack_into('>H', header, 0x422, drFreeBks)

    accum = bytearray()
    accum.extend(header)
    accum.extend(bitmap)
    accum.extend(bytes(drAlBlSt*512 - len(accum)))
    accum.extend(guts)
    accum.extend(header[0x400:0x800])
    accum.extend(bytes(512))

    return accum


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='''
        Resize an HFS disk image by adding/removing allocation blocks.
        Warning: only images from `machfs` can be shrunk, because the
        real MacOS uses the allocation blocks at the end of the disk.
    ''')

    parser.add_argument('diskimage', metavar='PATH', action='store', help='disk image')
    parser.add_argument('--freespace', metavar='BYTES', action='store', type=int, default=0, help='free space target (0 means shrink)')
    parser.add_argument('--verbose', '-v', action='store_true', help='print stats')

    args = parser.parse_args()

    with open(args.diskimage, 'rb') as f:
        oldimage = f.read()

    if oldimage[1024:1026] != b'BD': sys.exit('Not an HFS volume')

    newimage = resize(oldimage, args.freespace)

    if args.verbose:
        for kind, img in (('old', oldimage), ('new', newimage)):
            drNmAlBlks, = struct.unpack_from('>H', img, 0x412)
            drFreeBks, = struct.unpack_from('>H', img, 0x422)
            print(kind, 'bytes:      ', len(img))
            print(kind, 'drNmAlBlks: ', drNmAlBlks)
            print(kind, 'drFreeBks:  ', drFreeBks)

        print('percentage size:', 100 * len(newimage) // len(oldimage))
        print('changed:        ', ('no' if newimage == oldimage else 'yes'))

    if newimage != oldimage:
        with open(args.diskimage, 'wb') as f:
            f.write(newimage)
