image: systools607.dsk.a Makefile
	rm -rf /tmp/system6
	mkdir /tmp/system6
	DumpHFS systools607.dsk /tmp/system6


	cp MacsBug\ 6.2.2/MacsBug* /tmp/system6/System\ Folder/


	vasm-1/vasmm68k_mot -Fbin -pic -o /tmp/my-init init.a
	rfx cp /tmp/my-init /tmp/system6/System\ Folder/INIT//INIT/16
	/bin/echo -n INITelmo >/tmp/system6/System\ Folder/INIT.idump


	MakeHFS /tmp/system6.dsk -i /tmp/system6 -s 4M -n SexyDisk

	Mini\ vMac\ Classic.app/Co*/Ma*/* /tmp/system6.dsk


Bootstrap.bin: Bootstrap.a
	vasm-1/vasmm68k_mot -quiet -Fbin -pic -o $@ $<

BootstrapFloppy/System.rdump: Bootstrap.bin
	rfx cp $< $@//boot/1

BootstrapFloppy.dsk: BootstrapFloppy/System.rdump
	MakeHFS -n 'NetBoot Enabler' -i BootstrapFloppy -s 1440k -d now $@

testclient: BootstrapFloppy.dsk
	Mini\ vMac\ Classic.app/Co*/Ma*/* $<







BootWrapper.bin: BootWrapper.a
	vasm-1/vasmm68k_mot -quiet -Fbin -pic -o $@ $<

payload: BootWrapper.bin
	#echo ' dcb.w 10000, $$A9FF' >/tmp/xasm
	#vasm-1/vasmm68k_mot -quiet -Fbin -pic -o /tmp/yasm /tmp/xasm
	#cat /tmp/yasm >payload
	cat BootWrapper.bin systools607.dsk >payload
	python3 snefru_hash.py payload

BootServer.INIT: payload FORCE
	./buildapp.bash BootServer

testserver: BootServer.INIT
	rm -rf /tmp/bootserv; mkdir /tmp/bootserv
	cp systools607.dsk bootserv.tmp
	DumpHFS systools607.dsk /tmp/bootserv
	cp MacsBug\ 6.2.2/* /tmp/bootserv/System\ Folder
	cp BootServer.INIT* /tmp/bootserv/System\ Folder
	MakeHFS -i /tmp/bootserv -s 10m bootserv.tmp
	Mini\ vMac\ Classic.app/Co*/Ma*/* bootserv.tmp

pyserver: payload FORCE
	./NetBoot.py payload




testpicker: BootPicker.bin FORCE
	cp sys701-144.img bootpick.tmp
	dd if=BootPicker.bin of=bootpick.tmp bs=138 seek=1 conv=notrunc
	Mini\ vMac\ Classic.app/Co*/Ma*/* bootpick.tmp

BootPicker.bin: BootPicker.a
	vasm-1/vasmm68k_mot -quiet -Fbin -pic -o $@ $<




ChainLoader.bin: ChainLoader.a BootPicker.a
	vasm-1/vasmm68k_mot -quiet -Fbin -pic -o $@ $<

testchain: ChainLoader.bin FORCE
	zsh -c 'trap "kill %1" SIGINT SIGTERM EXIT; ./ChainBoot.py **/*.dsk & make testclient'



ServerDA.bin: ServerDA.a
	vasm-1/vasmm68k_mot -quiet -Fbin -pic -o $@ $<

ServerDA ServerDA.idump ServerDA.rdump: ServerDA.bin
	touch ServerDA ServerDA.idump
	/bin/echo -n dfilmovr >ServerDA.idump
	echo data "'DRVR'" '(12, "", purgeable) {};' >ServerDA.rdump
	rfx cp ServerDA.bin ServerDA.rdump//DRVR/12

testda: FORCE ServerDA ServerDA.idump ServerDA.rdump
	rm -rf /tmp/testda; mkdir -p /tmp/testda/Desktop\ Folder; cp ServerDA ServerDA.idump ServerDA.rdump /tmp/testda/Desktop\ Folder/
	MakeHFS -s 400k -n TestDA -d now -i /tmp/testda /tmp/testda.dsk
	rsync Big.dsk /tmp/Big.dsk
	Mini\ vMac\ Classic.app/Co*/Ma*/* /tmp/Big.dsk /tmp/testda.dsk




FORCE:
