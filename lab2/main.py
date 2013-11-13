import networking 
import netparser
import argparse
import os

if __name__ == '__main__':
	sys.path.insert(0, os.path.abspath(os.path.dirname(__file__), "..")))



def echo_server_routine(conn):
	while 1:
		data = conn.recv(1024)
		if data == "QUIT\n":
			raise
		conn.send(data)


def main():
	parser = argparse.ArgumentParser()
	parse_t = netparser.parse_type("port")
	parser.add_argument("port", type=parse_t, help="port number in range [0,65353)")
	
	port = parser.parse_args().port	
	networking.run_server(port, echo_server_routine)

if __name__ == "__main__":
	main()
