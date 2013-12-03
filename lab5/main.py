#!/usr/bin/env python

import os
import argparse
import sys

if __name__ == '__main__':
        sys.path.insert(0, \
        	os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spolkslib import netserver, netparser, netclient, rtwork, filework 

from udp_client import * 
from udp_server import *
from tcp_client import *
from tcp_server import *
from tcp_server_urg import *
from tcp_client_urg import *

def main():
	parser = argparse.ArgumentParser()

	port = netparser.parse_type("port")
	
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group(required=True)

	group.add_argument('-t', '--tcp', action='store_true')
	group.add_argument('-u', '--udp', action='store_true')

	group = parser.add_mutually_exclusive_group(required=True)

	group.add_argument('-s', '--server', type=port, dest='port')
	group.add_argument('-c', '--client', nargs=3,  
		type=''.join, dest='args')
	parser.add_argument('--urgent', action='store_true')
	
	args = parser.parse_args()
	if args.args:
		cl_nfo = netparser.parse_list(args.args)
		cl_args = (getattr(cl_nfo, "filename"),
				getattr(cl_nfo, "host"), 
				getattr(cl_nfo, "port"))
			

	if args.udp:
		if args.port:
			print "server runs on port", args.port
			netserver.run_udp_server(args.port, udp_server)
		elif cl_nfo:
			print ("connecting to (%s, %s) ..." % 
				(cl_nfo.host, cl_nfo.port))

			netclient.run_udp_client(cl_nfo.host, 
			cl_nfo.port, udp_client, cl_args)
	elif args.tcp:
		if args.port:
			print "server runs on port", args.port
			if args.urgent:
				netserver.run_tcp_server(args.port,
					tcp_server_urg)
			else: netserver.run_tcp_server(args.port, tcp_server)
		elif cl_nfo:
			print ("connecting to (%s, %s)" % 
				(cl_nfo.host, cl_nfo.port))
			if args.urgent:
				netclient.run_tcp_client(cl_nfo.host,
				cl_nfo.port, tcp_client_urg, cl_nfo.filename)
			else:
				netclient.run_tcp_client(cl_nfo.host,
				cl_nfo.port, tcp_client, cl_nfo.filename)
		
if __name__ == "__main__":
	main()
