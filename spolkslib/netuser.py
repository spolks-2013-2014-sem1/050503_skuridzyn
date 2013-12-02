import socket
import sys


def run_client(host, port, action, a_args):
	BUF_SIZE = 65353
	try:
		client_socket = socket.socket(socket.AF_INET,\
			socket.SOCK_STREAM)

		client_socket.connect((host, port))
		action(client_socket, a_args)


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
