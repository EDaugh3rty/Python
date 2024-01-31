########
# Student name: Ethan Daugherty
# Course: COSC 3603 Section 01 – Networks
# Assignment:UDP Pinger
# Filename: daugherty02
#
# Purpose: To learn UDP programming
#
# Input: None
#
# Output: web server
#
# Assumptions:
#
# Limitations: The abilities of the programmer
#
# Development Computer: Macbook pro
# Operating System: MacOs Monterey
# Compiler:
# Integrated Development Environment (IDE): jGRASP
# Operational Status:
#######

from socket import *
import time

serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(10):

   try:
      message = 'Ping ' + str(i + 1) + " " + str(time.time())
      
      #sends message to the server
      start = time.time()
      clientSocket.sendto(message.encode(),(serverName, serverPort))
      modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
      end = time.time()
      timeTaken = end - start
      
      #prints the modified message
      print(modifiedMessage.decode())
      print("RTT: " + str(timeTaken) + "\n") 
   except:
      print("Request timed out \n")
      
#Close client socket
clientSocket.close()


