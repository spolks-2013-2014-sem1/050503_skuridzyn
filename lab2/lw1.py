import socket
import sys
import signal


s = None

#interruption handler
def abort_handler(signum, frame):
	global s
	print '\nterminate\n'
	if s != None:
		s.close()
		s = None
	sys.exit(1)

signal.signal(signal.SIGTERM, abort_handler)
signal.signal(signal.SIGINT, abort_handler)
HOST = ''
PORT = 50007

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connected by', addr

while 1:
	data = conn.recv(1024)
	if not data: break
	conn.sendall(data)
conn.close()

