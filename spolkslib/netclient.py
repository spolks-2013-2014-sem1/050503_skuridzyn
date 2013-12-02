import socket
import sys


BUF_SIZE = 65353

def __client_socket_create(isTcp = True):
	if isTcp: sock_type = socket.SOCK_STREAM
	else: sock_type = socket.SOCK_DGRAM
	
	s = socket.socket(socket.AF_INET, sock_type)
	return s

def __tcp_client_routine(s, host, port, action, a_args=()):
	s.connect((host, port))
	if isinstance(a_args, tuple):
		action(s, *a_args)
	else: action(s, a_args)

def __udp_client_routine(s, host, port, action, a_args=()):
	if isinstance(a_args, tuple):
		action(s, *a_args)
	else: action(s, a_args)
	 
def __choose_routine(isTcp):
	if isTcp: return __tcp_client_routine
	else: return __udp_client_routine

def __make_client(host, port, action, a_args=(), isTcp=True):
	try:
		client_socket = __client_socket_create(isTcp)
		client_routine = __choose_routine(isTcp)
		
		client_routine(client_socket, host, port, action, a_args)

	except KeyboardInterrupt as e:
		print "Keyboard interrupt was detected!\n"
	except 	socket.error as e:
		print ("socket error %s" % e)
	except IOError as e:
		print "cannot open the file"
	except Exception as e:
		print e
	finally:
		if client_socket != None:
			client_socket.close()
			sys.exit(0)

def run_tcp_client(host, port, action, a_args=()):
	return __make_client(host, port, action, a_args)

def run_udp_client(host, port, action, a_args=()):
	return __make_client(host, port, action, a_args, False)
