'''
Created on 2018-6-7
Function:Server-Clients chat using non-blocking TCP socket
@Author:BuYuqi
'''
#import packets
import socket
import select
import sys

HOST = '192.168.201.129' #serverIP
PORT = 8000 #port no.
BUFSIZ = 1048576 #1MB
ADDR = (HOST,PORT)
SockList = []

#create a socket(TCP)
try:
    tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' ,Error message: ' + msg[1]
    sys.exit();

tcpCliSock.connect(ADDR) #connect to server

SockList.append(tcpCliSock) #put tcpCliSock into SockList
SockList.append(sys.stdin) #put the input message into SockList

print ('Connected to Server')
sys.stdout.write('Client > ')
sys.stdout.flush() #clean up the buffer

while True:
    read_sock, write_sock, error_sock = select.select(SockList, [], [])
    for sock in read_sock: #when data read in
        if sock == tcpCliSock: #data of server
            data = sock.recv(BUFSIZ) #receive message from server
            if not data:
                sys.exit()
            else:
                sys.stdout.write('\r' + data) #show the message on the screen
                sys.stdout.write('Client > ')
		sys.stdout.flush()
        else: #data of client
            msg = sys.stdin.readline() #input message
            tcpCliSock.send('\r[From Client] ' + msg) #send the message to server
            sys.stdout.write('Client > ')
	    sys.stdout.flush()
