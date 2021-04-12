#!/bin/bash

trap 'killall minivmac' SIGINT SIGTERM EXIT

n=0
for args; do
    Mini\ vMac\ Classic.app/Co*/Ma*/* $args &
    vmacs="$vmacs $!"
done

vmacs="{`echo $vmacs | tr ' ' ','`}"
echo $vmacs

osascript <<END
set n to 0
set allpids to $vmacs
repeat with mypid in allpids
	repeat
		tell application "System Events" to set allmatch to (every process whose unix id is mypid)
		if (count of allmatch) > 0 then exit repeat
		delay 0.1
	end repeat

	tell application "System Events" to tell (first process whose unix id is mypid)
		tell window 1
			set position to {(item 1 of (position as list)) + (n - ((count of allpids) - 1) / 2) * 1.02 * (item 1 of (size as list)), (item 2 of (position as list))}
		end tell
		set frontmost to true
	end tell
	set n to n + 1
end repeat
END

wait < <(jobs -p)
