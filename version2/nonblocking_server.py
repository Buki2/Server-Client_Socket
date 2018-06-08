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
ConnList = []

#create a socket(TCP)
try:
    tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' ,Error message: ' + msg[1]
    sys.exit();

tcpSerSock.bind(ADDR) #bind listening port
tcpSerSock.listen(5) #listening queue for 5

ConnList.append(tcpSerSock) #put tcpSerSock into ConnList
ConnList.append(sys.stdin) #put the input message into ConnList

print ( 'Waiting For Connection ...')

while True:
    read_sock, write_sock, error_sock = select.select(ConnList, [], []) 
    for sock in read_sock: #when data read in
        if sock == tcpSerSock:
            tcpCliSock, addr = tcpSerSock.accept() #connect to client
            ConnList.append(tcpCliSock) #put tcpCliSock into ConnList
            print 'Connected from:', addr
	    sys.stdout.write('Server > ')
	    sys.stdout.flush() #clean up the buffer
        elif sock == sys.stdin: #data of server
	    sys.stdout.write('Server > ')
    	    sys.stdout.flush() 
            msg = sys.stdin.readline() #input message
	    for i in ConnList:
	        if i == tcpCliSock:
                    tcpCliSock.send('[From Server] ' + msg) #send the message to client           
        else: #data of client
            data = sock.recv(BUFSIZ) #receive message from client            
	    sys.stdout.write('\r' + data) #show the message on the screen
            sys.stdout.write('Server > ')
	    sys.stdout.flush()
