########
# Student name: Ethan Daugherty
# Course: COSC 3143 Section 01 – Pi and Python
# Assignment: Programming Assignment 3
# Filename: daugherty03_client.py
#
# Purpose: to use a server on port 9000 that listens for data from a gui to change
#          the state of a RGB LED with options to toggle and blink five times
#
# Input: button click and gui
#
# Output: RGB LED lighting up
#
# Common Cathode RGB LED 
#######
import socket
import RPi.GPIO as GPIO
import tkinter as Tk
import time



#function to send a command to the server
def send_to_server(command):
	#creating a client to talk to the server
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(('localhost', 9000))
	client.sendall(command.encode())
	client.close()
	
	
root = Tk.Tk() #creating the main window and storing the window object in 'win'
root.title('Menu') #setting title of the window
lbl = Tk.Label(root, text="Change the state of the button")
lbl.pack()
assignment2 = Tk.Button(root, text="Assignment2 Settings", command=lambda: send_to_server("assign2"))
assignment2.pack()
toggle_state = Tk.Button(root, text="Toggle", command=lambda: send_to_server("toggle_state"))
toggle_state.pack()
blink = Tk.Button(root, text="Blink", command=lambda: send_to_server("blink"))
blink.pack()


root.mainloop() #running the loop that works as a trigger


