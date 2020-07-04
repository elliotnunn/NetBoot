image: systools607.dsk.a Makefile
	rm -rf /tmp/system6
	mkdir /tmp/system6
	DumpHFS systools607.dsk /tmp/system6


	cp MacsBug\ 6.2.2/MacsBug* /tmp/system6/System\ Folder/


	vasm-1/vasmm68k_mot -Fbin -pic -o /tmp/my-init init.a
	rfx cp /tmp/my-init /tmp/system6/System\ Folder/INIT//INIT/16
	/bin/echo -n INITelmo >/tmp/system6/System\ Folder/INIT.idump


	MakeHFS /tmp/system6.dsk -i /tmp/system6 -s 4M -n SexyDisk

	Mini\ vMac\ Classic.app/Co*/Ma*/* xo.rom /tmp/system6.dsk


systools607.dsk.a: systools607.dsk
	python3 -c 'for b in open("systools607.dsk","rb").read(): print(" dc.b $$%02X" % b)' >systools607.dsk.a
