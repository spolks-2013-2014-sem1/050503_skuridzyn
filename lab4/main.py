#!/usr/bin/env python

import os, sys
import argparse

if __name__ == '__main__':
        sys.path.insert(0, \
        	os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spolkslib import netserver, netclient, netparser
from client import *
from server import *

def main():

        parser = argparse.ArgumentParser()
        port = netparser.parse_type('port')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument('-s', '--server', type=port, dest='port')
        group.add_argument('-c', '--client', nargs=3,
                type=''.join, dest='args')

	parser.add_argument('-v', '--verbosity', action='store_true')
        args = parser.parse_args()

        if args.args:
                cl_nfo = netparser.parse_list(args.args)
                cl_args = (getattr(cl_nfo, "filename"),
                                getattr(cl_nfo, "host"),
                                getattr(cl_nfo, "port"))

        if args.port:
		if args.verbosity:
                	netserver.run_tcp_server(args.port, tcp_server_urg)
		else: netserver.run_tcp_server(args.port, tcp_server)
        elif args.args:
		if args.verbosity:
                	netclient.run_tcp_client(cl_nfo.host, cl_nfo.port,
                        	tcp_client_urg, cl_nfo.filename)
		else: netclient.run_tcp_client(cl_nfo.host, cl_nfo.port,
				tcp_client, cl_nfo.filename)


if __name__ == "__main__":
        main()

