#!/usr/bin/env python

import os
import argparse
import sys
import socket
import select

"""change path for searching libraries in 
higher directories"""

if __name__ == '__main__':
        sys.path.insert(0, \
        	os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

"""importing libraries"""

from spolkslib import netserver, netclient, netparser, rtwork, filework

BUF_SIZE = 65536 #send/receive block size
f_name = "file_1" #initial name for saving filenames
URG_PERIOD = 1048576 #urgent data send period ~ 1 MB

def server_routine(conn):

	"""server action"""

        global f_name
	i = 0
	data_length = 0
        f = open(f_name, 'wb')
        while True:
		
		#polling for usual and OOB data with time-out ~ 1s
                client, rtw, ie = select.select([conn], [], [conn], 1.0)
		
		if len(ie) > 0:
			try: urg = conn.recv(BUF_SIZE, socket.MSG_OOB)
			except socket.error, value: urg = None
			if urg:
				print ("%s bytes recieved" % data_length)

		#usual data  detected
                if len(client) > 0:
                        data = rtwork.recieve(conn, BUF_SIZE)
                        
			#client disconnected
			if not data:
                     		break
                	
			f.write(data)
			
			#urgent data detected
		else: break
		data_length += len(data)

        print 'Client disconnected\nWaiting for the next client...'
        f.close()
        f_name = f_name[:-1] + str(int(f_name[-1]) + 1)
        return True

def client_routine(s, f_name):

	"""client action"""	

	i = 0
        f = open(f_name, 'rb')
        f_size = filework.get_fsize(f)
        bytes_send = 0

        while True:
		
		#if 1MB of usual have been sended since previous urgent data
		#send urgent again
		if bytes_send % URG_PERIOD == 0:
			s.send('!', socket.MSG_OOB)
			print ("%s bytes sended" % bytes_send)

                buffer = f.read(BUF_SIZE)
                rtr, server, ie = select.select([], [s], [], 1.0)

                if len(server) > 0:
                        success = rtwork.transmit(s, buffer)
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
                netserver.run_tcp_server(args.port, server_routine)
        elif args.m == 'user':
                print args.host, args.port, args.fname
                netclient.run_tcp_client(args.host, args.port,
                        client_routine, args.fname)

if __name__ == "__main__":
        main()

