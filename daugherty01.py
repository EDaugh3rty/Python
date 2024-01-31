########
# Student name: Ethan Daugherty
# Course: COSC 3603 Section 01 – Networks
# Assignment: Programming Assignment 1
# Filename:
#
# Purpose: To make a simple web server.
#
# Input: None
#
# Output: web server
#
# Assumptions:
#
# Limitations: 
#
# Development Computer: Macbook Pro
# Operating System: MacOS
# Compiler:
# Integrated Development Environment (IDE):JGRASP
# Operational Status:
#######

#import socket module
from socket import *
import sys # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(('localhost',serverPort))
serverSocket.listen(1)
print("The server is ready to receive")

while True:
   #Establish the connection
   print('Ready to serve...')
   connectionSocket, addr = serverSocket.accept()
   try:
      message = connectionSocket.recv(1024).decode()
      filename = message.split()[1]
      f = open(filename[1:])
      outputdata = f.read()
      #Send one HTTP header line into socket
      connectionSocket.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'.encode())
      #Send the content of the requested file to the client
      for i in range(0, len(outputdata)):
         connectionSocket.send(outputdata[i].encode())
      connectionSocket.send("\r\n".encode())
      connectionSocket.close()
   except IOError:
      #Send response message for file not found
      connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
      
      #Close client socket
      connectionSocket.close()
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
