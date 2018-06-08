'''
Created on 2018-6-5
Function:Server-Client chat and file transfer
@Author:BuYuqi
'''
#import packets
from socket import *
import socket
import os
import sys
import stat

HOST = ''
PORT = 8000 #port no.
BUFSIZ = 1048576 #1MB
ADDR = (HOST,PORT)

#create a socket(TCP)
try:
	tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	print 'Failed to create socket. Error code: ' + str(msg[0]) + ' ,Error message: ' + msg[1]
	sys.exit();

tcpSerSock.bind(ADDR) #bind listening port
tcpSerSock.listen(5) #listening queue for 5

while True:
    print 'Waiting for connection...'
    tcpCliSock,addr = tcpSerSock.accept() #connect to client
    print 'Connected from:',addr

    while True:
        data = tcpCliSock.recv(BUFSIZ) #receive message from client
        if not data or data=='exit':
            	break
        print '[From Client]: ',data
	if data=='file':
		filename = tcpCliSock.recv(BUFSIZ) #receive the file name
		print '[From Client] Filename is ',filename
		fileaddr = raw_input("Input the address you want to put the file in(e.g. a.txt):")
		os.mknod(fileaddr) #create a file
		os.chmod(fileaddr,stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO) #set the permission of the new file
		f = open(fileaddr,'wb') #open the file
		l = tcpCliSock.recv(BUFSIZ) #receive the file
		print 'Receiving ...'
		f.write(l) #write it to the new file
		f.close() #close the file
		print 'Received'
	if data=='hi':
		print 'Server > hi'
		tcpCliSock.send('hi') #send message to client
	else:
        	message = raw_input('Server > ') #input message
        	tcpCliSock.send(message) #send message to client

tcpSerSock.close()
