from spolkslib import rtwork, filework, netserver
import socket, select, os

__BUF_SIZE = 32*1024

def udp_server(server):

        filename = filework.random_name()
        rtr, rtw, ie = select.select([server], [], [])
        if server in rtr:
                data, client = rtwork.recieve_from(server, __BUF_SIZE)
                f = open(filename, 'wb')
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
	
	if not eof_detected:
		os.remove(filename)

        return True


