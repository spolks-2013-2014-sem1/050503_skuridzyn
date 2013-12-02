import socket
import sys

def server_socket_create(port, host='', isTcp=True, listeners=1):

	if isTcp: sock_type = socket.SOCK_STREAM
	else: sock_type = socket.SOCK_DGRAM

	s = socket.socket(socket.AF_INET, sock_type)
	s.bind((host, port))
	if isTcp:
		s.listen(listeners)
	return s

def tcp_server_routine(s, action, action_args=(), greetings="tcp-server is at your service\n"):
	conn, addr = s.accept()
	print 'Connected by', addr
	wait_for_next = action(conn, *action_args)
	conn.close()
	return wait_for_next

def udp_server_routine(s, action, action_args=(), greetings="udp-server is at your service\n"):
	data, addr = sock.recvfrom(1024)
	action(addr, *action_args)

def choose_routine(isTcp):

	"""chosese wether it'll be a tcp connection or udp"""

	if isTcp:
		return tcp_server_routine
	else:
		return udp_server_routine

#def make_server(port, action, action_args, isTcp=True, oneConnection=False):
def make_server(port, action, action_args, isTcp=True, oneConnection=False):

	"""depending on parametres runs server on port <port>
	which applyes action to the input data, according to it's
	arguments <action_args>, it can be either tcp or udp server
	also it supports reconnection"""

	s = None
	BUF_SIZE = 1024

	try:
		s = server_socket_create(port)	
		server_routine = choose_routine(isTcp)
			
		server_routine(s, action, action_args)
		while not oneConnection:
			if not server_routine(s, action, action_args):	
				break

	except socket.error as e:
		print ("\nsocket errno %s\n" % (e))
	except KeyboardInterrupt as e:
		print ("keyboard interrupt detected\n")
	except Exception as e:
		print ("exception occured %s\n" % (e))
	finally:
		if s != None:
			print "socket is closing\n"
			s.close()
		sys.exit(1)

def run_server(port, action, action_args=(), isTcp=True, oneConnection=False):

	"""runs server with parametres: port - port number,
	action - which type of operation should server do
	action_args - 2-nd 3rd etc argumnets, first argumnet
	in declaration should always be the conn"""

	make_server(port, action, action_args, isTcp, oneConnection)


def transmit(s, buffer):
	try:
		buffer_size = len(buffer)
		bytes_sended = s.send(buffer)

		while (bytes_sended < buffer_size):
			buffer = buffer[bytes_sended:]
			buffer_size = len(buffer)
			bytes_sended = s.send(buffer)
		
		return True
	except Exception as e:
		print ("send buffer error %s" %  e)
		return False

def recieve(s, buf_size):
	buffer, readed = '', 0
	try:
		while (True):
			if readed == buf_size:
				break
			chunk = s.recv(buf_size - readed)
			if not chunk:
				break
			readed += len(chunk)
			buffer += chunk
	except Exception as e:
		print ("recieve buffer error %s" % e)
	finally:
		return buffer
