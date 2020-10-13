#!/bin/bash

set -e

EXT=.INIT

for x; do
    touch "$x$EXT"
    echo -n 'INIT????' >"$x$EXT.idump"
    echo -n '' >"$x$EXT.rdump"

    for subfile in "$x"/*; do
        ./vasm-1/vasmm68k_mot -quiet -Fbin -pic -o /tmp/mytmp "$subfile"
        rspec="${subfile%.*}"
        rspec="$(basename "$rspec" | sed -E 's!([-[:digit:]])!/\1!')"
        rfx cp /tmp/mytmp "$x$EXT.rdump//$rspec"
    done
done
