########
# Student name: Ethan Daugherty
# Course: COSC 3603 Section 01 – Networks
# Assignment: Assignment 04
# Filename: daugherty04.py
#
# Purpose: To learn ICMP client programming
#
# Input: 
#
# Output: 
#
# Assumptions: 
#
# Limitations: 
# 
# Development Computer: Macbook Pro
# Operating System: macOs Monterey
# Compiler:  
# Integrated Development Environment (IDE): Jgrasp
# Operational Status:
#######
from socket import *
import os
import sys
import struct
import time
import select
import binascii
ICMP_ECHO_REQUEST = 8


#####
# Function: checksum(string)
#
# Parameters:
#	string 	the header and the data
#
# Returns: integer
#
# Assumptions: Valid input is inserted
#
# Limitations: No limitations
#
# Operational Status: Functional
######
def checksum(string):
	csum = 0
	countTo = (len(string) // 2) * 2
	count = 0

	while count < countTo:
		thisVal = string[count+1] * 256 + string[count]
		csum = csum + thisVal
		csum = csum & 0xffffffff
		count = count + 2

	if countTo < len(string):
		csum = csum + ord(string[len(string) - 1])
		csum = csum & 0xffffffff

	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum
	answer = answer & 0xffff
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer

#####
# Function: receiveOnePing(mySocket, ID, timeout, destAddr)
#
# Parameters:
#	mySocket	Socket
#   ID		  integer, the packet id
#   timeout	 integer, time until timeout
#   destAddr	string, the destination address
#
# Returns: String
#
# Assumptions: Valid input is inserted
#
# Limitations: No limitations
#
# Operational Status: Functional
######


def receiveOnePing(mySocket, ID, timeout, destAddr):
   timeLeft = timeout
   while 1:
      startedSelect = time.time()
      whatReady = select.select([mySocket], [], [], timeLeft)
      howLongInSelect = (time.time() - startedSelect)
      if whatReady[0] == []:  # Timeout
         return "Request timed out."
      
      timeReceived = time.time()
      recPacket, addr = mySocket.recvfrom(1024)
      
      #Fill in start
      
      #Fetch the ICMP header from the IP packet
      icmp_header = recPacket[20:28]
      icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq = struct.unpack("bbHHh", icmp_header) 
      doub_size = struct.calcsize("d")
      time_of_bytes = recPacket[28:28 + doub_size]
      time_sent = struct.unpack("d", time_of_bytes)[0]
      the_time = timeReceived - time_sent
      data = "Time Taken: " + str(the_time * 1000) + " ms " + "Type: " + str(icmp_type) + " "  + "Code: " + str(icmp_code) + " " + "Check Sum: " + str(icmp_checksum) + " " + "ID: " + str(icmp_id) + " " + "Sequence: " + str(icmp_seq)
      return data
      
      #Fill in End
      
      timeLeft = timeLeft - howLongInSelect
      
      if timeLeft <= 0:
      	return "Request timed out."

#####
# Function: sendOnePing(mySocket, destAddr, ID)
#
# Parameters:
#	mySocket	Socket
#   destAddr	string, the destination address
#   ID		  integer, the packet id
#
# Returns: Void
#
# Assumptions: Valid input is inserted
#
# Limitations: No limitations
#
# Operational Status: Functional
######


def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)

	myChecksum = 0
	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(bytes(header + data))

	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		# Convert 16-bit integers from host to network  byte order
		myChecksum = htons(myChecksum) & 0xffff
	else:
		myChecksum = htons(myChecksum)

	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data

	# AF_INET address must be tuple, not str
	mySocket.sendto(packet, (destAddr, 1))
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.


#####
# Function: doOnePing(destAddr, timeout)
#
# Parameters:
#   destAddr	string, the destination address
#   timeout	 integer, time until timeout
#
# Returns: String
#
# Assumptions: Valid input is inserted
#
# Limitations: No limitations
#
# Operational Status: Functional
######
def doOnePing(destAddr, timeout):
	icmp = getprotobyname("icmp")
	# Create Socket here
	mySocket = socket(AF_INET, SOCK_RAW, icmp)

	myID = os.getpid() & 0xFFFF  # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	delay = receiveOnePing(mySocket, myID, timeout, destAddr)

	mySocket.close()
	return delay

#####
# Function: ping(host, timeout)
#
# Parameters:
#   host	string
#   timeout	 integer, time until timeout
#
# Returns: String
#
# Assumptions: Valid input is inserted
#
# Limitations: No limitations
#
# Operational Status: Functional
######


def ping(host, timeout=1):
	dest = gethostbyname(host)
	print("Pinging " + dest + " using Python:")
	print("")
	# Send ping requests to a server separated by approximately one second
	while 1:
		delay = doOnePing(dest, timeout)
		print(delay)
		time.sleep(1)  # one second
	return delay


ping("localhost")
#ping("www.google.com") #North America
#ping("www.nationalgeographic.com") #Africa
#ping("www.bbc.co.uk") #Europe
#ping("www.mercadolibre.com.br") #South America