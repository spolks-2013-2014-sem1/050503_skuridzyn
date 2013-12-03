import socket
import sys

def __server_socket_create(port, host='', isTcp=True, listeners=1):

	if isTcp: sock_type = socket.SOCK_STREAM
	else: sock_type = socket.SOCK_DGRAM

	s = socket.socket(socket.AF_INET, sock_type)
	s.bind((host, port))
	if isTcp:
		s.listen(listeners)
	return s

def __tcp_server_routine(s, action, action_args=()):
	conn, addr = s.accept()
	print 'Connected by', addr
	wait_for_next = action(conn, *action_args)
	conn.close()
	return wait_for_next

def __udp_server_routine(s, action, action_args=()):
	return action(s, *action_args)

def __choose_routine(isTcp):

	"""chosese wether it'll be a tcp connection or udp"""

	if isTcp:
		return __tcp_server_routine
	else:
		return __udp_server_routine

#def make_server(port, action, action_args, isTcp=True, oneConnection=False):
def __make_server(port, action, action_args, isTcp=True, oneConnection=False):

	"""depending on parametres runs server on port <port>
	which applyes action to the input data, according to it's
	arguments <action_args>, it can be either tcp or udp server
	also it supports reconnection"""

	s = None

	try:
		s = __server_socket_create(port, '', isTcp)	
		server_routine = __choose_routine(isTcp)
			
		server_routine(s, action, action_args)
		while not oneConnection:
			if not server_routine(s, action, action_args):	
				break

	except socket.error as e:
		print ("\nsocket errno %s" % (e))
	except KeyboardInterrupt as e:
		print ("keyboard interrupt detected")
	except Exception as e:
		print ("exception occured %s" % (e))
	finally:
		if s != None:
			print "socket is closing"
			s.close()
		sys.exit(0)

def run_tcp_server(port, action, a_args=(), oneConnection=False):

	"""runs server with parametres: port - port number,
	action - which type of operation should server do
	action_args - 2-nd 3rd etc argumnets, first argumnet
	in declaration should always be the conn"""

	return __make_server(port, action, a_args, True, oneConnection)

def run_udp_server(port, action, a_args=(), oneConnection=False):
	return __make_server(port, action, a_args, False, oneConnection)
