import socket, select
from spolkslib import rtwork, filework

__BUF_SIZE = 65536

def tcp_server_urg(server):

        filename = filework.random_name()
        data_length = 0
        conn, addr = server.accept()
        print "connected by", addr

        f = open(filename, 'wb')
        while True:
                rtr, rtw, ie = select.select([conn], [], [conn], 1.0)
                if conn in ie:
			urg = conn.recv(__BUF_SIZE, socket.MSG_OOB)
			data = rtwork.recieve(conn, __BUF_SIZE)
			f.write(data)
                        print ("%s bytes recieved" % data_length)

                elif conn in rtr:
                        data = rtwork.recieve(conn, __BUF_SIZE)
                        if not data: break
                        f.write(data)
                else: break
                data_length += len(data)

        f.close()
	conn.close()
        print 'Client disconnected\nWaiting for the next client...'
        return True

