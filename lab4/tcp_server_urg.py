import socket, select
from spolkslib import rtwork, filework

__BUF_SIZE = 65536
__filename = "file_1"

def tcp_server_urg(server):

        global __filename
        data_length = 0
        conn, addr = server.accept()
        print "connected by", addr

        f = open(__filename, 'wb')
        while True:
                rtr, rtw, ie = select.select([conn], [], [conn], 1.0)
                if conn in ie:
			urg = conn.recv(__BUF_SIZE, socket.MSG_OOB)
			data = rtwork.recieve(conn, __BUF_SIZE)
			f.write(data)
                        print ("%s bytes recieved" % data_length)

                elif conn in rtr:
                        data = rtwork.recieve(conn, __BUF_SIZE)
                        if not data:
				print "STRANGE" 
				break

                        f.write(data)
                else: break
                data_length += len(data)

        f.close()
	conn.close()
        print 'Client disconnected\nWaiting for the next client...'
        __filename = __filename[:-1] + str(int(__filename[-1]) + 1)
        return True

