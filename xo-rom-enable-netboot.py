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
    # Skip the initial PRAM check in forXO.a:InstallNetBoot
    f.seek(0x1d928)
    while f.tell() < 0x1D982:
        f.write(b'Nq') # nop

    # Find a safe place to store our overridden NetBoot config struct
    # (Which would otherwise be cobbled from various parts of PRAM)
    garbage_location = 0x67046 # The MacsBug copyright string in the ROM Disk

    # Make out own structure, as adapted from NetBoot.h
    the_netboot_structure = struct.pack('>BBBB BB 16s 32s 8s H', # Note that "int"s are 4 bytes, somehow!
        # First 4 bytes at PRAM+4
        1,                              # char    osType;         /* preferred os to boot from */
        1,                              # char    protocol;       /* preferred protocol to boot from */
        0,                              # char    errors;         /* last error in network booting */
        0xC0,                           # char    flags;          /* flags for: never net boot, boot first, etc. */

        # Now, the AppleTalk-protocol-specific part
        0,                              # unsigned char   nbpVars;        /* address of last server that we booted off of */
        0,                              # unsigned char   timeout;        /* seconds to wait for bootserver response */
        b'',                            # unsigned int    signature[4];   /* image signature */ Elliot notes: zeroes match anything!
        b'Elliot',                      # char            userName[31];   /* an array of char, no length byte */
        b'volapuk',                     # char            password[8];    /* '' */
        0xBABE,                         # short           serverNum;      /* the server number */
    ).ljust(72, b'\0')

    # the_netboot_structure = bytearray(the_netboot_structure)
    # for i, j in enumerate(range(54, len(the_netboot_structure))):
    #     the_netboot_structure[j] = i

    # This is the guts of the NetBoot ReadPRAM procedure
    f.seek(0x1DF08)
    write_asm(f, f'''
        move.l  a0,a1
        move.l  0x2ae,a0 ; RomBase
        add.l   #{hex(garbage_location)},a0
        move.l  #{hex(len(the_netboot_structure))},d0
        .2byte  0xA02E ; BlockMove
        rts
    ''')

    f.seek(garbage_location)
    f.write(the_netboot_structure)

    # Do the dodgy... cancel signature validation!
    f.seek(0x21A84)
    while f.tell() < 0x21A98:
        f.write(b'Nq') # nop

    # Work around Mini vMac's cutesy many-drives hack (it steals out preferred drivenum of 4 from us)
    f.seek(0x1DF51) # AddMyDrive: moveq #4,d9
    f.write(b'\x10')
    f.seek(0x1DFDF) # myExtFSFilter: cmp.w #4,d0
    f.write(b'\x10')

    # Enable this to make a SysError, for rudimentaly debug output
    for x in '9380'.split():
        x = eval('0x' + x)
        f.seek(x)
        f.write(assemble(f' move.l #{x},D0 \n .2byte  0xA9C9'))
