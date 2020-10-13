#!/bin/bash

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

make BootstrapFloppy.dsk

Mini\ vMac\ Classic.app/Contents/MacOS/minivmac xo.rom BootstrapFloppy.dsk && kill %1
