#!/bin/sh

mkdir -p manysystems.tmp; ls baseofmanysystems | grep ^System | grep -v dump$ | while read -r x; do rsync -a --delete --delete-excluded --include "$x*" --exclude='System *' baseofmanysystems /tmp/; MakeHFS -s 20m -i /tmp/baseofmanysystems -n "$x" manysystems.tmp/"$x".dsk; done
