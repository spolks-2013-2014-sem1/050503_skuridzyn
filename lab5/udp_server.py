from spolkslib import rtwork, filework, netserver
import socket, select, os

__BUF_SIZE = 32*1024
__filename = "file_1"

def udp_server(server):

        global __filename
        rtr, rtw, ie = select.select([server], [], [])
        if server in rtr:
                data, client = rtwork.recieve_from(server, __BUF_SIZE)
                f = open(__filename, 'wb')
                print "connected by", client
                f.write(data)
                rtwork.transmit_to(server, "ACK", client)
        else: return True

	eof_detected = False
        while True:
                rtr, rtw, ie = select.select([server], [], [], 10.0)
                if server in rtr:
                        data, addr = rtwork.recieve_from(server, __BUF_SIZE)
			if client != addr:
				continue
                        if data == "FIN":
				eof_detected = True
                                break
                        f.write(data)
                        rtwork.transmit_to(server, "ACK", client)
                else: break
	
	if not eof_detected:
		print 'eof is not detected! erase bufer data...'
        print 'Client disconnected\nWaiting for the next client...'
        f.close()
	
	if eof_detected:
        	__filename = __filename[:-1] + str(int(__filename[-1]) + 1)
	else:
		os.remove(__filename)

        return True


