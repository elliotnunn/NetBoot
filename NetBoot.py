#!/usr/bin/env python3

# Multicast client
# Adapted from: http://chaos.weblogs.us/archives/164

import socket
import os
from os import path
import struct

import time

from snefru_hash import snefru




# ; the below code might come in handy later on, when we support executable boot blocks.
# CodeToUncorruptTheBootBlocks:
#     move.l  (SP),A1
#     sub.l   #8,A1                   ; What will be the start address of the boot blocks??

#     lea     BigDiskImage,A0
#     move.l  #1024,D0
#     dc.w    0xA02E                  ; BlockMove

#     sub.l   #6,(SP)                 ; Re-run the code that called us; it will be real boot blocks now!
#     rts






my_unique_ltoudp_id = b'El' + (os.getpid() & 0xFFFF).to_bytes(2, 'big')



disk_image = open(path.join(path.dirname(path.abspath(__file__)), 'systools607.dsk'), 'rb').read()



def assemble(the_code):
    with open('/tmp/vasm.bootblocks', 'w') as f:
        f.write(the_code)

    try:
        os.remove('/tmp/vasm.bootblocks.bin')
    except FileNotFoundError:
        pass

    assembler = path.join(path.dirname(path.abspath(__file__)), 'vasm-1/vasmm68k_mot')
    os.system(f'{assembler} -quiet -Fbin -pic -o /tmp/vasm.bootblocks.bin /tmp/vasm.bootblocks')

    with open('/tmp/vasm.bootblocks.bin', 'rb') as f:
        return f.read()




# typedef short (*j_code)(    short       command,  # SP+4 (sign-extend to long)
#                             DGlobals    *g,       # SP+8
#                             int         **var1,   # SP+12
#                             int         **var2);  # SP+16

# We return our OSErr in d0, and leave the 16 bytes of arguments on the stack for the caller to clean

