#!/usr/bin/env python3

import sys
import struct



# Awful hack to run code through vasm
def assemble(the_code):
    with open('/tmp/vasm.elliot', 'w') as f:
        f.write(the_code)

    import os
    from os import path
    assembler = path.join(path.dirname(path.abspath(__file__)), 'vasm-1/vasmm68k_std')
    os.system(f'{assembler} -quiet -Fbin -pic -o /tmp/vasm.elliot.bin /tmp/vasm.elliot')

    with open('/tmp/vasm.elliot.bin', 'rb') as f:
        return f.read()

def write_asm(f, asm):
    f.write(assemble(f' .org {hex(f.tell())} \n rom: \n {asm}'))



with open(sys.argv[1], 'r+b') as f:
    # I have implemented Snefru, so this is no longer needed:
    # Do the dodgy... cancel signature validation!
    # f.seek(0x21A84)
    # while f.tell() < 0x21A98:
    #     f.write(b'Nq') # nop

    # Work around Mini vMac's cutesy many-drives hack (it steals out preferred drivenum of 4 from us)
    f.seek(0x1DF51) # AddMyDrive: moveq #4,d9
    f.write(b'\x10')
    f.seek(0x1DFDF) # myExtFSFilter: cmp.w #4,d0
    f.write(b'\x10')

    # Enable this to make a SysError, for rudimentaly debug output
    # for x in '218DA'.split():
    #     x = eval('0x' + x)
    #     f.seek(x)
    #     f.write(assemble(f' move.l #{x},D0 \n .2byte  0xA9C9'))
