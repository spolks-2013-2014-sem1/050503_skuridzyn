#!/usr/bin/env python

import os
import sys
import argparse

if __name__ == '__main__':
    sys.path.insert(0, \
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from spolkslib import netserver, netparser, netclient

from server import *
from client import *


def main():

    parser = netparser.create_parser('-c', '-s')
    args = parser.parse_args()

    if args.args:
        cl_nfo = netparser.parse_list(args.args)
        cl_args = (cl_nfo.filename, cl_nfo.host, cl_nfo.port)

    if args.port:
        netserver.run_tcp_server(args.port, tcp_server)
    elif args.args:
        netclient.run_tcp_client(cl_nfo.host, cl_nfo.port,
        tcp_client, (cl_nfo.filename,))


if __name__ == "__main__":
    main()
