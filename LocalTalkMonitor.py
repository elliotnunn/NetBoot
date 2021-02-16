#!/usr/bin/env python3

# Multicast client
# Adapted from: http://chaos.weblogs.us/archives/164

import socket
import os
from os import path
import struct



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



while 1:
    data, addr = sock.recvfrom(1024)

    if len(data) < 4: continue
    data = data[4:] # Trim down to LLAP packet (not "frame")

    if len(data) < 3: continue
    llap_dest_node = data[0]
    llap_src_node = data[1]
    llap_proto_type = data[2]
    data = data[3:] # Trim down to LLAP payload

    if llap_proto_type == 1:
        # ddp, short
        if len(data) < 5: continue
        ddp_len, ddp_dest_socket, ddp_src_socket, ddp_proto_type = struct.unpack_from('>HBBB', data)
        data = data[5:ddp_len]
    elif llap_proto_type == 2:
        # ddp, long (what should we do with this extra information?)
        if len(data) < 13: continue
        ddp_len, ddp_cksum, ddp_dest_net, ddp_src_net, ddp_dest_node, ddp_src_node, ddp_dest_socket, ddp_src_socket, ddp_proto_type = struct.unpack_from('>4H5B', data)
        ddp_hop_count = (ddp_len >> 10) & 0xF
        ddp_len &= 0x3FF
        data = data[13:ddp_len]
        print(ddp_src_net, ddp_dest_net)
    else:
        # llap control packet -- can probably ignore!
        continue

    print(f'datagram {llap_proto_type} {llap_src_node}:{ddp_src_socket}->{llap_dest_node}:{ddp_dest_socket}')

    if ddp_proto_type == 2: # NBP
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

        print('    NBP func', nbp_func, 'id', nbp_id)
        for t in nbp_tuples:
            print(f'    net:node:sock={t[0]}:{t[1]}:{t[2]} enum={t[3]} object:type@zone={t[4]}:{t[5]}@{t[6]}')

    elif ddp_proto_type == 10: # ATBOOT
        if len(data) < 2:
            print('malformed short packet %r' % data.hex())
            continue
        boot_type, boot_vers = struct.unpack_from('>BB', data)

        if boot_type == 1:
            print('    ATBOOT "syn"', data[2:].hex())
        elif boot_type == 2:
            print('    ATBOOT "ack"', data[2:].hex())
        elif boot_type == 3:
            print('    ATBOOT image request', data[2:].hex())
        elif boot_type == 4:
            print('    ATBOOT image reply', data[2:].hex())
        elif boot_type >= 0x80:
            print('    ATBOOT Elliot', data.hex())
        else:
            print('    ATBOOT ???', boot_type, boot_vers, data[2:].hex())

    else:
        print('Totally unknown DDP type', ddp_proto_type)
        print('    ' + data.hex())
