netBOOT for Old World Macs
==========================
Read this thread: https://mac68k.info/forums/thread.jspa?threadID=76&tstart=0

Now I'm trying to get it working! The dream is to boot all my Classics over PhoneNet.


Progress so far
---------------
The best build options for Mini vMac are: `-br 37 -m Classic -lt -speed z -as 0 -chr 0`. Note that this requires the new (as of mid-2020) version of Mini vMac, with Rob Mitchelmore's clever LocalTalk-over-UDP tunneling.

Run `make testchain` to boot an emulated Classic from a Python server.


Trivia
------
The Classic is the only non-IIci non-SuperMario ROM with .netBOOT and .ATBOOT drivers. They are part of the overpatch imposed on the SE ROM, and were essentially backported (see the SuperMario forXO.a file). I use the Classic ROM here because it can be emulated in Mini vMac, but the newer netBOOT-equipped ROMs should work.


Credits
-------
To all the intrepid individuals on the mac68k forum thread. Join Freenode #mac68k to meet them.

Thanks to my friends on #mac68k for their ongoing encouragement and assistance.

Credit to bbraun http://synack.net/~bbraun/ for the contents of the "bbraun-pram" dir.
