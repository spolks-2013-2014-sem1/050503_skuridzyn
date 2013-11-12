import socket
import sys
import signal
import argparse


def handler_wrap(s):
	"""returns interrupt handler with socket in closure"""
	def abort_handler(signum, frame):
		s.close()
		print "\nterminate"
		sys.exit(1)
	return abort_handler


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument("port_num", type=int)

	s = None
	BUF_SIZE = 1024

	try:	
		args = parser.parse_args()
		
		HOST = ''
		PORT = args.port_num
		
		
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((HOST, PORT))
		s.listen(1)

		#signal.signal(signal.SIGTERM, handler_wrap(s))
		#signal.signal(signal.SIGINT, handler_wrap(s))
	
		while 1:
			conn, addr = s.accept()
			conn.sendall("echo-server 3000 is at your service\n")
			print 'Connected by', addr

			while 1:
				data = conn.recv(BUF_SIZE)
				if data == "QUIT\n":
					conn.send("bye-bye\n")
					raise
				elif not data: 
					break
				conn.send(data)
	
		conn.close()
	except socket.error as e:
		print ("\nsocket errno %s" % (e))
	except KeyboardInterrupt as e:
		print ("keyboard interrupt detected")
	finally:
		if s != None:
			s.close()
		sys.exit(1)


if __name__ == "__main__":
    main()
