import socket
import select
import sys
import os
from spolkslib import rtwork, filework

__TCP_BUF_SIZE = 65536
__UDP_BUF_SIZE = 32768


def __tcp_server_routine(server, verbosity=False):

    data_length = 0
    conn, addr = server.accept()
    print "connected by", addr

    filename = filework.random_name()
    f = open(filename, 'wb')

    while True:
        rtr, rtw, ie = select.select([conn], [], [conn], 10.0)

        if verbosity and conn in ie:
            urg = conn.recv(__TCP_BUF_SIZE, socket.MSG_OOB)
            data = rtwork.recieve(conn, __TCP_BUF_SIZE)
            f.write(data)
            print ("%s bytes recieved" % data_length)

        elif conn in rtr:
            data = rtwork.recieve(conn, __TCP_BUF_SIZE)
            if not data:
                break
            f.write(data)
        else:
            break

        data_length += len(data)

    f.close()
    conn.close()
    print 'Client disconnected\nWaiting for the next client...'

    return True


def __udp_server_routine(server):

    rtr, rtw, ie = select.select([server], [], [])
    if server in rtr:
        data, client = rtwork.recieve_from(server, __UDP_BUF_SIZE)
        filename = filework.random_name()
        f = open(filename, 'wb')
        print "connected by", client
        f.write(data)
        rtwork.transmit_to(server, "ACK", client)
    else:
        return True

    eof_detected = False
    while True:
        rtr, rtw, ie = select.select([server], [], [], 10.0)
        if server in rtr:
            data, addr = rtwork.recieve_from(server, __UDP_BUF_SIZE)
            if client != addr:
                continue
            if data == "FIN":
                eof_detected = True
                break
            f.write(data)
            rtwork.transmit_to(server, "ACK", client)
        else:
            break

    if not eof_detected:
        print 'eof is not detected! erase bufer data...'
        f.close()
        os.remove(filename)
    else:
        print 'Client disconnected\nWaiting for the next client...'
        f.close()

    return True


tcp_server = __tcp_server_routine
tcp_server_urg = lambda s: __tcp_server_routine(s, True)
udp_server = __udp_server_routine
