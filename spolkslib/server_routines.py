import rtwork, filework
import socket, select, sys, os

__TCP_BUF_SIZE = 65536
__UDP_BUF_SIZE = 32768
__filename = "file_1"

def __tcp_server_routine(server, verbosity=False):

        global __filename
        data_length = 0
        conn, addr = server.accept()
        print "connected by", addr

        f = open(__filename, 'wb')
        while True:
                rtr, rtw, ie = select.select([conn], [], [conn], 10.0)
                if conn in ie and verbosity == True:
                        urg = conn.recv(__TCP_BUF_SIZE, socket.MSG_OOB)
                        data = rtwork.recieve(conn, __TCP_BUF_SIZE)
                        f.write(data)
                        print ("%s bytes recieved" % data_length)

                elif conn in rtr:
                        data = rtwork.recieve(conn, __TCP_BUF_SIZE)
                        if not data: break
                        f.write(data)
                else: break
                data_length += len(data)

        f.close()
        conn.close()
        print 'Client disconnected\nWaiting for the next client...'
        __filename = __filename[:-1] + str(int(__filename[-1]) + 1)
        return True

def __udp_server_routine(server):

        global __filename
        rtr, rtw, ie = select.select([server], [], [])
        if server in rtr:
                data, client = rtwork.recieve_from(server, __UDP_BUF_SIZE)
                f = open(__filename, 'wb')
                print "connected by", client
                f.write(data)
                rtwork.transmit_to(server, "ACK", client)
        else: return True

        eof_detected = False
        while True:
                rtr, rtw, ie = select.select([server], [], [], 10.0)
                if server in rtr:
                        data, addr = rtwork.recieve_from(server, __UDP_BUF_SIZE)
                        if client != addr:
                                continue
                        if data == "FIN":
                                eof_detected = True
                                break
                        f.write(data)
                        rtwork.transmit_to(server, "ACK", client)
                else: break

        if not eof_detected:
                print 'eof is not detected! erase bufer data...'
        print 'Client disconnected\nWaiting for the next client...'
        f.close()

        if eof_detected:
                __filename = __filename[:-1] + str(int(__filename[-1]) + 1)
        else:
                os.remove(__filename)

        return True