image = assemble(f'''
myUnitNum       equ     52
myDRefNum       equ     ~myUnitNum


Code
            cmp.l   #1,4(SP)
            beq     getBootBlocks
            cmp.l   #2,4(SP)
            beq     getSysVol
            cmp.l   #3,4(SP)
            beq     mountSysVol

            move.l  #-1,d0
            rts


getBootBlocks
            lea     DiskImage,A0
            move.l  8(SP),A1                ; Inside the global struct...
            add.l   #$BA,A1                 ; ...is an element for the structured part of the boot blocks
            move.l  #138,D0                 ; ...of this length

            dc.w    $A02E                  ; BlockMove

            bra     return

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

getSysVol
    ; Our register conventions:
    ;   A2 = fake dqe; A3 = dce; A4 = copied driver

            link    A6,#-$32
            movem.l A2-A4/D3,-(SP)

    ; Now I copy all this stuff under BufPtr (because this current location will disappear)
            sub.l   #(BufPtrCopyEnd-BufPtrCopy),$10C        ; BufPtr
            move.l  $10C,A4                                 ; ... into A4

    ; Copy the driver and image as one chunk
            lea     BufPtrCopy,A0
            move.l  A4,A1
            move.l  #(BufPtrCopyEnd-BufPtrCopy),D0
            dc.w    $A02E                                   ; BlockMove

    ; Truncate this block to reduce heap fragmentation
            lea     Code,A0
            move.l  #BufPtrCopy-Code,D0
            dc.w    $A020                                   ; _SetPtrSize

    ; Install the driver in the unit table
            move.l  #myDRefNum,D0
            dc.w    $A43D                                   ; _DrvrInstall ReserveMem
            bne     error

    ; Get DCE handle of installed driver
            move.l  $11C,A0                                 ; UTableBase
            add.l   #myUnitNum*4,A0
            move.l  (A0),A3

    ; Lock it down
            move.l  A3,A0
            dc.w    $A029                                   ; _HLock

    ; Populate the empty DCE that DrvrInstall left us
            move.l  (A3),A0                                 ; A0 = dce ptr

            move.l  A4,0(A0)                                ; dCtlDriver is pointer (not hdl)

            move.w  0(A4),D0                                ; drvrFlags
            and.w   #~$0040,D0                              ; Clear dRAMBased bit (to treat dCtlDriver as a pointer)
            move.w  D0,4(A0)                                ; dCtlFlags

    ; Copy these other values that apparently the Device Mgr forgets
            move.w  2(A4),$22(A0)                           ; drvrDelay to dCtlDelay
            move.w  4(A4),$24(A0)                           ; drvrEMask to dCtlEMask
            move.w  6(A4),$26(A0)                           ; drvrMenu to dCtlMenu

    ; Open the driver
            lea     -$32(A6),A0
            bsr     clearblock
            lea     DrvrNameString,A1
            move.l  A1,$12(A0)                              ; IOFileName
            dc.w    $A000                                   ; _Open
            bne     error

    ; Create a DQE
            move.l  #$16,D0
            dc.w    $A71E                                   ; _NewPtr ,Sys,Clear
            add.l   #4,A0                                   ; has some cheeky flags at negative offset
            move.l  A0,A2

    ; Point our caller to the fake dqe
            move.l  4+12(A6),A1
            move.l  A2,(A1)

    ; Find a free drive number (nicked this code from BootUtils.a:AddMyDrive)
            LEA     $308,A0                     ; [DrvQHdr]
            MOVEQ   #4,D3                       ; start with drive number 4
CheckDrvNum
            MOVE.L  2(A0),A1                    ; [qHead] start with first drive
CheckDrv
            CMP.W   6(A1),D3                    ; [dqDrive] does this drive already have our number?
            BEQ.S   NextDrvNum                  ; yep, bump the number and try again.
            CMP.L   6(A0),A1                    ; [qTail] no, are we at the end of the queue?
            BEQ.S   GotDrvNum                   ; if yes, our number's unique! Go use it.
            MOVE.L  0(A1),A1                    ; [qLink] point to next queue element
            BRA.S   CheckDrv                    ; go check it.

NextDrvNum
    ; this drive number is taken, pick another

            ADDQ.W  #1,D3                       ; bump to next possible drive number
            BRA.S   CheckDrvNum                 ; try the new number
GotDrvNum

    ; Populate the DQE
            move.l  #$80080000,-4(A2)                       ; secret flags, see http://mirror.informatimago.com/next/developer.apple.com/documentation/mac/Files/Files-112.html
            move.w  #1,4(A2)                                ; qType
            move.w  #(DiskImageEnd-DiskImage)&$FFFF,$C(A2)  ; dQDrvSz
            move.w  #(DiskImageEnd-DiskImage)>>16,$E(A2)    ; dQDrvSz2
            move.w  #0,$A(A2)                               ; dQFSID should be for a native fs

            lea     gDQEAddr,A0
            move.l  A2,(A0)

    ; Into the drive queue (which will further populate the DQE)
            move.l  A2,A0                                   ; A0 = DQE ptr
            move.w  D3,D0
            swap.w  D0                                      ; D0.H = drive number
            move.w  #myDRefNum,D0                           ; D0.L = driver refnum
            dc.w    $A04E                                   ; _AddDrive
            bne     error

    ; Save this most precious knowledge for later
            lea     gDriveNum,A0
            move.w  D3,(A0)

    ; Clean up our stack frame
            movem.l (SP)+,A2-A4/D3
            unlk    A6

            bra     return

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

mountSysVol
            link    A6,#-$32
            movem.l A2-A4/D3,-(SP)

            lea     gDriveNum,A0
            move.w  (A0),D3

    ; Set aside the FS queue to stop MountVol jamming up
            move.w  $360,-(SP)      ; FSBusy
            move.l  $362,-(SP)      ; FSQHead
            move.l  $366,-(SP)      ; FSQTail
            clr.w   $360
            clr.l   $362
            clr.l   $366

    ; MountVol
            lea     -$32(A6),A0
            bsr     clearblock
            move.w  D3,$16(A0)                              ; ioVRefNum = ioDrvNum = the drive number
            dc.w    $A00F                                   ; _MountVol

    ; Restore the FS queue
            move.l  (SP)+,$366
            move.l  (SP)+,$362
            move.w  (SP)+,$360

    ; Tattle about the DQE and VCB
            move.l  4+12(A6),A1
            move.l  $356+2,A0                               ; VCBQHdr.QHead (maybe I should be clever-er)
            move.l  A0,(A1)

            move.l  4+16(A6),A1
            lea     gDQEAddr,A0
            move.l  (A0),(A1)

            movem.l (SP)+,A2-A4/D3
            unlk    A6

return
            move.l  #0,d0
            rts

error
            dc.w    $A9C9


clearblock
            clr.w   $0(A0)
            clr.w   $2(A0)
            clr.w   $4(A0)
            clr.w   $6(A0)
            clr.w   $8(A0)
            clr.w   $a(A0)
            clr.w   $c(A0)
            clr.w   $e(A0)
            clr.w   $10(A0)
            clr.w   $12(A0)
            clr.w   $14(A0)
            clr.w   $16(A0)
            clr.w   $18(A0)
            clr.w   $1a(A0)
            clr.w   $1c(A0)
            clr.w   $1e(A0)
            clr.w   $20(A0)
            clr.w   $22(A0)
            clr.w   $24(A0)
            clr.w   $26(A0)
            clr.w   $28(A0)
            clr.w   $2a(A0)
            clr.w   $2c(A0)
            clr.w   $2e(A0)
            clr.w   $30(A0)
            rts


DrvrNameString
            dc.b    11, ".netRamDisk"


gDriveNum   dc.w    0
gDQEAddr    dc.l    0


; code on this side is for start only, and stays in the netBOOT driver globals until released

BufPtrCopy

; code on this side gets copied beneath BufPtr (is that the best place??)


; Shall we start with a driver?
DrvrBase
            dc.w    $4F00           ; dReadEnable dWritEnable dCtlEnable dStatEnable dNeedLock
            dc.w    0               ; delay
            dc.w    0               ; evt mask
            dc.w    0               ; menu

            dc.w    DrvrOpen-DrvrBase
            dc.w    DrvrPrime-DrvrBase
            dc.w    DrvrControl-DrvrBase
            dc.w    DrvrStatus-DrvrBase
            dc.w    DrvrClose-DrvrBase
            dc.b    11, ".netRamDisk"

; a0=iopb, a1=dce on entry to all of these...

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DrvrOpen
            move.w  #0,$10(A0)      ; ioResult
            rts

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DrvrPrime
            movem.l A0-A1/D0-D2,-(SP)

            cmp.b   #2,$7(A0)       ; ioTrap == aRdCmd
            bne.s   notRead

    ; D1 = image offset
            move.l  $10(A1),D1      ; Device Mgr gives us dCtlPosition

    ; D0 = number of bytes
            move.l  $24(A0),D0      ; ioReqCount
            move.l  D0,$28(A0)      ; -> ioActCount

    ; Advance the pointer
            move.l  D1,D2
            add.l   D0,D2           ; calculate new position
            move.l  D2,$10(A1)      ; -> dCtlPosition

    ; Do the dirty (we are just about to trash A0, so use it first)
            move.w  #0,$10(A0)      ; ioResult
            move.l  $20(A0),A1      ; ioBuffer
            lea     DiskImage,A0
            add.l   D1,A0
            dc.w    $A02E           ; BlockMove

            bra.s   primeFinish

notRead
            cmp.b   #3,7(A0)        ; ioTrap == aRdCmd
            bne.s   primeFinish

    ; D1 = image offset
            move.l  $10(A1),D1      ; Device Mgr gives us dCtlPosition

    ; D0 = number of bytes
            move.l  $24(A0),D0      ; ioReqCount
            move.l  D0,$28(A0)      ; -> ioActCount

    ; Advance the pointer
            move.l  D1,D2
            add.l   D0,D2           ; calculate new position
            move.l  D2,$10(A1)      ; -> dCtlPosition

    ; Do the dirty (we are just about to trash A0, so use it first)
            move.w  #0,$10(A0)      ; ioResult
            move.l  $20(A0),A0      ; ioBuffer
            lea     DiskImage,A1
            add.l   D1,A1
            dc.w    $A02E           ; BlockMove

primeFinish
            movem.l (SP)+,A0-A1/D0-D2
            bra     DrvrFinish

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DrvrControl
            move.w  #-18,$10(A0)     ; ioResult
            bra     DrvrFinish

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DrvrStatus
            cmp.w   #6,$1A(A0)
            beq.s   status_fmtLstCode
            cmp.w   #8,$1A(A0)
            beq.s   status_drvStsCode
            bra.s   status_unknown

status_fmtLstCode ; tell them about our size
            move.l  A2,-(SP)

            move.w  #1,$1C(A0)
            move.l  $1C+2(A0),A2
            move.l  #(DiskImageEnd-DiskImage),0(A2)
            move.l  #$40000000,4(A2)

            move.l  (SP)+,A2

            move.w  #0,$10(A0)          ; ioResult = statusErr
            bra     DrvrFinish

status_drvStsCode ; tell them about some of our flags
            move.w  #0,$1C(A0)          ; csParam[0..1] = track no (0)
            move.l  #80080000,$1C+2(A0) ; csParam[2..5] = same flags as dqe
            
            move.w  #0,$10(A0)          ; ioResult = noErr
            bra     DrvrFinish

status_unknown
            move.w  $1A(A0),D0          ; dodgy, for debugging
            add.w   #$3000,D0
            dc.w    $A9C9

            move.w  #-18,$10(A0)        ; ioResult
            bra     DrvrFinish

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DrvrClose
            move.w  #$4444,D0
            dc.w    $A9C9

            move.w  #0,$10(A0)      ; ioResult
            rts

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

DrvrFinish
            move.w  6(A0),D1        ; iopb.ioTrap
            btst    #9,D1           ; noQueueBit
            bne.s   DrvrNoIoDone
            move.l  $8FC,-(SP)      ; jIODone
DrvrNoIoDone
            rts


DiskImage {chr(10).join(' dc.b ' + str(x) for x in disk_image)}
DiskImageEnd

BufPtrCopyEnd
''')




