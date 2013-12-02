#!/usr/bin/python

from __future__ import print_function
import os
import argparse
import sys

if __name__ == '__main__':
	sys.path.insert(0, \
		os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spolkslib import netserver, netparser

def echo_server_routine(conn):
	while 1:
		data = conn.recv(1024)
		if data == "QUIT\n":
			return False
		if not data:
			break
		conn.send(data)
	return True


def main():
	parser = argparse.ArgumentParser()
	parse_t = netparser.parse_type("port")
	parser.add_argument("port", type=parse_t, help="port number in range [0,65353)")
	
	port = parser.parse_args().port	
	netserver.run_tcp_server(port, echo_server_routine)

if __name__ == "__main__":
	main()
