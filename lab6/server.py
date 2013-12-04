import socket, select, sys, os
from spolkslib import rtwork, filework



__TCP_BUF_SIZE = 65536
__UDP_BUF_SIZE = 32768

class Connection(object):

	"""class holding connection unit consisting
	of socket object, addres info, associated
	filename and file descriptor, and length of
	received data"""

	def __init__(self, socket, addr, fin=True):

		"""initialize connection object
		filename generates randomly"""

		self.socket = socket
		self.addr = addr
		self.filename = filework.random_name()
		self.data_length = 0
        	self.f = open(self.filename, 'wb')
		self.fin = fin

	def __del__(self):

		"""destructor: called when number of
		pointers on object is equal to zero
		and closes socket and file descriptor"""
		
		if self.fin == True and self.socket:
			self.socket.close()
			self.f.close()
		
		elif self.fin == False:
			print "eof from client {0} was not detected\nfile will be erased".format(self.addr)
			os.remove(self.filename)

class ConnTable(object):

	"""connections table holds connection units
	described above"""

	def __init__(self):
		
		"""inital table entry is empty"""

		self.table = []

	def add(self, socket, addr, fin=True):
		element = Connection(socket, addr, fin)
		self.table.append(element)

	def remove(self, socket):

		"""removes connection from list and
		delete it"""

		conn = self.get(socket)
		del conn
		self.table = [el for el in self.table if el.socket != socket]
		
		return True

	def remove_addr(self, addr):

		conn = self.get_addr(addr)
		del conn
		self.table = [el for el in self.table if el.addr != addr]
		
		return True
	
	def get(self, socket):
		
		"""return connection unit by socket"""

		for el in self.table:
			if socket == el.socket:
				return el
		else: return None
	
	def get_addr(self, addr):

		for el in self.table:
			if addr == el.addr:
				return el
		else: return None
	
	def values(self):

		"""returns all sockets in table"""

		values = []
		for el in self.table:
			values.append(el.socket)

		return values

	def addrs(self):
		values = []
		for el in self.table:
			value.append(el.addr)

		return values
		

def __tcp_server_routine(server, verbosity=False):

	#initialize connections table
	connTable = ConnTable()

        while True:
		open_connections = connTable.values()
                rtr, rtw, ie = select.select(open_connections + [server], 
					[], open_connections)
		for s in rtr:
			if s == server:
				conn, addr = server.accept()
				connTable.add(conn, addr)
				continue

			receive_data = False
			conn = connTable.get(s)
			if verbosity and conn.socket in ie:
				receive_data = True
                        	urg = s.recv(__TCP_BUF_SIZE, socket.MSG_OOB)
                        	print "{0} from {1} bytesrecieved".format(conn.data_length, conn.addr)

               	 	if conn.socket in rtr or receive_data:
				receive_data = False
                        	data = rtwork.recieve(s, __TCP_BUF_SIZE)
                        	if not data:
        				print 'Client {0} disconnected!'.format(conn.addr)
					connTable.remove(s)
					conn.fin = True
					del conn
					continue
                        	conn.f.write(data)
                	else: continue
                	conn.data_length += len(data)
        return True


def __udp_server_routine(server):

	connTable = ConnTable()

	while True:
		rtr, rtw, ie = select.select([server], [], [])
		if server in rtr:
			data, client = rtwork.recieve_from(server, __UDP_BUF_SIZE)
			if not connTable.get_addr(client):
				print 'client {0} connected'.format(client)
				connTable.add(None, client, False)
			
			conn = connTable.get_addr(client)

			if data == "FIN":
				print 'client {0} disconnected'.format(conn.addr)
				conn.fin = True
				connTable.remove_addr(client)
				del conn
			else:
				conn.f.write(data)
				rtwork.transmit_to(server, "ACK", client)	
        return True


tcp_server = __tcp_server_routine
tcp_server_urg = lambda s: __tcp_server_routine(s, True)
udp_server = __udp_server_routine