image = bytearray(image)

while len(image) % 512 != 512 - 64: image.append(0)
the_hash = snefru(image)
while len(image) % 512 != 512 - 16: image.append(0)
image.extend(the_hash)
print('Sig:', ''.join(('%02X' % b) for b in image[-16:]))


ANY = "0.0.0.0"
MCAST_ADDR = "239.192.76.84"
MCAST_PORT = 1954

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP) # IPPROTO_UDP could just be 0

# Allow multiple sockets to use the same PORT number
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)

# Bind to the port that we know will receive multicast data
sock.bind((ANY,MCAST_PORT))

# Tell the kernel that we want to add ourselves to a multicast group
# The address for the multicast group is the third param
status = sock.setsockopt(socket.IPPROTO_IP,
socket.IP_ADD_MEMBERSHIP,
socket.inet_aton(MCAST_ADDR) + socket.inet_aton(ANY))



# Wrap up in all sorts of crap...
def mk_ddp(dest_node, dest_socket, src_node, src_socket, proto_type, data):
    # Wrap into DDP datagram
    data = struct.pack('>HBBB', len(data) + 5, dest_socket, src_socket, proto_type) + data

    # Wrap into LLAP packet
    data = struct.pack('>BBB', dest_node, src_node, 1) + data

    # Wrap the novel LToUDP header
    data = my_unique_ltoudp_id + data

    return data



