#!/bin/bash

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

make BootstrapFloppy.dsk

./NetBoot.py & cp xo.rom edit.rom && ./xo-rom-enable-netboot.py edit.rom && Mini\ vMac\ Classic.app/Contents/MacOS/minivmac edit.rom BootstrapFloppy.dsk && kill %1
