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
			print "connecting to (%s, %s) ..." % (cl_nfo.host, cl_nfo.port)
			netclient.run_udp_client(cl_nfo.host, 
			cl_nfo.port, udp_client, cl_args)

	
if __name__ == "__main__":
	main()
