#!/usr/bin/python

import os
import argparse
import sys


if __name__ == '__main__':
    sys.path.insert(0, \
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from spolkslib import netserver, netparser


BUF_SIZE = 1024


def echo_server_routine(server):

    conn, addr = server.accept()
    print "connected by", addr

    while True:
        data = conn.recv(BUF_SIZE)

        if data == "QUIT\n":
            conn.close()
            return False

        if not data:
            break

        conn.send(data)

    print "{0} disconnected".format(addr)
    conn.close()

    return True


def main():

    parser = netparser.create_parser('-s')
    port = parser.parse_args().port
    netserver.run_tcp_server(port, echo_server_routine)

if __name__ == "__main__":
    main()
