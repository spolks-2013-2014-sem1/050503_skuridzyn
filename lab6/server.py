import socket, select, sys, os
from spolkslib import rtwork, filework



__TCP_BUF_SIZE = 65536
__UDP_BUF_SIZE = 32768

class Connection:

	def __init__(self, socket, addr):
		self.socket = socket
		self.addr = addr
		self.filename = filework.random_name()
		self.data_length = 0
        	self.f = open(self.filename, 'wb')

	def __del__(self):
		print "delete"
		self.socket.close()
		self.f.close()

class ConnTable:
	def __init__(self):
		self.table = []

	def add(self, socket, addr):
		element = Connection(socket, addr)
		self.table.append(element)

	def remove(self, socket):
		print 'remove'
		self.table = [el for el in self.table if el.socket != socket]
		return True
	
	def get(self, socket):
		for el in self.table:
			if socket == el.socket:
				return el
		else: return None
	
	def values(self):
		values = []
		for el in self.table:
			values.append(el.socket)

		return values
		

def __tcp_server_routine(server, verbosity=False):

	connTable = ConnTable()
	i, j = 0, 0
        while True:
		open_connections = connTable.values()
                rtr, rtw, ie = select.select(open_connections + [server], 
					[], open_connections)
		for s in rtr:
			if s == server:
				conn, addr = server.accept()
				connTable.add(conn, addr)
				continue

			conn = connTable.get(s)
			if verbosity and conn.socket in ie:
				i += 1
                        	urg = s.recv(__TCP_BUF_SIZE, socket.MSG_OOB)
                        	data = rtwork.recieve(s, __TCP_BUF_SIZE)
				if not data:
					print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
					connTable.remove(s)
					print i, j
					continue
                        	conn.f.write(data)
                        	print "{0} from {1} bytes recieved".format(conn.data_length, conn.addr)

               	 	elif conn.socket in rtr:
				j += 1 
                        	data = rtwork.recieve(s, __TCP_BUF_SIZE)
                        	if not data:
        				print 'Client {0} disconnected\nWaiting for the next client...'.format(conn.addr)
					connTable.remove(s)
					print i, j
					continue	
                        	conn.f.write(data)
                	else: continue
                	conn.data_length += len(data)

        return True

def __udp_server_routine(server):

        rtr, rtw, ie = select.select([server], [], [])
        if server in rtr:
                data, client = rtwork.recieve_from(server, __UDP_BUF_SIZE)
		filename = filework.random_name()
                f = open(filename, 'wb')
                print "connected by", client
                f.write(data)
                rtwork.transmit_to(server, "ACK", client)
        else: return True

        eof_detected = False
        while True:
                rtr, rtw, ie = select.select([server], [], [], 10.0)
                if server in rtr:
                        data, addr = rtwork.recieve_from(server, __UDP_BUF_SIZE)
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

tcp_server = __tcp_server_routine

tcp_server_urg = lambda s: __tcp_server_routine(s, True)

udp_server = __udp_server_routine

