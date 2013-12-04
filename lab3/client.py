import socket, select
from spolkslib import rtwork, filework


__TCP_BUF_SIZE = 65536

def __tcp_client_routine(conn, filename):
        f = open(filename, 'rb')
        f_size = filework.get_fsize(f)
        bytes_sended = 0

        while True:
                buffer = f.read(__TCP_BUF_SIZE)
                rtr, rtw, ie = select.select([], [conn], [], 10.0)

                if conn in rtw:
                        success = rtwork.transmit(conn, buffer)
                else: break

                if bytes_sended == f_size or not success: break
                bytes_sended += len(buffer)

        conn.close()
        f.close()

tcp_client = __tcp_client_routine
