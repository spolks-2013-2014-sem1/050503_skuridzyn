import socket, select
from spolkslib import rtwork, filework, netclient


__BUF_SIZE = 65536

def tcp_client(conn, filename):
        f = open(filename, 'rb')
        f_size = filework.get_fsize(f)
        bytes_sended = 0

        while True:
                buffer = f.read(__BUF_SIZE)
                rtr, rtw, ie = select.select([], [conn], [], 2.0)

                if conn in rtw:
                        success = rtwork.transmit(conn, buffer)
                else: break

                if bytes_sended == f_size or not success: break
                bytes_sended += len(buffer)

        conn.close()
        f.close()