def pstring(x):
    try:
        x = x.encode('mac_roman')
    except AttributeError:
        pass

    return bytes([len(x)]) + x



while 1:
    data, addr = sock.recvfrom(1024)

    # Okay... LToUDP parsing here. Let's start with the LLAP packet.
    # Man, chaining protocols is hard. This will inevitably require a rewrite.
    # Be careful to keep this as one cascading thing...

    if len(data) < 4: continue
    if data.startswith(my_unique_ltoudp_id): continue
    data = data[4:] # Trim down to LLAP packet (not "frame")

    if len(data) < 3: continue
    llap_dest_node = data[0]
    llap_src_node = data[1]
    llap_proto_type = data[2]
    data = data[3:] # Trim down to LLAP payload

    # Try to extract a DDP header, which is all we want!
    if llap_proto_type == 1:
        # ddp, short
        if len(data) < 5: continue
        ddp_len, ddp_dest_socket, ddp_src_socket, ddp_proto_type = struct.unpack_from('>HBBB', data)
        data = data[5:ddp_len]
    elif llap_proto_type == 2:
        # ddp, long (what should we do with this extra information?)
        if len(data) < 13: continue
        ddp_len, ddp_cksum, ddp_dest_net, ddp_src_net, ddp_dest_node, ddp_src_node, ddp_dest_socket, ddp_src_socket = struct.unpack_from('>4H5B', data)
        ddp_hop_count = (ddp_len >> 10) & 0xF
        ddp_len &= 0x3FF
        data = data[13:ddp_len]
    else:
        # llap control packet -- can probably ignore!
        continue

    print(f'datagram {llap_src_node}:{ddp_src_socket}->{llap_dest_node}:{ddp_dest_socket}', end='  ')

    if ddp_proto_type == 2:
        # Name Binding Protocol

        if len(data) < 2: continue
        nbp_func = data[0] >> 4
        nbp_tuple_cnt = data[0] & 0xF
        nbp_id = data[1]
        data = data[2:]

        nbp_tuples = []
        while data and len(nbp_tuples) < nbp_tuple_cnt:
            if len(data) < 5: break
            this_tuple = list(struct.unpack_from('>HBBB', data))
            data = data[5:]
            for i in range(3):
                # This should be coded more defensively, perhaps using exceptions
                this_tuple.append(data[1:1+data[0]].decode('mac_roman'))
                data = data[1+data[0]:]
            nbp_tuples.append(tuple(this_tuple))


        print('nbp func', nbp_func, 'id', nbp_id)
        for t in nbp_tuples:
            print(f'    net:node:sock={t[0]}:{t[1]}:{t[2]} enum={t[3]} object:type@zone={t[4]}:{t[5]}@{t[6]}')

        if nbp_func == 2:
            # NBP LkUp

            if len(nbp_tuples) == 1 and nbp_tuples[0][5] == 'BootServer': # Looking for us
                sock.sendto(mk_ddp(
                    dest_node=llap_src_node, dest_socket=ddp_src_socket,
                    src_node=99, src_socket=99,
                    proto_type=2,
                    data=bytes([0x31, nbp_id]) + # 3=LkUp-Reply, 1=number-of-tuples
                    struct.pack('>HBBB', # Pack the first tuple
                        0,                  # (My) Network number
                        99,                 # (My) Node ID
                        99,                 # (My) Socket number
                        0,                  # (My) Enumerator (i.e. which of many possible names for 99/99 is this?)
                    ) +
                    pstring(nbp_tuples[0][5]) + pstring('BootServer') + pstring('*')
                ),
                (MCAST_ADDR, MCAST_PORT))

    elif ddp_proto_type == 10:
        # Mysterious ATBOOT protocol

        if len(data) < 2: continue
        boot_type, boot_vers = struct.unpack_from('>BB', data)
        data = data[2:]

        # rbNullCommand       EQU     0                       ; ignore this one
        # rbMapUser           EQU     1                       ; user record request
        # rbUserReply         EQU     2                       ; user record reply
        # rbImageRequest      EQU     3                       ; image request & bitmap
        # rbImageData         EQU     4                       ; image data
        # rbImageDone         EQU     5                       ; server done with current image
        # rbUserRecordUpdate  EQU     6                       ; new user info to server
        # rbUserRecordAck     EQU     7                       ; info received from server

        if boot_type == 1:
            # It might be neater to trim off the "type" and "version" fields a bit earlier
            boot_machine_id, boot_timestamp, boot_username = struct.unpack_from('>HL 34p', data)

            print(f'atboot type={boot_type}, vers={boot_vers}, machineID={boot_machine_id}, userName={boot_username}')

            # // This defines a user record.
            # // Some of these fields can be determined on the fly by the boot server,
            # // while others are stored on disk by the boot server
            # typedef struct
            # {
            #     char    serverName[serverNameLength];   // server name to boot off of 
            #     char    serverZone[zoneNameLength];     // and the zone it lives in
            #     char    serverVol[volNameLength];       // the volume name
            #     short   serverAuthMeth;                 // authentication method to use (none, clear txt, rand)
            #     unsigned    long    sharedSysDirID;     // dir id of shared system folder
            #     unsigned    long    userDirID;          // dir id of the user's private system folder
            #     unsigned    long    finderInfo[8];      // blessed folder dir id, startup folder dir id etc...
            #     unsigned    char    bootBlocks[138];    // see Inside Mac V-135
            #     unsigned    short   bootFlag;           // server based flags
            #     unsigned    char    pad[306-18];        // <pd 5>pad to ddpMaxData
            # }userRecord;

            # // This defines the user record reply sent to workstations.
            # typedef struct
            # {
            #     unsigned    char        Command;    /* record or image request command word */
            #     unsigned    char        pversion;   /* version of boot protocol spoken by requestor */
            #     unsigned    short       osID;       /* type and version of os */
            #     unsigned    int         userData;   /* time stamp goes here */
            #     unsigned    short       blockSize;  /* size of blocks we will send */
            #     unsigned    short       imageID;    /* image ID */
            #     short                   result;     /* error codes */
            #     unsigned    int         imageSize;  /* size of image in blocks */
            #     userRecord  userRec;    /* tell user where to go */
            # }BootPktRply;

            # Ignore the silly user record. Just make the fucker work!
            sock.sendto(mk_ddp(
                dest_node=llap_src_node, dest_socket=ddp_src_socket,
                src_node=99, src_socket=99,
                proto_type=10,
                data=struct.pack('>BBHLHHhL', 2, 1, boot_machine_id, boot_timestamp, 512, 0, 0, len(image) // 512).ljust(586, b'\0')
            ),
            (MCAST_ADDR, MCAST_PORT))

        elif boot_type == 3:
            # It seems to want part of the boot image!
            # print('it wants data', data)

            # typedef struct
            # {
            #     unsigned    short   imageID;    /* */
            #     unsigned    char    section;    /* "section" of the image the bitmap refers to */
            #     unsigned    char    flags;      /* ??? */
            #     unsigned    short   replyDelay;
            #     unsigned    char    bitmap[512];    /* bitmap of the section of the image requested */
            # }bir; // Boot Image Req

            print('Boot Image Req')

            if len(data) < 6: continue
            boot_image_id, boot_section, boot_flags, boot_reply_delay = struct.unpack_from('>HBBH', data)
            data = data[6:]

            # Okay, pretty much just send the bits that were requested!
            print('Sending blocks')
            for blocknum in range(len(image) // 512):
                if len(data) > blocknum // 8 and (data[blocknum // 8] >> (blocknum % 8)) & 1:
                    # typedef struct  {
                    #     unsigned    char    packetType;     /* The command number */
                    #     unsigned    char    packetVersion;  /* Protocol version number */
                    #     unsigned    short   packetImage;    /* The image this block belongs to */
                    #     unsigned    short   packetBlockNo;  /* The block of the image (starts with 1) */
                    #     unsigned    char    packetData[512];/* the data portion of the packet */
                    #     } BootBlock,*BootBlockPtr;

                    # print(f' {blocknum}', end='', flush=True)
                    sock.sendto(mk_ddp(
                        dest_node=llap_src_node, dest_socket=ddp_src_socket,
                        src_node=99, src_socket=99,
                        proto_type=10,
                        data=struct.pack('>BBHH', 4, 1, boot_image_id, blocknum) + image[blocknum*512:blocknum*512+512]
                    ),
                    (MCAST_ADDR, MCAST_PORT))

                    # time.sleep(0.5)
                    # break # wait for another request, you mofo!

        elif boot_type > 4:
            print(f'protocol10 type={boot_type} vers={boot_vers} contents={repr(data)}')




    else:
        print('unknown ddp payload', ddp_proto_type)
















# ;            clr.l   D1
# ;            cmp.b   #1,$2C(A2)      ; ? ioPosMode == fsFromStart
# ;            beq.s   dontAddMark
# ;            move.l  $10(A3),D1      ; add dCtlPosition
# ;dontAddMark
# ;            cmp.b   #3,$2C(A2)      ; ? ioPosMode == fsFromMark
# ;            bne.s   dontAddOffset
# ;            add.l   $2E(A2),D1      ; add ioPosOffset
# ;dontAddOffset

