from spolkslib import rtwork, filework, netclient
import socket, select

__BUF_SIZE = 32 * 1024


def udp_client(client, filename, host, port):
	server = (host, port)
        print 'connected to', server
        f = open(filename, 'rb')
        f_size = filework.get_fsize(f)
        bytes_sended = 0

        while True:
                buffer = f.read(__BUF_SIZE)
		__resend_until_ack(client, buffer, server)
                
		if bytes_sended == f_size:
                        rtwork.transmit_to(client, "FIN", server)
                        break
                bytes_sended += len(buffer)
	
        client.close()
        f.close()

def __resend_until_ack(client, buffer, server):

	send_again = False
	while True:
		rtwork.transmit_to(client, buffer, server)
		while True:
			rtr, rtw, ie = select.select([client], [], [], 10.0)
			addr = None
		
			if client in rtr:
				ack, addr = rtwork.recieve_from(client, 3)
			
			if not addr:
				raise Exception("server is off-line")	
			if addr == server:
				if ack == "ACK": return True
				elif send_again: 
					raise Exception("server disconnected")
				else: 
					send_again = True
					break
