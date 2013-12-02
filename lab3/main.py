#!/usr/bin/env python

import os
import argparse
import sys
import socket
import select

if __name__ == '__main__':
        sys.path.insert(0, \
        	os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spolkslib import networking
from spolkslib import netparser
from spolkslib import netuser
from spolkslib import filework

BUF_SIZE = 65353 
		

f_name = "file_1"

def server_routine(conn):
	global f_name
	f = open(f_name, 'wb')
	while True:
		client, rtw, ie = select.select([conn], [], [], 1.0)
		if len(client) > 0:
			data = networking.recieve(conn, BUF_SIZE)
			if not data:
				break
			f.write(data)
		else: break
	print 'Client disconnected\nWaiting for the next...'	
	f.close()
	f_name = f_name[:-1] + str(int(f_name[-1]) + 1)
	return True


def client_routine(s, f_name):
	f = open(f_name, 'rb')  
   	f_size = filework.get_fsize(f)
        bytes_send = 0
                
  	while True:
        	buffer = f.read(BUF_SIZE)
		rtr, server, ie = select.select([], [s], [], 2.0)
			
		if len(server) > 0:
           		success = networking.transmit(s, buffer)
    		else: break

		if bytes_send == f_size:
            		break
         	if not success:
              		break
         	bytes_send += len(buffer) 
                
    	s.close()
	f.close()


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
		netuser.run_client(args.host, args.port, 
			client_routine, args.fname)	

if __name__ == "__main__":
	main()
