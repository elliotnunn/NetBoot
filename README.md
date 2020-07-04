netBOOT for Old World Macs
==========================
Read this thread: https://mac68k.info/forums/thread.jspa?threadID=76&tstart=0

Now I'm trying to get it working! The dream is to boot all my Classics over PhoneNet.


Progress so far
---------------
The best build options for Mini vMac are: `-br 37 -m Classic -lt -speed z -as 0 -chr 0`. Note that this requires the new (as of mid-2020) version of Mini vMac, with Rob Mitchelmore's clever LocalTalk-over-UDP tunneling.

The xo-rom-enable-netboot.py script can edit xo.rom (Macintosh Classic) to force-enable the netBOOT driver (essentially by editing PRAM). (It requires you to build vasm with a quick `make CPU=m68k SYNTAX=std`.) This enables quick iteration:

	cp xo.rom edit.rom && ./xo-rom-enable-netboot.py edit.rom&& Mini\ vMac\ Classic.app/Co*/Ma*/* edit.rom

Running NetBoot.py simultaneously now shows the netBOOT driver sending DDP packets.

(Some progress that I didn't bother writing about)

It works! (Albeit with a heavily patched Classic ROM.)


Trivia
------
The Classic is the only non-IIci non-SuperMario ROM with .netBOOT and .ATBOOT drivers. They are part of the overpatch imposed on the SE ROM, and were essentially backported (see the SuperMario forXO.a file). I use the Classic ROM here because it can be emulated in Mini vMac, but the newer netBOOT-equipped ROMs should work.


Credits
-------
To all the intrepid individuals on the mac68k forum thread. Join Freenode #mac68k to meet them.

Credit to bbraun http://synack.net/~bbraun/ for the contents of the "bbraun-pram" dir.
