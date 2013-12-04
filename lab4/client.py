import socket
import select
from spolkslib import rtwork, filework

__URG_PERIOD = 1048576
__TCP_BUF_SIZE = 65536


def __tcp_client_routine(conn, filename, verbosity=False):

    f = open(filename, 'rb')
    f_size = filework.get_fsize(f)
    bytes_sended = 0

    while True:
        if verbosity and bytes_sended % __URG_PERIOD == 0:
            conn.send('!', socket.MSG_OOB)
            print ("%s bytes sended" % bytes_sended)

        buffer = f.read(__TCP_BUF_SIZE)
        rtr, rtw, ie = select.select([], [conn], [], 10.0)

        if conn in rtw:
            success = rtwork.transmit(conn, buffer)
        else:
            break
        if bytes_sended == f_size or not success:
            break
        bytes_sended += len(buffer)

    conn.close()
    f.close()

    return True

tcp_client = __tcp_client_routine
tcp_client_urg = lambda conn, filename: __tcp_client_routine(conn,
filename, True)
