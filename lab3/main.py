#!/usr/bin/env python

import os
import argparse
import sys
import socket

if __name__ == '__main__':
        sys.path.insert(0, \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spolkslib import networking
from spolkslib import netparser

BUF_SIZE = 65353 
		
def get_fsize(f):
	old_file_position = f.tell()
	f.seek(0, os.SEEK_END)
	size = f.tell()
	f.seek(old_file_position, os.SEEK_SET)	
	return size	

def client_routine(host, port, f_name):
	try:
		f = None
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client_socket.connect((host, port))
		f = open(f_name, 'rb')	
		f_size = get_fsize(f)
		bytes_send = 0
		
		while True:
			buffer = f.read(BUF_SIZE)
			if bytes_send == f_size:
				break
			success = networking.transmit(client_socket, buffer)
			if not success:
				break
			bytes_send += len(buffer) 
		
		client_socket.shutdown(1)
		f.close()
	except KeyboardInterrupt as e:
		print "Keyboard interrupt was detected!\n"
	except 	socket.error as e:
		print ("socket error %s" % e)
	except IOError as e:
		print "cannot open the file"
	finally:
		if client_socket != None:
			client_socket.shutdown(1)
		if f != None: f.close
		sys.exit(1)

f_name = "file_1"

def server_routine(conn):
	global f_name
	f = open(f_name, 'wb')
	while True:
		data = networking.recieve(conn, BUF_SIZE)
		if not data:
			break
		f.write(data)	
	f.close()
	f_name = f_name[:-1] + str(int(f_name[-1]) + 1)
	print f_name
	return True

def main():
	parser = argparse.ArgumentParser()
	p_type = netparser.parse_type('port')
	h_type = netparser.parse_type('ip')	

	parser.add_argument('-m', choices=['server', 'user'])
	parser.add_argument('-p', action='store', dest='port', type=p_type)
	parser.add_argument('-ip', action='store', dest='host', type=h_type)
	parser.add_argument('-f', action='store', dest='fname', type=str)	
	args = parser.parse_args()	
	
	if args.m == 'server':
		networking.run_server(args.port, server_routine)
	elif args.m == 'user':
		print args.host, args.port, args.fname
		client_routine(args.host, args.port, args.fname)	

if __name__ == "__main__":
	main()
