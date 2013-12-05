import socket
import select
from spolkslib import rtwork, filework

__TCP_BUF_SIZE = 65536


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

tcp_server = __tcp_server_routine
tcp_server_urg = lambda s: __tcp_server_routine(s, True)
