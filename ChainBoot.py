#!/usr/bin/env python3

# Multicast client
# Adapted from: http://chaos.weblogs.us/archives/164

import socket
import os
from os import path
import struct
import sys

import time
import random

from snefru_hash import append_snefru




ATBOOT_BLOCK_SIZE = 256 # must be a multiple of 64 or snefru will choke

UNRELIABILITY_PERCENT = 0
def failchance():
    return (random.random() < UNRELIABILITY_PERCENT/100)

my_unique_ltoudp_id = b'El' + (os.getpid() & 0xFFFF).to_bytes(2, 'big')


image = open('ChainLoader.bin', 'rb').read()
image2 = sys.argv[1:]
image2dict = {}
for img2name in image2:
    img2 = open(img2name, 'rb').read()
    img2name = path.basename(img2name)
    while len(img2) % 512: img2 += b'\0'
    image2dict[img2name] = bytearray(img2)

    img2name = img2name.encode('mac_roman')
#     image += struct.pack('>LB', len(img2)//512, len(img2name)) + img2name
    while len(image) % 2: image += b'\0'

# Constraint: client crashes when there is only one block
while len(image) <= ATBOOT_BLOCK_SIZE: image += b'\0'

# Constraint: client expects hash in the last 64 bytes of the last block
while len(image) % ATBOOT_BLOCK_SIZE != ATBOOT_BLOCK_SIZE - 64: image += b'\0'
image = append_snefru(image)

writable_image = bytearray(open('A608.dsk', 'rb').read())

open('/tmp/imgdebug', 'wb').write(image)

# typedef short (*j_code)(    short       command,  # SP+4 (sign-extend to long)
#                             DGlobals    *g,       # SP+8
#                             int         **var1,   # SP+12
#                             int         **var2);  # SP+16

# We return our OSErr in d0, and leave the 16 bytes of arguments on the stack for the caller to clean


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

def send(ddp):
    if failchance(): return
    sock.sendto(ddp, (MCAST_ADDR, MCAST_PORT))




def pstring(x):
    try:
        x = x.encode('mac_roman')
    except AttributeError:
        pass

    return bytes([len(x)]) + x



buf_sequence = -1



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
                send(mk_ddp(
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
                    pstring(nbp_tuples[0][4]) + pstring('BootServer') + pstring('*')
                ))

    elif ddp_proto_type == 10:
        # Mysterious ATBOOT protocol

        if len(data) < 2: continue
        boot_type, boot_vers = struct.unpack_from('>BB', data)
        whole_data = data
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
            send(mk_ddp(
                dest_node=llap_src_node, dest_socket=ddp_src_socket,
                src_node=99, src_socket=99,
                proto_type=10,
                data=struct.pack('>BBHLHHhL', 2, 1, boot_machine_id, boot_timestamp, ATBOOT_BLOCK_SIZE, 0, 0, len(image) // ATBOOT_BLOCK_SIZE).ljust(586, b'\0')
            ))

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
            for blocknum in range(len(image) // ATBOOT_BLOCK_SIZE):
#                 if len(data) > blocknum // 8 and (data[blocknum // 8] >> (blocknum % 8)) & 1:
                if 1:
                    # typedef struct  {
                    #     unsigned    char    packetType;     /* The command number */
                    #     unsigned    char    packetVersion;  /* Protocol version number */
                    #     unsigned    short   packetImage;    /* The image this block belongs to */
                    #     unsigned    short   packetBlockNo;  /* The block of the image (starts with 1) */
                    #     unsigned    char    packetData[512];/* the data portion of the packet */
                    #     } BootBlock,*BootBlockPtr;

                    # print(f' {blocknum}', end='', flush=True)
                    send(mk_ddp(
                        dest_node=llap_src_node, dest_socket=ddp_src_socket,
                        src_node=99, src_socket=99,
                        proto_type=10,
                        data=struct.pack('>BBHH', 4, 1, boot_image_id, blocknum) + image[blocknum*ATBOOT_BLOCK_SIZE:blocknum*ATBOOT_BLOCK_SIZE+ATBOOT_BLOCK_SIZE]
                    ))

                    # time.sleep(0.5)
                    # break # wait for another request, you mofo!

        elif boot_type == 128:
            boot_seq, boot_imgnum, boot_blkoffset, boot_blkcnt = struct.unpack_from('>HLLL', data); boot_imgname = b'A608.dsk'
            boot_blkcnt = min(boot_blkcnt, 32)
            boot_imgname = boot_imgname.decode('mac_roman')
            for blk in range(boot_blkoffset, boot_blkoffset + boot_blkcnt):
                thisblk = writable_image[blk*512:blk*512+512]
                send(mk_ddp(
                    dest_node=llap_src_node, dest_socket=ddp_src_socket,
                    src_node=99, src_socket=99,
                    proto_type=10,
                    data=struct.pack('>BBH', 129, blk-boot_blkoffset, boot_seq) + thisblk
                ))

        elif boot_type == 130:
            boot_type, blk, seq, boot_imgnum, hunk_start = struct.unpack_from('>BBHLL', whole_data)
            if seq != buf_sequence:
                buf_sequence = seq
                buf = bytearray(32*512)

            putdata = whole_data[8:]
            buf[(blk % 32) * 512:(blk % 32) * 512 + len(putdata)] = putdata

            if blk & 0x80:
                del buf[(blk % 32) * 512 + 512:]
                writable_image[hunk_start*512:hunk_start*512+len(buf)] = buf

                send(mk_ddp(
                    dest_node=llap_src_node, dest_socket=ddp_src_socket,
                    src_node=99, src_socket=99,
                    proto_type=10,
                    data=struct.pack('>BBH', 131, 0, seq)
                ))

        else:
            print(f'ATBOOT type={boot_type} vers={boot_vers} contents={repr(data)}')




    else:
        print('unknown ddp payload', ddp_proto_type)
