import socket
import select
from spolkslib import rtwork, filework

__TCP_BUF_SIZE = 65536


def __tcp_server_routine(server):

    filename = filework.random_name()

    conn, addr = server.accept()
    print "connected by", addr

    f = open(filename, 'wb')
    while True:
        rtr, rtw, ie = select.select([conn], [], [], 10.0)
        if conn in rtr:
            data = rtwork.recieve(conn, __TCP_BUF_SIZE)
            if not data:
                break
            f.write(data)
        else:
            break

    print '{0} disconnected\nWaiting for the next...'.format(addr)
    f.close()

    return True

tcp_server = __tcp_server_routine
