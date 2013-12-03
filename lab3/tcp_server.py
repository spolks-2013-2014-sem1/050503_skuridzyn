import socket, select
from spolkslib import rtwork, filework

__BUF_SIZE = 65536

def tcp_server(server):

        filename = filework.random_name()

        conn, addr = server.accept()
        print "connected by", addr

        f = open(filename, 'wb')
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
        return True

