'''
Created on 2018-6-5
Function:Server-Client chat and file transfer
@Author:BuYuqi
'''
#import packets
import sys
from socket import * 

HOST = '192.168.201.129' #serverIP
PORT = 8000 #port no.
BUFSIZ = 1048576 #1MB
ADDR = (HOST,PORT)

#create a socket(TCP)
try:
	tcpCliSock = socket(AF_INET,SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' ,Error message: ' + msg[1]
	sys.exit();

tcpCliSock.connect(ADDR) #connect to server

while True:
    data = raw_input('Client > ') #input message
    if not data or data=='exit':
        break #disconnect
    tcpCliSock.send(data) #send message to server
    if data=='file':
        fileaddr = raw_input("Please input file's address(e.g. E:\\a.txt): ")
    	tcpCliSock.send(fileaddr) #send file address to server
        f = open(fileaddr, 'rb') #open the file
    	print 'Sending Data ...'
    	l = f.read() #read the file
    	tcpCliSock.send(l) #send the file
        f.close() #close the file
        print 'Sent'
    message = tcpCliSock.recv(BUFSIZ) #receive message from server
    if not data:
        break
    print '[From Server]: ',message

tcpCliSock.close()