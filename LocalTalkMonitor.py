#!/usr/bin/env python3

# Multicast client
# Adapted from: http://chaos.weblogs.us/archives/164

import socket
import os
from os import path
import struct
import subprocess
import shutil



def get_ddp_type_name(n):
    if n == 1: s = 'RTMP'
    elif n == 2: s = 'NBP'
    elif n == 3: s = 'ATP'
    elif n == 4: s = 'AEP'
    elif n == 5: s = 'RTMP'
    elif n == 6: s = 'ZIP'
    elif n == 7: s = 'ADSP'
    elif n == 10: s = 'ABP'
    else: s = '?'
    return '%d(%s)' % (n, s)

def hexdump(d):
    HEXCHUNK = 2
    wid, _ = shutil.get_terminal_size()
    lw = 2
    while 4 + lw//HEXCHUNK*(2*HEXCHUNK+1) + lw <= wid:
        lw *= 2
    lw //= 2
    ret = ''
    for i in range(0, len(d), lw):
        dd = d[i:i+lw]
        ret += '%03x|' % i
        hex = dd.hex().ljust(lw*2)
        for j in range(0, len(hex), 2*HEXCHUNK):
            ret += hex[j:j+2*HEXCHUNK] + ' '
        ret = ret[:-1] + '|'
        ret += ''.join(chr(c) if 32 <= c < 127 else '.' for c in dd).ljust(lw)
        ret += '\n'
    return ret



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
    else:
        # llap control packet -- can probably ignore!
        continue

    print(f'{get_ddp_type_name(ddp_proto_type)} {llap_src_node}:{ddp_src_socket}->{llap_dest_node}:{ddp_dest_socket}')
    print(hexdump(data))
