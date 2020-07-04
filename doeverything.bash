#!/bin/bash

trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

./NetBoot.py & cp xo.rom edit.rom && ./xo-rom-enable-netboot.py edit.rom && Mini\ vMac\ Classic.app/Contents/MacOS/minivmac edit.rom && kill %1
