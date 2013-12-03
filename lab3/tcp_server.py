import socket, select
from spolkslib import rtwork, filework, netserver

__BUF_SIZE = 65536
__filename = "file_1"

def tcp_server(server):

        global __filename

        conn, addr = server.accept()
        print "connected by", addr

        f = open(__filename, 'wb')
        while True:
                rtr, rtw, ie = select.select([conn], [], [], 1.0)
                if conn in rtr:
                        data = rtwork.recieve(conn, __BUF_SIZE)
                        if not data:
                                break
                        f.write(data)
                else: break
        print 'Client disconnected\nWaiting for the next...'
        f.close()
        __filename = __filename[:-1] + str(int(__filename[-1]) + 1)
        return True

