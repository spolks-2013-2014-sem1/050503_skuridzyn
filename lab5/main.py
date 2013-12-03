#!/usr/bin/env python

import os
import argparse
import sys
import socket
import select
import time

if __name__ == '__main__':
        sys.path.insert(0, \
        	os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spolkslib import netserver, netparser, netclient, rtwork, filework 

BUF_SIZE = 32*1024 
f_name = "file_1"

def server_routine(conn):

	global f_name
	rtr, rtw, ie = select.select([conn], [], [])
	if conn in rtr > 0:
		data, addr = rtwork.recieve_from(conn, BUF_SIZE)
		f = open(f_name, 'wb')
		print "connected by", addr
		f.write(data)
		rtwork.transmit_to(conn, "ACK", addr)
	else: return True
	
	
	while True:
		rtr, rtw, ie = select.select([conn], [], [], 10.0)
		if conn in rtr:
			data, addr = rtwork.recieve_from(conn, BUF_SIZE)
			if data == "FIN":
				break
			f.write(data)
			rtwork.transmit_to(conn, "ACK", addr)
		else: break
	
	print 'Client disconnected\nWaiting for the next client...'
	f.close()
	f_name = f_name[:-1] + str(int(f_name[-1]) + 1)
	return True 


def client_routine(s, f_name, host, port):
	print 'connected to', (host, port)
	f = open(f_name, 'rb')  
   	f_size = filework.get_fsize(f)
        bytes_send = 0
                
  	while True:
        	buffer = f.read(BUF_SIZE)
		rtwork.transmit_to(s, buffer, (host, port))
		rtr, rtw, ie = select.select([s], [], [], 10.0)
		if s in rtr:
			ack, addr = rtwork.recieve_from(s, 3)
		if ack != "ACK": 
			rtwork.transmit_to(s, buffer, (host, port))			
		if bytes_send == f_size:
			rtwork.transmit_to(s, "FIN", (host, port))
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
		netserver.run_udp_server(args.port, server_routine)
	elif args.m == 'user':
		print args.host, args.port, args.fname
		netclient.run_udp_client(args.host, args.port, 
			client_routine, (args.fname, args.host, args.port))	

if __name__ == "__main__":
	main()
